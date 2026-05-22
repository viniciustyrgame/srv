from flask import Flask, send_from_directory, request, jsonify, Response
import os
import logging
from datetime import datetime

app = Flask(__name__)

PORT = int(os.environ.get("PORT", "5000"))
BASE_URL = "https://srv-mtei.onrender.com"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# =========================================================
# LOGS EM MEMÓRIA
# =========================================================

logs_memory = []

def add_log(text):
    print(text)

    logs_memory.append(text)

    # limita memória
    if len(logs_memory) > 500:
        logs_memory.pop(0)

def scan_request(name):
    add_log("")
    add_log("=" * 70)
    add_log(f"{name} REQUEST")
    add_log("=" * 70)

    add_log(f"TIME: {datetime.now().strftime('%H:%M:%S')}")
    add_log(f"METHOD: {request.method}")
    add_log(f"RAW PATH: {request.full_path}")
    add_log(f"CLEAN PATH: {request.path}")

    add_log("")
    add_log("HEADERS:")

    for k, v in request.headers.items():
        add_log(f"{k}: {v}")

    add_log("")
    add_log("QUERY:")

    for k, v in request.args.items():
        add_log(f"{k}={v}")

    body = request.get_data()

    if body:
        add_log("")
        add_log("BODY:")

        try:
            add_log(body.decode())
        except:
            add_log("<binary body>")

    add_log("=" * 70)
    add_log("")


# =========================================================
# HOME COM VISUALIZADOR
# =========================================================

@app.route("/")
def home():

    html_logs = "<br>".join(logs_memory[-300:])

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Unity Live Scanner</title>

        <meta http-equiv="refresh" content="2">

        <style>

            body {{
                background: #0d1117;
                color: #00ff88;
                font-family: monospace;
                padding: 20px;
            }}

            h1 {{
                color: white;
            }}

            .box {{
                background: #161b22;
                border: 1px solid #30363d;
                padding: 15px;
                border-radius: 10px;
                white-space: pre-wrap;
                overflow-wrap: break-word;
            }}

        </style>
    </head>

    <body>

        <h1>UNITY LIVE REQUEST SCANNER</h1>

        <p>Status: ONLINE</p>
        <p>Port: {PORT}</p>

        <div class="box">
{html_logs}
        </div>

    </body>
    </html>
    """


# =========================================================
# VER.PHP
# =========================================================

@app.route("/live/ver.php", methods=["GET", "POST"])
def ver_php():

    scan_request("VER.PHP")

    response_text = (
        "1.17.1\r\n"
        f"{BASE_URL}/Versioninfo.txt\r\n"
        f"{BASE_URL}/Fileinfo.txt\r\n"
        f"{BASE_URL}/live/\r\n"
    )

    add_log("VER RESPONSE:")
    add_log(repr(response_text))

    return Response(
        response_text,
        mimetype="text/plain"
    )


# =========================================================
# FILEINFO
# =========================================================

FILEINFO_CONTENT = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
"""

VERSIONINFO_CONTENT = "1.17.1"


# =========================================================
# FILEINFO ROTAS
# =========================================================

@app.route("/Fileinfo")
@app.route("/fileinfo")
@app.route("/Fileinfo.txt")
@app.route("/fileinfo.txt")
@app.route("/live/Fileinfo")
@app.route("/live/fileinfo")
@app.route("/live/Fileinfo.txt")
@app.route("/live/fileinfo.txt")
def fileinfo():

    scan_request("FILEINFO")

    return Response(
        FILEINFO_CONTENT,
        mimetype="text/plain"
    )


# =========================================================
# VERSIONINFO ROTAS
# =========================================================

@app.route("/Versioninfo")
@app.route("/versioninfo")
@app.route("/Versioninfo.txt")
@app.route("/versioninfo.txt")
@app.route("/live/Versioninfo")
@app.route("/live/versioninfo")
@app.route("/live/Versioninfo.txt")
@app.route("/live/versioninfo.txt")
def versioninfo():

    scan_request("VERSIONINFO")

    return Response(
        VERSIONINFO_CONTENT,
        mimetype="text/plain"
    )


# =========================================================
# APP INFO LOGIN
# =========================================================

@app.route("/app/info/get")
def app_info():

    scan_request("APP INFO")

    return jsonify({
        "success": True,
        "status": "ok",
        "app_id": "100067",
        "client_version": "2018120316"
    })


# =========================================================
# LIVE FILES
# =========================================================

@app.route("/live/<path:path>", methods=["GET", "POST"])
def live_files(path):

    scan_request("LIVE FILE")

    full = os.path.join("assets", path)

    if os.path.exists(full):
        return send_from_directory("assets", path)

    return Response("OK", status=200)


# =========================================================
# CATCH ALL
# =========================================================

@app.route("/<path:path>", methods=["GET", "POST", "PUT", "DELETE"])
def catch_all(path):

    scan_request("CATCH ALL")

    return jsonify({
        "status": "captured",
        "path": path,
        "method": request.method
    })


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    os.makedirs("assets", exist_ok=True)

    add_log("=" * 70)
    add_log("UNITY ADVANCED LIVE SCANNER STARTED")
    add_log(f"PORT: {PORT}")
    add_log("=" * 70)

    app.run(
        host="0.0.0.0",
        port=PORT
)
