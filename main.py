from flask import Flask, send_from_directory, request, Response, abort
import os

app = Flask(__name__)

BASE_DIR = os.path.join(os.path.dirname(__file__), "assets", "android")

# -----------------------------
# VERSION INFO
# -----------------------------
@app.route("/Versioninfo.txt")
def version_info():
    file_path = os.path.join(BASE_DIR, "Versioninfo.txt")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return Response(f.read(), mimetype="text/plain")
    return "1.17.1", 200


# -----------------------------
# FILE INFO
# -----------------------------
@app.route("/Fileinfo.txt")
def file_info():
    file_path = os.path.join(BASE_DIR, "Fileinfo.txt")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return Response(f.read(), mimetype="text/plain")
    return "", 404


# -----------------------------
# LIVE FILES (CORE DO SISTEMA)
# -----------------------------
@app.route("/live/<path:filepath>")
def live_files(filepath):
    full_path = os.path.join(BASE_DIR, "live", filepath)

    if not os.path.exists(full_path):
        print(f"[MISS] {filepath}")
        return abort(404)

    print(f"[OK] SERVING: {filepath}")

    return send_from_directory(
        os.path.dirname(full_path),
        os.path.basename(full_path),
        conditional=True
    )


# -----------------------------
# ROOT (TEST)
# -----------------------------
@app.route("/")
def home():
    return "SERVER ONLINE", 200


# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
