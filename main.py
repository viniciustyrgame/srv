from flask import Flask, request, send_from_directory, Response
from datetime import datetime
import os

app = Flask(__name__)

# =========================================
# CONFIG
# =========================================

BASE_DIR = "assets/android"

SERVER_HOST = "https://srv-mtei.onrender.com"
SERVER_VERSION = "9999999999"

logs = []


# =========================================
# LOG SYSTEM
# =========================================

def add_log(text):
    now = datetime.now().strftime("%H:%M:%S")
    line = f"[{now}] {text}"
    print(line)

    logs.insert(0, line)

    if len(logs) > 500:
        logs.pop()


# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():
    html_logs = "<br>".join(logs)

    return f"""
    <html>
    <head>
        <title>UNITY LIVE LOGS</title>

        <meta name="viewport" content="width=device-width, initial-scale=1">

        <style>
            body {{
                background: #0d1117;
                color: #00ff88;
                font-family: monospace;
                padding: 15px;
            }}

            h1 {{
                color: white;
            }}

            .box {{
                background: #161b22;
                border-radius: 10px;
                padding: 15px;
                margin-bottom: 20px;
            }}

            .log {{
                white-space: pre-wrap;
                word-wrap: break-word;
                font-size: 14px;
            }}
        </style>
    </head>

    <body>

        <div class="box">
            <h1>UNITY LIVE LOGS</h1>

            <b>SERVER ONLINE</b><br><br>

            <b>HOST:</b><br>
            {SERVER_HOST}<br><br>

            <b>VERSION:</b><br>
            {SERVER_VERSION}
        </div>

        <div class="box log">
            {html_logs}
        </div>

    </body>
    </html>
    """


# =========================================
# FAVICON
# =========================================

@app.route("/favicon.ico")
def favicon():
    add_log("FAVICON REQUEST")
    return Response(status=204)


# =========================================
# VERSIONINFO
# =========================================

@app.route("/Versioninfo.txt")
def versioninfo():
    add_log("Versioninfo.txt REQUEST")
    return send_from_directory(BASE_DIR, "Versioninfo.txt")


# =========================================
# FILEINFO
# =========================================

@app.route("/Fileinfo.txt")
def fileinfo():
    add_log("Fileinfo.txt REQUEST")
    return send_from_directory(BASE_DIR, "Fileinfo.txt")


# =========================================
# VER.PHP
# =========================================

@app.route("/live/ver.php")
def ver_php():

    version = request.args.get("version", "unknown")
    lang = request.args.get("lang", "unknown")
    device = request.args.get("device", "unknown")
    appstore = request.args.get("appstore", "unknown")

    add_log("")
    add_log("VER.PHP REQUEST")
    add_log("")
    add_log(f"TIME: {datetime.now().strftime('%H:%M:%S')}")
    add_log(f"METHOD: {request.method}")
    add_log("")
    add_log(f"RAW PATH: {request.full_path}")
    add_log("")
    add_log("HEADERS:")

    for key, value in request.headers.items():
        add_log(f"{key}: {value}")

    add_log("")
    add_log("QUERY:")
    add_log("")
    add_log(f"version: {version}")
    add_log(f"lang: {lang}")
    add_log(f"device: {device}")
    add_log(f"appstore: {appstore}")
    add_log("")

    response_text = (
        f"{SERVER_VERSION}\r\n"
        f"{SERVER_HOST}/Versioninfo.txt\r\n"
        f"{SERVER_HOST}/Fileinfo.txt\r\n"
        f"{SERVER_HOST}/live/\r\n"
    )

    add_log("VER RESPONSE:")
    add_log("")
    add_log(response_text)

    return Response(response_text, mimetype="text/plain")


# =========================================
# LIVE FILES
# =========================================

@app.route("/live/<path:filename>")
def live_files(filename):

    full_path = os.path.join(BASE_DIR, "live", filename)

    add_log("")
    add_log("LIVE FILE REQUEST")
    add_log(f"FILE: {filename}")

    if os.path.exists(full_path):
        add_log("STATUS: FOUND")
        return send_from_directory(
            os.path.join(BASE_DIR, "live"),
            filename
        )

    add_log("STATUS: NOT FOUND")
    return "FILE NOT FOUND", 404


# =========================================
# UNKNOWN ROUTES
# =========================================

@app.errorhandler(404)
def not_found(e):

    add_log("")
    add_log("UNKNOWN REQUEST")
    add_log(f"PATH: {request.path}")
    add_log(f"METHOD: {request.method}")

    return "404", 404


# =========================================
# START
# =========================================

if __name__ == "__main__":

    add_log("SERVER STARTED")

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
