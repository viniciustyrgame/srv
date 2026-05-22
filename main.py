from flask import Flask, send_from_directory, request, Response
import os

app = Flask(__name__)

# Base URL identified: https://versionescommons.luna-corp.online/live/
# Assets directory: assets/android/

@app.route("/live/ver.php")
def ver_php():
    try:
        with open("assets/android/versioninfo", "r") as f:
            version = f.read().strip()
        return version
    except Exception as e:
        return str(e), 500

@app.route("/live/android/<path:filename>")
def serve_android_assets(filename):
    return send_from_directory("assets/android", filename)

@app.route("/live/<path:filename>")
def serve_live_root(filename):
    return send_from_directory("assets/android", filename)

if __name__ == "__main__":
    print("Servidor rodando em http://0.0.0.0:5000")
    print("Endpoints disponíveis:")
    print("  - http://localhost:5000/live/ver.php")
    print("  - http://localhost:5000/live/android/fileinfo")
    print("  - http://localhost:5000/live/android/versioninfo")
    app.run(host="0.0.0.0", port=5000)
