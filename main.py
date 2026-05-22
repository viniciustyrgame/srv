from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os
import traceback
import json
import re
import time

PORT = int(os.environ.get("PORT", 10000))


class Handler(BaseHTTPRequestHandler):

    # REMOVE LOG PADRÃO
    def log_message(self, format, *args):
        return

    # RESPONSE
    def send_ok(self, text="OK"):

        self.send_response(200)

        self.send_header(
            "Content-Type",
            "text/plain; charset=utf-8"
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.end_headers()

        self.wfile.write(
            text.encode("utf-8")
        )

    # LOGGER
    def print_request(self, body=None):

        print("\n")
        print("=" * 60)
        print("NEW REQUEST")
        print("=" * 60)

        print("TIME:", time.strftime("%H:%M:%S"))

        print("IP:", self.client_address[0])

        print("METHOD:", self.command)

        print("RAW PATH:", self.path)

        # PATH LIMPO
        raw_path = self.path.split("?")[0]

        clean_path = "/" + re.sub(
            r"/+",
            "/",
            raw_path
        ).lstrip("/")

        print("CLEAN PATH:", clean_path)

        # QUERY
        if "?" in self.path:

            query = self.path.split("?", 1)[1]

            print("\nQUERY:")
            print(query)

        # HEADERS
        print("\nHEADERS:")

        for key, value in self.headers.items():

            print(f"{key}: {value}")

        # BODY
        if body:

            print("\nBODY:")

            try:
                print(body.decode("utf-8"))
            except:
                print(body)

        print("=" * 60)
        print("\n")

    # GET
    def do_GET(self):

        try:

            self.print_request()

            # RESPONDE 200 PRA TUDO
            self.send_ok("OK")

        except Exception as e:

            print(traceback.format_exc())

            self.send_response(500)
            self.end_headers()

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

            self.print_request(body)

            # JSON GENÉRICO
            response = {
                "status": "ok",
                "message": "request received"
            }

            self.send_response(200)

            self.send_header(
                "Content-Type",
                "application/json"
            )

            self.end_headers()

            self.wfile.write(
                json.dumps(response).encode()
            )

        except Exception as e:

            print(traceback.format_exc())

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

print("=" * 60)
print(f"SCANNER SERVER RUNNING PORT {PORT}")
print("=" * 60)

server.serve_forever()
