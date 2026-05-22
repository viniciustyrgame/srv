from flask import Flask, send_from_directory, request, jsonify
import os

app = Flask(__name__)

PORT = int(os.environ.get("PORT", 5000))

# Base URL identificada na metadata: https://versionescommons.luna-corp.online/live/
# Estrutura de arquivos: assets/android/

@app.route("/")
def index():
    return "Mini Servidor de Assets IL2CPP rodando!"

@app.route("/live/ver.php")
def ver_php():
    """
    Simula o endpoint de verificação de versão.
    Retorna um JSON com a versão e uma URL de atualização, como é comum em jogos Unity.
    """
    try:
        current_version = "1.17.1"
        if os.path.exists("assets/android/versioninfo"):
            with open("assets/android/versioninfo", "r") as f:
                current_version = f.read().strip()
        
        # Simula uma resposta de servidor de atualização
        response_data = {
            "version": current_version,
            "update_url": f"https://{request.host}/live/android/", # Usa o host atual para a URL de atualização
            "force_update": False,
            "message": "No new update available."
        }
        return jsonify(response_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/live/android/<path:filename>")
def serve_android_assets(filename):
    """
    Serve os arquivos de assets como fileinfo, versioninfo e bundles.
    """
    return send_from_directory("assets/android", filename)

@app.route("/live/<path:filename>")
def serve_live_root(filename):
    """
    Fallback para arquivos na raiz do diretório live.
    """
    return send_from_directory("assets/android", filename)

if __name__ == "__main__":
    # Garante que o diretório de assets existe e cria os arquivos
    os.makedirs("assets/android", exist_ok=True)
    
    fileinfo_content = '''gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
avatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0
avatar/uma_dcs,BSJQtQt6qEeFdLv8gsrVtPDQubo=,14523,0'''

    with open('assets/android/fileinfo', 'w') as f:
        f.write(fileinfo_content)

    with open('assets/android/versioninfo', 'w') as f:
        f.write('1.17.1')

    print(f"Servidor rodando na porta {PORT}")
    app.run(host="0.0.0.0", port=PORT)
