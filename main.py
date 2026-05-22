from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import traceback
import re
import time
import uuid

PORT = int(os.environ.get("PORT", 10000))
VERSION = "1.17.1"

FILEINFO_DATA = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
avatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0
avatar/uma_dcs,BSJQtQt6qEeFdLv8gsrVtPDQubo=,14523,0"""


class Handler(BaseHTTPRequestHandler):

    # REMOVE LOG PADRÃO DO PYTHON
    def log_message(self, format, *args):
        return

    # HEAD REQUEST
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()

    # LOG CUSTOM
    def print_request_log(self, clean_path):
        print("\n========== REQUEST ==========")
        print("IP:", self.client_address[0])
        print("METHOD:", self.command)
        print("RAW PATH:", self.path)
        print("CLEAN PATH:", clean_path)

        print("\n--- HEADERS ---")
        for key, value in self.headers.items():
            print(f"{key}: {value}")

        print("=============================\n")

    # RESPONSE TEXT
    def send_text(self, text, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(text.encode("utf-8"))

    # RESPONSE JSON
    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    # MAIN HANDLER
    def handle_request(self):

        try:

            # REMOVE QUERY PARAMS
            raw_path = self.path.split('?')[0]

            # REMOVE MULTIPLE //
            clean_path = "/" + re.sub(r'/+', '/', raw_path).lstrip('/')

            # LOWERCASE
            lower_path = clean_path.lower()

            # LOG
            self.print_request_log(clean_path)

            # =========================================
            # VER.PHP
            # =========================================
            if "ver.php" in lower_path:

                host = self.headers.get(
                    "Host",
                    "srv-mtei.onrender.com"
                )

                base_url = f"https://{host}/live/"

                response = (
                    f"{VERSION},"
                    f"{base_url},"
                    f"{base_url},"
                    f"{base_url}"
                )

                print("VER RESPONSE:", response)

                self.send_text(response)
                return

            # =========================================
            # VERSIONINFO
            # =========================================
            if "versioninfo" in lower_path:

                print("VERSIONINFO REQUEST")

                self.send_text(VERSION)
                return

            # =========================================
            # FILEINFO
            # =========================================
            if "fileinfo" in lower_path:

                print("FILEINFO REQUEST")

                self.send_text(FILEINFO_DATA)
                return

            # =========================================
            # OAUTH / LOGIN
            # =========================================
            if "/oauth/" in lower_path:

                token = str(uuid.uuid4()).replace("-", "")

                data = {
                    "access_token": token,
                    "refresh_token": token,
                    "expiry_time": int(time.time()) + 86400,
                    "open_id": "123456789",
                    "platform": 0
                }

                # INSPECT
                if "inspect" in lower_path:

                    data = {
                        "open_id": "123456789",
                        "platform": 0,
                        "expire": int(time.time()) + 86400
                    }

                print("OAUTH RESPONSE:", data)

                self.send_json(data)
                return

            # =========================================
            # LIVE ASSETS REDIRECT
            # =========================================
            if "/live/" in lower_path:

                asset_path = clean_path.replace("/live/", "")

                # IGNORA PHP
                if asset_path and not asset_path.endswith(".php"):

                    cdn_url = (
                        "https://freefiremobile-a.akamaihd.net/live/"
                        + asset_path
                    )

                    print("REDIRECT:", cdn_url)

                    self.send_response(302)
                    self.send_header("Location", cdn_url)
                    self.end_headers()
                    return

            # =========================================
            # ROOT
            # =========================================
            if clean_path == "/":

                self.send_json({
                    "server": "online",
                    "version": VERSION
                })

                return

            # =========================================
            # FALLBACK
            # =========================================
            print("UNKNOWN PATH")

            self.send_text("OK")

        except Exception as e:

            print("\n========== ERROR ==========")
            print(traceback.format_exc())
            print("===========================\n")

            self.send_json({
                "error": str(e)
            }, 500)

    # GET
    def do_GET(self):
        self.handle_request()

    # POST
    def do_POST(self):

        try:

            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            if content_length > 0:

                body = self.rfile.read(content_length)

                print("\n========== POST BODY ==========")

                try:
                    print(body.decode("utf-8"))
                except:
                    print(body)

                print("================================\n")

        except:
            pass

        self.handle_request()


server = ThreadingHTTPServer(
    ("0.0.0.0", PORT),
    Handler
)

print(f"SERVER UNIVERSAL RUNNING ON PORT {PORT}")

server.serve_forever()
