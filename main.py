from flask import Flask, send_from_directory, request, jsonify, Response
import os
import logging

app = Flask(__name__)

# Configurações para o Render: Porta dinâmica via variável de ambiente
PORT = int(os.environ.get("PORT", 5000))

# Configurar logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Base URL identificada na metadata: https://versionescommons.luna-corp.online/live/
# Estrutura de arquivos: assets/android/

@app.route("/")
def index():
    logging.info(f"Requisição HOME: {request.url}")
    return "Mini Servidor de Assets IL2CPP (Auto-Scan) rodando!"

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

    # Resposta padrão: JSON estruturado (mais comum para Unity)
    response_data = {
        "version": reported_version,
        "update_url": f"https://{request.host}/live/android/",
        "force_update": False, # Pode ser True se reported_version > current_version
        "message": "No new update available." if reported_version == current_version else "New update available."
    }
    
    # Se a versão reportada for maior que a atual, sugerir force_update
    if reported_version > current_version:
        response_data["force_update"] = True

    logging.info(f"Respondendo /live/ver.php com JSON: {response_data}")
    return jsonify(response_data)

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
