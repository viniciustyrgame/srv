from flask import Flask, request, Response, send_file
import os
import datetime

app = Flask(__name__)

PORT = int(os.environ.get("PORT", 5000))

logs = []

def add_log(text):
    time = datetime.datetime.now().strftime("%H:%M:%S")
    full = f"[{time}] {text}"
    print(full)
    logs.insert(0, full)

VERSION = "1.17.1"

# =========================
# HOME LOG VIEWER
# =========================
@app.route("/")
def home():
    html_logs = "<br>".join(logs[:300])

    return f"""
    <html>
    <head>
        <title>Unity Log Viewer</title>
        <meta http-equiv="refresh" content="2">
        <style>
            body {{
                background:#0d1117;
                color:#00ff88;
                font-family:monospace;
                padding:20px;
            }}
            .box {{
                background:#161b22;
                padding:15px;
                border-radius:10px;
                white-space:pre-wrap;
            }}
        </style>
    </head>
    <body>
        <h2>UNITY LIVE LOGS</h2>
        <div class="box">{html_logs}</div>
    </body>
    </html>
    """

# =========================
# VER.PHP
# =========================
@app.route("/live/ver.php", methods=["GET"])
def ver_php():

    add_log("===================================")
    add_log("VER.PHP REQUEST")
    add_log(f"TIME: {datetime.datetime.now().strftime('%H:%M:%S')}")
    add_log(f"METHOD: {request.method}")
    add_log(f"RAW PATH: {request.full_path}")

    for k, v in request.args.items():
        add_log(f"{k} = {v}")

    ua = request.headers.get("User-Agent", "")
    unity = request.headers.get("X-Unity-Version", "")

    add_log(f"USER-AGENT: {ua}")
    add_log(f"UNITY: {unity}")

    host = request.host_url.rstrip("/")

    response_text = (
        f"{VERSION}\r\n"
        f"{host}/Versioninfo.txt\r\n"
        f"{host}/Fileinfo.txt\r\n"
        f"{host}/live/\r\n"
    )

    add_log("VER RESPONSE:")
    add_log(response_text)

    return Response(
        response_text,
        mimetype="text/plain"
    )

# =========================
# VERSIONINFO
# =========================
@app.route("/Versioninfo.txt")
@app.route("/live/versioninfo.txt")
@app.route("/live/Versioninfo.txt")
def versioninfo():

    add_log("VERSIONINFO REQUEST")

    content = VERSION

    return Response(
        content,
        mimetype="text/plain"
    )

# =========================
# FILEINFO
# =========================
@app.route("/Fileinfo.txt")
@app.route("/live/fileinfo.txt")
@app.route("/live/Fileinfo.txt")
def fileinfo():

    add_log("FILEINFO REQUEST")

    content = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
avatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0
avatar/uma_dcs,BSJQtQt6qEeFdLv8gsrVtPDQubo=,14523,0"""

    return Response(
        content,
        mimetype="text/plain"
    )

# =========================
# CATCH ALL
# =========================
@app.route("/<path:path>", methods=["GET", "POST"])
def catch_all(path):

    add_log("===================================")
    add_log("UNKNOWN REQUEST")
    add_log(f"PATH: /{path}")
    add_log(f"METHOD: {request.method}")

    for k, v in request.headers.items():
        add_log(f"{k}: {v}")

    return Response(
        "OK",
        status=200,
        mimetype="text/plain"
    )

# =========================
# START
# =========================
if __name__ == "__main__":

    add_log("===================================")
    add_log("UNITY SERVER STARTED")
    add_log(f"PORT: {PORT}")

    app.run(
        host="0.0.0.0",
        port=PORT
    )
