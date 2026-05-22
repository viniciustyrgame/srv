from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

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

class Handler(BaseHTTPRequestHandler):

    def log_request(self):
        print("\n========== REQUEST ==========")
        print("IP:", self.client_address[0])
        print("METHOD:", self.command)
        print("PATH:", self.path)

        print("\n--- HEADERS ---")
        for key, value in self.headers.items():
            print(f"{key}: {value}")

        print("=============================\n")

    def send_text(self, text):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()
        self.wfile.write(text.encode())

    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        self.log_request()

        # LIVE HASH
        if self.path == TARGET_PATH:

            self.send_json({
                "status": "ok",
                "version": "1.17.1",
                "next": "/Versioninfo"
            })

        # VERSIONINFO
        elif "Versioninfo" in self.path:

            self.send_text("1.17.1")

        # FILEINFO
        elif "fileinfo" in self.path:

            self.send_text(FILEINFO_DATA)

        # AVATAR TEST
        elif "/Avatar/" in self.path:

            self.send_text("avatar ok")

        # DEFAULT
        else:

            self.send_json({
                "unknown_path": self.path
            })

    def do_POST(self):
        self.log_request()

        content_length = self.headers.get('Content-Length')

        body = b''

        if content_length:
            body = self.rfile.read(int(content_length))

        print("\n--- BODY ---")

        try:
            print(body.decode())
        except:
            print(body)

        self.send_json({
            "status": "post_received"
        })

server = HTTPServer(("0.0.0.0", PORT), Handler)

print(f"SERVER RUNNING PORT {PORT}")

server.serve_forever()
