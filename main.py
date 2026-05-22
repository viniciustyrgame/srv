from flask import Flask, send_from_directory, request, Response, render_template_string
import os
from datetime import datetime

app = Flask(__name__)

PORT = int(os.environ.get("PORT", "5000"))

# =========================
# CONFIG
# =========================

VERSION = "1.17.2"

logs = []

def add_log(text):
    now = datetime.now().strftime("%H:%M:%S")
    logs.insert(0, f"[{now}] {text}")

    # Limite de logs
    if len(logs) > 500:
        logs.pop()

# =========================
# HOME / LOG VIEWER
# =========================

@app.route("/")
def home():
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Unity Mini Server</title>

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
                padding: 10px;
                border-radius: 10px;
                margin-bottom: 15px;
            }}

            .log {{
                white-space: pre-wrap;
                word-wrap: break-word;
                font-size: 14px;
                border-bottom: 1px solid #222;
                padding: 4px;
            }}

            .top {{
                color: cyan;
            }}

            .red {{
                color: #ff5555;
            }}

            .yellow {{
                color: #ffd866;
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

            URL:
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

# =========================
# VER.PHP
# =========================

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
    add_log(f"Host: {request.headers.get('Host')}")
    add_log(f"User-Agent: {request.headers.get('User-Agent')}")
    add_log(f"Accept-Encoding: {request.headers.get('Accept-Encoding')}")
    add_log(f"Cdn-Loop: {request.headers.get('Cdn-Loop')}")
    add_log(f"Cf-Connecting-Ip: {request.headers.get('Cf-Connecting-Ip')}")
    add_log(f"Cf-Ipcountry: {request.headers.get('Cf-Ipcountry')}")
    add_log(f"Cf-Ray: {request.headers.get('Cf-Ray')}")
    add_log(f"Cf-Visitor: {request.headers.get('Cf-Visitor')}")
    add_log(f"Render-Proxy-Ttl: {request.headers.get('Render-Proxy-Ttl')}")
    add_log(f"Rndr-Id: {request.headers.get('Rndr-Id')}")
    add_log(f"True-Client-Ip: {request.headers.get('True-Client-Ip')}")
    add_log(f"X-Forwarded-For: {request.headers.get('X-Forwarded-For')}")
    add_log(f"X-Forwarded-Proto: {request.headers.get('X-Forwarded-Proto')}")
    add_log(f"X-Request-Start: {request.headers.get('X-Request-Start')}")
    add_log(f"X-Unity-Version: {request.headers.get('X-Unity-Version')}")

    add_log("")
    add_log("QUERY:")
    add_log("")

    for k, v in request.args.items():
        add_log(f"{k} {v}")

    add_log("")
    add_log(f"USER-AGENT: {request.headers.get('User-Agent')}")
    add_log("")
    add_log(f"UNITY: {request.headers.get('X-Unity-Version')}")
    add_log("")

    # =========================
    # RESPONSE FORMAT
    # =========================

    response_text = (
        f"{VERSION}\r\n"
        f"https://{request.host}/Versioninfo.txt\r\n"
        f"https://{request.host}/Fileinfo.txt\r\n"
        f"https://{request.host}/live/\r\n"
    )

    add_log("VER RESPONSE:")
    add_log("")
    add_log(response_text)

    return Response(response_text, mimetype="text/plain")

# =========================
# VERSIONINFO
# =========================

@app.route("/Versioninfo.txt")
def versioninfo():

    add_log("")
    add_log("VERSIONINFO REQUEST")
    add_log(f"IP: {request.headers.get('Cf-Connecting-Ip')}")

    text = f"{VERSION}"

    return Response(text, mimetype="text/plain")

# =========================
# FILEINFO
# =========================

@app.route("/Fileinfo.txt")
def fileinfo():

    add_log("")
    add_log("FILEINFO REQUEST")
    add_log(f"IP: {request.headers.get('Cf-Connecting-Ip')}")

    data = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0"""

    return Response(data, mimetype="text/plain")

# =========================
# LIVE FILES
# =========================

@app.route("/live/<path:path>")
def live_files(path):

    add_log("")
    add_log("LIVE FILE REQUEST")
    add_log(f"PATH: /live/{path}")

    full = os.path.join("assets", path)

    if os.path.exists(full):
        return send_from_directory("assets", path)

    add_log("FILE NOT FOUND")

    return Response("NOT FOUND", status=404)

# =========================
# FAVICON
# =========================

@app.route("/favicon.ico")
def favicon():

    add_log("")
    add_log("UNKNOWN REQUEST")
    add_log("")
    add_log(f"METHOD: {request.method}")
    add_log(f"PATH: /favicon.ico")
    add_log(f"Host: {request.headers.get('Host')}")
    add_log(f"User-Agent: {request.headers.get('User-Agent')}")

    return Response("", status=204)

# =========================
# CATCH ALL
# =========================

@app.route("/<path:path>", methods=["GET", "POST"])
def catch_all(path):

    add_log("")
    add_log("UNKNOWN REQUEST")
    add_log("")
    add_log(f"METHOD: {request.method}")
    add_log(f"PATH: /{path}")

    return Response("OK", status=200)

# =========================
# START
# =========================

if __name__ == "__main__":

    os.makedirs("assets", exist_ok=True)

    add_log("SERVER STARTED")
    add_log(f"PORT {PORT}")

    app.run(host="0.0.0.0", port=PORT)
