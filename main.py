from flask import Flask, request, Response
import time
import os

app = Flask(__name__)

# =========================
# CONFIG
# =========================

VERSION = "1.17.1"

BASE_URL = "https://srv-mtei.onrender.com"

ASSET_PATH = "assets/android"

# =========================
# LOG SYSTEM
# =========================

logs = []

def log(msg):
    ts = time.strftime("%H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    logs.append(line)

    if len(logs) > 400:
        logs.pop(0)

# =========================
# SAFE QUERY PARSER
# =========================

def fix_args(args):
    clean = {}
    for k, v in args.items():
        k = k.replace("-", "")
        clean[k] = v
    return clean

# =========================
# LOAD FILES (GITHUB STYLE)
# =========================

def load_file(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return ""

# =========================
# ROUTES
# =========================

@app.route("/")
def home():
    return "<pre>" + "\n".join(logs[-200:]) + "</pre>"

# =========================
# VERSION CHECK (UNITY)
# =========================

@app.route("/live/ver.php")
def ver():
    args = fix_args(request.args)

    version = args.get("version", "")
    lang = args.get("lang", "")
    device = args.get("device", "")
    appstore = args.get("appstore", "")

    log("VER.PHP REQUEST")
    log(f"version={version} lang={lang} device={device} appstore={appstore}")

    # headers (debug)
    for k, v in request.headers.items():
        log(f"{k}: {v}")

    # IMPORTANTE: resposta correta do updater
    response = f"""{VERSION}
{BASE_URL}/Versioninfo.txt
{BASE_URL}/Fileinfo.txt
{BASE_URL}/live/"""

    log("VER RESPONSE SENT OK")

    return Response(response, mimetype="text/plain")


# =========================
# FILEINFO
# =========================

@app.route("/Fileinfo.txt")
def fileinfo():
    log("Fileinfo.txt REQUEST")

    data = load_file(f"{ASSET_PATH}/Fileinfo.txt")

    return Response(data, mimetype="text/plain")


# =========================
# VERSIONINFO
# =========================

@app.route("/Versioninfo.txt")
def versioninfo():
    log("Versioninfo.txt REQUEST")

    data = load_file(f"{ASSET_PATH}/Versioninfo.txt")

    return Response(data, mimetype="text/plain")


# =========================
# LIVE CDN FILES
# =========================

@app.route("/live/<path:path>")
def live(path):
    log(f"LIVE REQUEST: {path}")

    file_path = os.path.join(ASSET_PATH, "live", path)

    if os.path.isfile(file_path):
        with open(file_path, "rb") as f:
            return Response(f.read())

    return Response("NOT FOUND", status=404)


# =========================
# FAVICON (STOP SPAM LOG)
# =========================

@app.route("/favicon.ico")
def favicon():
    log("FAVICON REQUEST (ignored)")
    return ("", 204)


# =========================
# START
# =========================

if __name__ == "__main__":
    log("SERVER STARTED")
    app.run(host="0.0.0.0", port=5000)
