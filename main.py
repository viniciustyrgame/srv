from flask import Flask, send_from_directory, request, jsonify, Response
import os
import logging
from datetime import datetime

app = Flask(__name__)

PORT = int(os.environ.get("PORT", "5000"))

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

BASE_URL = "https://srv-mtei.onrender.com"

# =========================================================
# LOG COMPLETO
# =========================================================

def scan_request(name):
    print("\n")
    print("=" * 70)
    print("UNITY REQUEST SCAN")
    print("=" * 70)

    print(f"TIME: {datetime.now().strftime('%H:%M:%S')}")
    print(f"METHOD: {request.method}")
    print(f"RAW PATH: {request.full_path}")
    print(f"CLEAN PATH: {request.path}")

    print("\nHEADERS:")
    for k, v in request.headers.items():
        print(f"{k}: {v}")

    print("\nQUERY:")
    for k, v in request.args.items():
        print(f"{k}={v}")

    body = request.get_data()

    if body:
        try:
            print("\nBODY:")
            print(body.decode())
        except:
            print("\nBODY: <binary>")

    print("=" * 70)
    print("\n")


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():
    scan_request("HOME")
    return "UNITY SCANNER ONLINE", 200


# =========================================================
# VER.PHP
# =========================================================

@app.route("/live/ver.php", methods=["GET", "POST"])
def ver_php():
    scan_request("VER")

    response_text = (
        "1.17.1\r\n"
        f"{BASE_URL}/Versioninfo.txt\r\n"
        f"{BASE_URL}/Fileinfo.txt\r\n"
        f"{BASE_URL}/live/\r\n"
    )

    print("VER RESPONSE:")
    print(repr(response_text))

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
# TODAS ROTAS FILEINFO
# =========================================================

@app.route("/Fileinfo")
@app.route("/fileinfo")
@app.route("/Fileinfo.txt")
@app.route("/fileinfo.txt")
@app.route("/live/Fileinfo")
@app.route("/live/fileinfo")
@app.route("/live/fileinfo.txt")
@app.route("/live/Fileinfo.txt")
def fileinfo():
    scan_request("FILEINFO")

    return Response(
        FILEINFO_CONTENT,
        mimetype="text/plain"
    )


# =========================================================
# TODAS ROTAS VERSIONINFO
# =========================================================

@app.route("/Versioninfo")
@app.route("/versioninfo")
@app.route("/Versioninfo.txt")
@app.route("/versioninfo.txt")
@app.route("/live/Versioninfo")
@app.route("/live/versioninfo")
@app.route("/live/versioninfo.txt")
@app.route("/live/Versioninfo.txt")
def versioninfo():
    scan_request("VERSIONINFO")

    return Response(
        VERSIONINFO_CONTENT,
        mimetype="text/plain"
    )


# =========================================================
# CONNECT LOGIN
# =========================================================

@app.route("/app/info/get")
def app_info():
    scan_request("APP INFO")

    return jsonify({
        "success": True,
        "app_id": "100067",
        "client_version": "2018120316",
        "status": "ok"
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
        "path": path,
        "method": request.method,
        "status": "captured"
    })


# =========================================================
# START
# =========================================================

if __name__ == "__main__":

    os.makedirs("assets", exist_ok=True)

    print("=" * 70)
    print("UNITY ADVANCED SCANNER STARTED")
    print(f"PORT: {PORT}")
    print("=" * 70)

    app.run(
        host="0.0.0.0",
        port=PORT
)
