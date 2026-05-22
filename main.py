from flask import Flask, request, Response, render_template_string, send_from_directory
from datetime import datetime
import json
import os

app = Flask(__name__)

PORT = int(os.environ.get("PORT", "5000"))

# =========================================
# CONFIG
# =========================================

VERSION = "9999999999"

logs = []

# =========================================
# LOG SYSTEM
# =========================================

def add_log(text=""):
    now = datetime.now().strftime("%H:%M:%S")
    logs.insert(0, f"[{now}] {text}")

    if len(logs) > 1500:
        logs.pop()

# =========================================
# HOME
# =========================================

@app.route("/")
def home():

    html = f"""
    <!DOCTYPE html>
    <html>

    <head>

        <title>Unity Update Server</title>

        <meta http-equiv="refresh" content="2">

        <style>

            body {{
                background: #0f1117;
                color: #00ff88;
                font-family: monospace;
                padding: 15px;
            }}

            h1 {{
                color: white;
            }}

            .box {{
                background: #161b22;
                border: 1px solid #30363d;
                padding: 15px;
                border-radius: 10px;
                margin-bottom: 15px;
            }}

            .log {{
                border-bottom: 1px solid #222;
                padding: 4px;
                white-space: pre-wrap;
                word-wrap: break-word;
            }}

            .top {{
                color: cyan;
            }}

        </style>

    </head>

    <body>

        <h1>UNITY LIVE LOGS</h1>

        <div class="box">

            <div class="top">
                SERVER ONLINE
            </div>

            <br>

            HOST:
            <br>

            https://{request.host}

            <br><br>

            VERSION:
            <br>

            {VERSION}

        </div>

        <div class="box">
            {"".join([f'<div class="log">{x}</div>' for x in logs])}
        </div>

    </body>
    </html>
    """

    return render_template_string(html)

# =========================================
# VER.PHP
# =========================================

@app.route("/live/ver.php", methods=["GET"])
def ver_php():

    add_log("")
    add_log("VER.PHP REQUEST")
    add_log("")

    add_log(f"TIME: {datetime.now().strftime('%H:%M:%S')}")
    add_log(f"METHOD: {request.method}")

    add_log("")
    add_log(f"RAW PATH: {request.full_path}")

    add_log("")
    add_log("HEADERS:")

    for k, v in request.headers.items():
        add_log(f"{k}: {v}")

    add_log("")
    add_log("QUERY:")

    for k, v in request.args.items():
        add_log(f"{k}: {v}")

    add_log("")
    add_log(f"USER-AGENT: {request.headers.get('User-Agent')}")

    add_log("")
    add_log(f"UNITY: {request.headers.get('X-Unity-Version')}")

    # =========================================
    # RESPONSE
    # =========================================

    response_text = (
        f"{VERSION}\r\n"
        f"https://{request.host}/Versioninfo.txt\r\n"
        f"https://{request.host}/Fileinfo.txt\r\n"
        f"https://{request.host}/live/\r\n"
    )

    add_log("")
    add_log("VER RESPONSE:")
    add_log("")
    add_log(response_text)

    return Response(
        response_text,
        mimetype="text/plain"
    )

# =========================================
# APP INFO GET
# =========================================

@app.route("/app/info/get", methods=["GET"])
def app_info():

    add_log("")
    add_log("APP INFO REQUEST")
    add_log("")

    add_log(f"TIME: {datetime.now().strftime('%H:%M:%S')}")
    add_log(f"METHOD: {request.method}")

    add_log("")
    add_log(f"RAW PATH: {request.full_path}")

    add_log("")
    add_log("HEADERS:")

    for k, v in request.headers.items():
        add_log(f"{k}: {v}")

    add_log("")
    add_log("QUERY:")

    for k, v in request.args.items():
        add_log(f"{k}: {v}")

    response = {
        "success": True,
        "app_id": "100067",
        "version": VERSION,
        "client_version": VERSION,
        "force_update": True,
        "update": True,
        "update_url": f"https://{request.host}/live/",
        "fileinfo": f"https://{request.host}/Fileinfo.txt",
        "versioninfo": f"https://{request.host}/Versioninfo.txt"
    }

    json_text = json.dumps(response)

    add_log("")
    add_log("APP INFO RESPONSE:")
    add_log("")
    add_log(json_text)

    return Response(
        json_text,
        mimetype="application/json"
    )

# =========================================
# VERSIONINFO
# =========================================

@app.route("/Versioninfo.txt", methods=["GET"])
def versioninfo():

    add_log("")
    add_log("VERSIONINFO REQUEST")
    add_log("")

    add_log(f"METHOD: {request.method}")
    add_log(f"IP: {request.headers.get('Cf-Connecting-Ip')}")

    text = VERSION

    add_log("")
    add_log("VERSIONINFO RESPONSE:")
    add_log("")
    add_log(text)

    return Response(
        text,
        mimetype="text/plain"
    )

# =========================================
# FILEINFO
# =========================================

@app.route("/Fileinfo.txt", methods=["GET"])
def fileinfo():

    add_log("")
    add_log("FILEINFO REQUEST")
    add_log("")

    add_log(f"METHOD: {request.method}")
    add_log(f"IP: {request.headers.get('Cf-Connecting-Ip')}")

    fileinfo_data = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
avatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0"""

    add_log("")
    add_log("FILEINFO RESPONSE:")
    add_log("")
    add_log(fileinfo_data)

    return Response(
        fileinfo_data,
        mimetype="text/plain"
    )

# =========================================
# LIVE FILES
# =========================================

@app.route("/live/<path:path>", methods=["GET"])
def live_files(path):

    add_log("")
    add_log("LIVE FILE REQUEST")
    add_log("")

    add_log(f"PATH: /live/{path}")

    full_path = os.path.join("assets", path)

    if os.path.exists(full_path):

        add_log("FILE FOUND")

        return send_from_directory("assets", path)

    add_log("FILE NOT FOUND")

    return Response(
        "NOT FOUND",
        status=404
    )

# =========================================
# FAVICON
# =========================================

@app.route("/favicon.ico")
def favicon():

    add_log("")
    add_log("FAVICON REQUEST")

    return Response(
        "",
        status=204
    )

# =========================================
# CATCH ALL
# =========================================

@app.route("/<path:path>", methods=["GET", "POST"])
def catch_all(path):

    add_log("")
    add_log("UNKNOWN REQUEST")
    add_log("")

    add_log(f"METHOD: {request.method}")
    add_log(f"PATH: /{path}")

    add_log("")
    add_log("HEADERS:")

    for k, v in request.headers.items():
        add_log(f"{k}: {v}")

    return Response(
        "OK",
        status=200
    )

# =========================================
# START
# =========================================

if __name__ == "__main__":

    os.makedirs("assets", exist_ok=True)

    add_log("SERVER STARTED")
    add_log(f"PORT: {PORT}")
    add_log(f"VERSION: {VERSION}")

    app.run(
        host="0.0.0.0",
        port=PORT
)
