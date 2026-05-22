from flask import Flask, send_from_directory, request, Response
import os

app = Flask(__name__)

# Configurações para o Render: Porta dinâmica via variável de ambiente
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
    Muitos jogos Unity esperam apenas a string da versão ou um JSON simples.
    """
    try:
        if os.path.exists("assets/android/versioninfo"):
            with open("assets/android/versioninfo", "r") as f:
                version = f.read().strip()
            return version
        return "1.17.1" # Fallback para a versão informada
    except Exception as e:
        return str(e), 500

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
    # Garante que o diretório de assets existe
    os.makedirs("assets/android", exist_ok=True)
    
    print(f"Servidor rodando na porta {PORT}")
    app.run(host="0.0.0.0", port=PORT)
