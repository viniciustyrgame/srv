from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os
import traceback
import json
import re
import time

PORT = int(os.environ.get("PORT", "10000"))

VERSION = "1.17.1"

FILEINFO_DATA = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
avatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0
avatar/uma_dcs,BSJQtQt6qEeFdLv8gsrVtPDQubo=,14523,0"""


class Handler(BaseHTTPRequestHandler):

    # REMOVE LOG PADRÃO
    def log_message(self, format, *args):
        return

    # PRINT REALTIME
    def log(self, *args):
        print(*args, flush=True)

    # RESPONSE TEXT
    def send_text(self, text, status=200):

        encoded = text.encode("utf-8")

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "text/plain; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(encoded))
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.end_headers()

        self.wfile.write(encoded)

    # RESPONSE JSON
    def send_json(self, data, status=200):

        encoded = json.dumps(data).encode("utf-8")

        self.send_response(status)

        self.send_header(
            "Content-Type",
            "application/json"
        )

        self.send_header(
            "Content-Length",
            str(len(encoded))
        )

        self.end_headers()

        self.wfile.write(encoded)

    # LOGGER
    def print_request(self, body=None):

        self.log("\n")
        self.log("=" * 60)
        self.log("NEW REQUEST")
        self.log("=" * 60)

        self.log("TIME:", time.strftime("%H:%M:%S"))

        self.log("IP:", self.client_address[0])

        self.log("METHOD:", self.command)

        self.log("RAW PATH:", self.path)

        # REMOVE QUERY
        raw_path = self.path.split("?")[0]

        # REMOVE //////
        clean_path = "/" + re.sub(
            r"/+",
            "/",
            raw_path
        ).lstrip("/")

        lower_path = clean_path.lower()

        self.log("CLEAN PATH:", clean_path)

        # QUERY
        if "?" in self.path:

            query = self.path.split("?", 1)[1]

            self.log("\nQUERY:")
            self.log(query)

        # HEADERS
        self.log("\nHEADERS:")

        for key, value in self.headers.items():

            self.log(f"{key}: {value}")

        # BODY
        if body:

            self.log("\nBODY:")

            try:
                self.log(body.decode("utf-8"))
            except:
                self.log(body)

        self.log("=" * 60)
        self.log("\n")

        return clean_path, lower_path

    # GET
    def do_GET(self):

        try:

            clean_path, lower_path = self.print_request()

            # =====================================================
            # VER.PHP
            # =====================================================
            if "ver.php" in lower_path:

                # IMPORTANTE:
                # UNITY ANTIGA USA CRLF (\r\n)

                response = (
                    f"{VERSION}\r\n"
                    f"/live/Versioninfo.txt\r\n"
                    f"/live/fileinfo.txt\r\n"
                    f"/live/\r\n"
                )

                self.log("VER RESPONSE:")
                self.log(repr(response))

                self.send_text(response)

                return

            # =====================================================
            # VERSIONINFO
            # =====================================================
            if "versioninfo" in lower_path:

                self.log("VERSIONINFO REQUEST")

                self.send_text(
                    VERSION + "\r\n"
                )

                return

            # =====================================================
            # FILEINFO
            # =====================================================
            if "fileinfo" in lower_path:

                self.log("FILEINFO REQUEST")

                self.send_text(
                    FILEINFO_DATA + "\r\n"
                )

                return

            # =====================================================
            # LIVE ASSETS
            # =====================================================
            if "/live/" in lower_path:

                asset_path = clean_path.replace(
                    "/live/",
                    ""
                )

                self.log("LIVE ASSET REQUEST:")
                self.log(asset_path)

                # IGNORA PHP
                if asset_path and not asset_path.endswith(".php"):

                    cdn_url = (
                        "https://freefiremobile-a.akamaihd.net/live/"
                        + asset_path
                    )

                    self.log("REDIRECT CDN:")
                    self.log(cdn_url)

                    # 301 MELHOR PRA UNITY ANTIGA
                    self.send_response(301)

                    self.send_header(
                        "Location",
                        cdn_url
                    )

                    self.end_headers()

                    return

            # =====================================================
            # ROOT
            # =====================================================
            if clean_path == "/":

                self.send_json({
                    "server": "online",
                    "version": VERSION
                })

                return

            # =====================================================
            # UNKNOWN
            # =====================================================
            self.log("UNKNOWN REQUEST")

            self.send_text("OK")

        except Exception as e:

            self.log("\n")
            self.log("=" * 60)
            self.log("ERROR")
            self.log("=" * 60)

            self.log(traceback.format_exc())

            self.send_json({
                "error": str(e)
            }, 500)

    # POST
    def do_POST(self):

        try:

            content_length = int(
                self.headers.get(
                    "Content-Length",
                    0
                )
            )

            body = b""

            if content_length > 0:

                body = self.rfile.read(
                    content_length
                )

            clean_path, lower_path = self.print_request(body)

            self.send_json({
                "status": "ok",
                "path": clean_path
            })

        except Exception as e:

            self.log(traceback.format_exc())

            self.send_response(500)

            self.end_headers()

    # HEAD
    def do_HEAD(self):

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/plain"
        )

        self.end_headers()


server = ThreadingHTTPServer(
    ("0.0.0.0", PORT),
    Handler
)

print("=" * 60, flush=True)
print(f"UNITY SCANNER SERVER RUNNING PORT {PORT}", flush=True)
print("=" * 60, flush=True)

server.serve_forever()
