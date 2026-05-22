from flask import Flask, request, Response, send_from_directory
import os
from datetime import datetime

app = Flask(__name__)

PORT = int(os.environ.get("PORT", 5000))

# =========================
# CONFIG
# =========================

CURRENT_VERSION = "9999999999"

LOGS = []

# =========================
# LOG SYSTEM
# =========================

def add_log(text):
    now = datetime.now().strftime("%H:%M:%S")
    line = f"[{now}] {text}"
    print(line)
    LOGS.insert(0, line)

    # Limite de logs
    if len(LOGS) > 500:
        LOGS.pop()


# =========================
# CREATE FILES
# =========================

os.makedirs("assets/android", exist_ok=True)

if not os.path.exists("assets/android/Versioninfo.txt"):
    with open("assets/android/Versioninfo.txt", "w") as f:
        f.write(CURRENT_VERSION)

if not os.path.exists("assets/android/Fileinfo.txt"):
    with open("assets/android/Fileinfo.txt", "w") as f:
        f.write(
            "gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0\n"
            "main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0\n"
        )

# =========================
# HOME
# =========================

@app.route("/")
def home():

    logs_html = "<br>".join(LOGS)

    return f"""
    <html>
    <head>
        <title>UNITY LIVE LOGS</title>

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
                border-radius: 10px;
                padding: 15px;
                margin-top: 20px;
                border: 1px solid #30363d;
            }}

            .online {{
                color: #00ff88;
            }}
        </style>
    </head>

    <body>

        <h1>UNITY LIVE LOGS</h1>

        <div class="box">
            <b class="online">SERVER ONLINE</b><br><br>

            HOST:<br>
            https://{request.host}<br><br>

            VERSION:<br>
            {CURRENT_VERSION}
        </div>

        <div class="box">
            {logs_html}
        </div>

    </body>
    </html>
    """


# =========================
# FAVICON
# =========================

@app.route("/favicon.ico")
def favicon():
    add_log("FAVICON REQUEST")
    return "", 204


# =========================
# VERSIONINFO
# =========================

@app.route("/Versioninfo.txt")
def versioninfo():

    add_log("VERSIONINFO REQUEST")

    return Response(
        CURRENT_VERSION,
        mimetype="text/plain"
    )


# =========================
# FILEINFO
# =========================

@app.route("/Fileinfo.txt")
def fileinfo():

    add_log("FILEINFO REQUEST")

    return send_from_directory(
        "assets/android",
        "Fileinfo.txt"
    )


# =========================
# LIVE VER.PHP
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

    for key, value in request.headers.items():
        add_log(f"{key}: {value}")

    add_log("")
    add_log("QUERY:")

    for key, value in request.args.items():
        add_log(f"{key}: {value}")

    unity = request.headers.get("X-Unity-Version", "unknown")
    ua = request.headers.get("User-Agent", "unknown")

    add_log("")
    add_log(f"UNITY: {unity}")
    add_log("")
    add_log(f"USER-AGENT: {ua}")

    host = request.host_url.rstrip("/")

    response_text = (
        f"{CURRENT_VERSION}\r\n"
        f"{host}/Versioninfo.txt\r\n"
        f"{host}/Fileinfo.txt\r\n"
        f"{host}/live/\r\n"
    )

    add_log("")
    add_log("VER RESPONSE:")
    add_log("")
    add_log(response_text)

    return Response(
        response_text,
        mimetype="text/plain"
    )


# =========================
# LIVE FILES
# =========================

@app.route("/live/<path:filename>")
def live_files(filename):

    add_log(f"LIVE FILE REQUEST: {filename}")

    full_path = os.path.join("assets/android", filename)

    if os.path.exists(full_path):
        return send_from_directory("assets/android", filename)

    return "NOT FOUND", 404


# =========================
# CATCH ALL
# =========================

@app.route("/<path:path>")
def catch_all(path):

    add_log("")
    add_log(f"UNKNOWN REQUEST: /{path}")
    add_log("")

    return Response(
        "OK",
        mimetype="text/plain"
    )


# =========================
# START
# =========================

if __name__ == "__main__":

    add_log("SERVER STARTED")

    app.run(
        host="0.0.0.0",
        port=PORT
        )
