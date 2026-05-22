from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import traceback

PORT = int(os.environ.get("PORT", 10000))

LIVE_HASH = "1000678a9449649a1748f16cc0b922eee9c83cea4f3ac6f5981211536ad9fa0db941332ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"

TARGET_PATH = f"/live/{LIVE_HASH}"

FILEINFO_DATA = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
avatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0
avatar/uma_dcs,BSJQtQt6qEeFdLv8gsrVtPDQubo=,14523,0"""

VERSION = "1.17.1"


class Handler(BaseHTTPRequestHandler):

    def write_log(self):
        print("\n========== REQUEST ==========")
        print("IP:", self.client_address[0])
        print("METHOD:", self.command)
        print("PATH:", self.path)

        print("\n--- HEADERS ---")
        for key, value in self.headers.items():
            print(f"{key}: {value}")

        print("=============================\n")

    def send_text(self, text, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(text.encode("utf-8"))

    def send_json(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))

    def do_GET(self):
        try:
            self.write_log()

            path_lower = self.path.lower()

            # LIVE HASH
            if self.path == TARGET_PATH:

                self.send_json({
                    "status": "ok",
                    "version": VERSION,
                    "message": "live endpoint working"
                })

            # VERSIONINFO
            elif "versioninfo" in path_lower:

                self.send_text(VERSION)

            # FILEINFO
            elif "fileinfo" in path_lower:

                self.send_text(FILEINFO_DATA)

            # AVATAR
            elif "/avatar/" in path_lower:

                self.send_text("avatar ok")

            # ROOT
            elif self.path == "/":

                self.send_json({
                    "server": "online",
                    "version": VERSION
                })

            # UNKNOWN
            else:

                self.send_json({
                    "unknown_path": self.path
                }, 404)

        except Exception as e:
            print(traceback.format_exc())

            self.send_json({
                "error": str(e)
            }, 500)

    def do_POST(self):
        try:
            self.write_log()

            content_length = int(
                self.headers.get("Content-Length", 0)
            )

            body = b""

            if content_length > 0:
                body = self.rfile.read(content_length)

            print("\n--- BODY ---")

            try:
                print(body.decode("utf-8"))
            except:
                print(body)

            self.send_json({
                "status": "post_received"
            })

        except Exception as e:
            print(traceback.format_exc())

            self.send_json({
                "error": str(e)
            }, 500)


server = ThreadingHTTPServer(
    ("0.0.0.0", PORT),
    Handler
)

print(f"SERVER RUNNING PORT {PORT}")

server.serve_forever()
