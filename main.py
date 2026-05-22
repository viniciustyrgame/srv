from flask import Flask, request, Response
import os
import datetime

app = Flask(__name__)

PORT = int(os.environ.get("PORT", 5000))

VERSION = "1.17.1"

logs = []

# =========================================================
# LOG SYSTEM
# =========================================================
def add_log(text):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    line = f"[{now}] {text}"

    print(line)

    logs.insert(0, line)

    if len(logs) > 500:
        logs.pop()

# =========================================================
# HOME LOG VIEWER
# =========================================================
@app.route("/")
def home():

    html_logs = "<br>".join(logs)

    return f"""
    <html>
    <head>
        <title>Unity Live Logs</title>

        <meta http-equiv="refresh" content="2">

        <style>
            body {{
                background: #0d1117;
                color: #00ff88;
                font-family: monospace;
                padding: 15px;
            }}

            .box {{
                background: #161b22;
                border-radius: 10px;
                padding: 15px;
                white-space: pre-wrap;
                font-size: 13px;
                line-height: 1.5;
            }}

            h1 {{
                color: white;
            }}
        </style>
    </head>

    <body>

        <h1>UNITY LIVE LOGS</h1>

        <div class="box">
            {html_logs}
        </div>

    </body>
    </html>
    """

# =========================================================
# VER.PHP
# =========================================================
@app.route("/live/ver.php", methods=["GET", "POST", "HEAD"])
def ver_php():

    add_log("=================================================")
    add_log("VER.PHP REQUEST")
    add_log(f"TIME: {datetime.datetime.now().strftime('%H:%M:%S')}")
    add_log(f"METHOD: {request.method}")
    add_log(f"RAW PATH: {request.full_path}")

    add_log("")

    add_log("HEADERS:")

    for k, v in request.headers.items():
        add_log(f"{k}: {v}")

    add_log("")

    add_log("QUERY:")

    for k, v in request.args.items():
        add_log(f"{k} = {v}")

    add_log("")

    ua = request.headers.get("User-Agent", "")
    unity = request.headers.get("X-Unity-Version", "")

    add_log(f"USER-AGENT: {ua}")
    add_log(f"UNITY: {unity}")

    host = request.host_url.rstrip("/")

    # =====================================================
    # UNITY RESPONSE FORMAT
    # =====================================================
    response_text = (
        f"{VERSION}\r\n"
        f"{host}/Versioninfo.txt\r\n"
        f"{host}/Fileinfo.txt\r\n"
        f"{host}/live/\r\n"
    )

    add_log("")
    add_log("VER RESPONSE:")
    add_log(response_text)

    response = Response(
        response_text,
        status=200,
        mimetype="text/plain"
    )

    response.headers["Connection"] = "keep-alive"
    response.headers["Accept-Ranges"] = "bytes"
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Server"] = "nginx"

    return response

# =========================================================
# VERSIONINFO
# =========================================================
@app.route("/Versioninfo.txt")
@app.route("/versioninfo.txt")
@app.route("/live/Versioninfo.txt")
@app.route("/live/versioninfo.txt")
def versioninfo():

    add_log("=================================================")
    add_log("VERSIONINFO REQUEST")

    content = f"{VERSION}\n"

    response = Response(
        content,
        status=200,
        mimetype="text/plain"
    )

    response.headers["Content-Type"] = "text/plain"
    response.headers["Accept-Ranges"] = "bytes"
    response.headers["Connection"] = "keep-alive"

    return response

# =========================================================
# FILEINFO
# =========================================================
@app.route("/Fileinfo.txt")
@app.route("/fileinfo.txt")
@app.route("/live/Fileinfo.txt")
@app.route("/live/fileinfo.txt")
def fileinfo():

    add_log("=================================================")
    add_log("FILEINFO REQUEST")

    content = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
avatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0
avatar/uma_dcs,BSJQtQt6qEeFdLv8gsrVtPDQubo=,14523,0"""

    response = Response(
        content,
        status=200,
        mimetype="text/plain"
    )

    response.headers["Content-Type"] = "text/plain"
    response.headers["Accept-Ranges"] = "bytes"
    response.headers["Connection"] = "keep-alive"

    return response

# =========================================================
# CATCH ALL
# =========================================================
@app.route("/<path:path>", methods=["GET", "POST", "HEAD"])
def catch_all(path):

    add_log("=================================================")
    add_log("UNKNOWN REQUEST")
    add_log(f"PATH: /{path}")
    add_log(f"METHOD: {request.method}")

    add_log("")

    add_log("HEADERS:")

    for k, v in request.headers.items():
        add_log(f"{k}: {v}")

    clean = path.lower()

    # =============================================
    # AUTO REDIRECTS
    # =============================================
    if clean == "fileinfo.txt":
        return fileinfo()

    if clean == "versioninfo.txt":
        return versioninfo()

    if clean.startswith("live/"):
        add_log("LIVE PATH DETECTED")

    # =============================================
    # GENERIC RESPONSE
    # =============================================
    response = Response(
        "OK",
        status=200,
        mimetype="text/plain"
    )

    response.headers["Accept-Ranges"] = "bytes"
    response.headers["Connection"] = "keep-alive"
    response.headers["Cache-Control"] = "no-cache"

    return response

# =========================================================
# START SERVER
# =========================================================
if __name__ == "__main__":

    add_log("=================================================")
    add_log("UNITY ADVANCED SERVER STARTED")
    add_log(f"PORT: {PORT}")
    add_log("READY")

    app.run(
        host="0.0.0.0",
        port=PORT
    )
