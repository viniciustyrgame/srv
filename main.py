from flask import Flask, request, send_from_directory, Response
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "android")

# ---------------------------
# LOGS
# ---------------------------
def log(msg):
    print(msg)

# ---------------------------
# VERSION CHECK
# ---------------------------
@app.route("/live/ver.php")
def version():
    version = request.args.get("version", "")
    lang = request.args.get("lang", "")
    device = request.args.get("device", "")
    appstore = request.args.get("appstore", "")

    log(f"VER REQUEST -> {version} {lang} {device} {appstore}")

    version_file = os.path.join(ASSETS_DIR, "Versioninfo.txt")

    if os.path.exists(version_file):
        with open(version_file, "r") as f:
            version_value = f.read().strip()
    else:
        version_value = "1.17.1"

    response = f"{version_value}"

    log(f"VER RESPONSE SENT OK -> {response}")
    return Response(response, mimetype="text/plain")


# ---------------------------
# FILEINFO
# ---------------------------
@app.route("/Fileinfo.txt")
def fileinfo():
    path = os.path.join(ASSETS_DIR, "Fileinfo.txt")
    return send_from_directory(os.path.dirname(path), os.path.basename(path), mimetype="text/plain")


# ---------------------------
# VERSIONINFO
# ---------------------------
@app.route("/Versioninfo.txt")
def versioninfo():
    path = os.path.join(ASSETS_DIR, "Versioninfo.txt")
    return send_from_directory(os.path.dirname(path), os.path.basename(path), mimetype="text/plain")


# ---------------------------
# LIVE FILES (IMPORTANT PART)
# ---------------------------
@app.route("/live/<path:file_path>")
def live_files(file_path):

    full_path = os.path.join(ASSETS_DIR, "live", file_path)

    log(f"LIVE REQUEST -> {file_path}")

    if not os.path.exists(full_path):
        log("FILE NOT FOUND")
        return "NOT FOUND", 404

    # Unity files must NOT be modified
    return send_from_directory(
        os.path.dirname(full_path),
        os.path.basename(full_path),
        conditional=True
    )


# ---------------------------
# ROOT DEBUG
# ---------------------------
@app.route("/")
def home():
    return "SERVER ONLINE"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
