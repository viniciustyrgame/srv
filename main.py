from flask import Flask, send_from_directory, request, jsonify, Response, render_template_string
import os
import logging

app = Flask(__name__)

PORT = int(os.environ.get("PORT", 5000))

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Variável global para controlar o formato da resposta do ver.php
# Pode ser 'text', 'json', 'pipe_separated'
response_mode = 'pipe_separated' # Default para o formato mais provável para Unity 5.6.3f1

@app.route("/")
def index():
    logging.info(f"Requisição HOME: {request.url}")
    global response_mode
    # Painel de controle simples para alternar o modo de resposta
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head><title>IL2CPP Mini Server Control</title></head>
    <body>
        <h1>IL2CPP Mini Server Control Panel</h1>
        <p>Current ver.php Response Mode: <strong>{response_mode}</strong></p>
        <form action="/set_response_mode" method="post">
            <label for="mode">Select ver.php Response Mode:</label>
            <select name="mode" id="mode">
                <option value="text" {'selected' if response_mode == 'text' else ''}>Plain Text (e.g., 1.17.1)</option>
                <option value="json" {'selected' if response_mode == 'json' else ''}>Full JSON</option>
                <option value="simple_json" {'selected' if response_mode == 'simple_json' else ''}>Simple JSON (version, update)</option>
                <option value="pipe_separated" {'selected' if response_mode == 'pipe_separated' else ''}>Pipe Separated (e.g., 1.17.1|false|url)</option>
            </select>
            <input type="submit" value="Set Mode">
        </form>
        <h2>Endpoints:</h2>
        <ul>
            <li><code>/live/ver.php</code></li>
            <li><code>/live/android/fileinfo</code></li>
            <li><code>/live/android/versioninfo</code></li>
        </ul>
        <p>Check Render logs for detailed request information.</p>
    </body>
    </html>
    """
    return render_template_string(html_content)

@app.route("/set_response_mode", methods=["POST"])
def set_response_mode():
    global response_mode
    new_mode = request.form.get('mode')
    if new_mode in ['text', 'json', 'simple_json', 'pipe_separated']:
        response_mode = new_mode
        logging.info(f"Modo de resposta do ver.php alterado para: {response_mode}")
    return index()

@app.route("/live/ver.php", methods=["GET", "POST"])
def ver_php():
    logging.info(f"Requisição para /live/ver.php: {request.url}")
    logging.info(f"  Método: {request.method}")
    logging.info(f"  Headers: {request.headers}")
    logging.info(f"  Query Params: {request.args}")
    if request.data:
        logging.info(f"  Corpo da Requisição: {request.data.decode()}")
    
    current_version = "1.17.1"
    if os.path.exists("assets/android/versioninfo"):
        with open("assets/android/versioninfo", "r") as f:
            current_version = f.read().strip()

    # Lógica para forçar uma versão superior, se solicitado
    force_higher_version = request.args.get("force_update_version")
    if force_higher_version:
        reported_version = force_higher_version
        logging.info(f"Forçando versão superior: {reported_version}")
    else:
        reported_version = current_version

    global response_mode
    if response_mode == 'json':
        response_data = {
            "version": reported_version,
            "update_url": f"https://{request.host}/live/android/",
            "force_update": False, 
            "message": "No new update available." if reported_version == current_version else "New update available."
        }
        if reported_version > current_version:
            response_data["force_update"] = True
        logging.info(f"Respondendo /live/ver.php com JSON completo: {response_data}")
        return jsonify(response_data)
    elif response_mode == 'simple_json':
        response_data = {
            "version": reported_version,
            "update": "false" if reported_version == current_version else "true"
        }
        logging.info(f"Respondendo /live/ver.php com JSON simplificado: {response_data}")
        return jsonify(response_data)
    elif response_mode == 'pipe_separated':
        # Formato comum em Unity mais antigos: version|update_needed|update_url
        update_needed = "false"
        if reported_version > current_version:
            update_needed = "true"
        response_string = f"{reported_version}|{update_needed}|https://{request.host}/live/android/"
        logging.info(f"Respondendo /live/ver.php com Pipe Separated: {response_string}")
        return Response(response_string, mimetype='text/plain')
    else: # 'text' ou qualquer outro default
        logging.info(f"Respondendo /live/ver.php com texto puro: {reported_version}")
        return Response(reported_version, mimetype='text/plain')

@app.route("/live/android/<path:filename>", methods=["GET", "POST"])
def serve_android_assets(filename):
    logging.info(f"Requisição para /live/android/{filename}: {request.url}")
    logging.info(f"  Método: {request.method}")
    logging.info(f"  Headers: {request.headers}")
    logging.info(f"  Query Params: {request.args}")
    if request.data:
        logging.info(f"  Corpo da Requisição: {request.data.decode()}")

    full_path = os.path.join("assets/android", filename)
    if os.path.exists(full_path):
        logging.info(f"Servindo arquivo: {full_path}")
        return send_from_directory("assets/android", filename)
    else:
        logging.warning(f"Arquivo não encontrado: {full_path}")
        return f"Arquivo {filename} não encontrado.", 404

@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
def catch_all(path):
    logging.info(f"Requisição CATCH-ALL para /{path}: {request.url}")
    logging.info(f"  Método: {request.method}")
    logging.info(f"  Headers: {request.headers}")
    logging.info(f"  Query Params: {request.args}")
    if request.data:
        logging.info(f"  Corpo da Requisição: {request.data.decode()}")
    
    full_path = os.path.join("assets/android", path)
    if os.path.exists(full_path):
        logging.info(f"Servindo arquivo via catch-all: {full_path}")
        return send_from_directory("assets/android", path)
    
    logging.warning(f"Nenhuma rota ou arquivo correspondente para /{path}. Respondendo com 200 OK genérico.")
    return jsonify({"status": "ok", "message": f"Received request for /{path}"}), 200

if __name__ == "__main__":
    os.makedirs("assets/android", exist_ok=True)
    
    fileinfo_content = '''gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0\nmain/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0\nlocalization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0\ningame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0\nconfig/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0\navatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0\navatar/uma_dcs,BSJQtQt6qEeFdLv8gsrVtPDQubo=,14523,0'''

    with open('assets/android/fileinfo', 'w') as f:
        f.write(fileinfo_content)

    with open('assets/android/versioninfo', 'w') as f:
        f.write('1.17.1')

    print(f"Servidor de Auto-Scan rodando na porta {PORT}")
    app.run(host="0.0.0.0", port=PORT)
