from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import os
import traceback
import json
import re
import time
import sys

PORT = int(os.environ.get("PORT", 10000))


class Handler(BaseHTTPRequestHandler):

    # REMOVE LOG PADRÃO
    def log_message(self, format, *args):
        return

    # PRINT REALTIME
    def log(self, *args):
        print(*args, flush=True)

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

        self.log("\n")
        self.log("=" * 60)
        self.log("NEW REQUEST")
        self.log("=" * 60)

        self.log("TIME:", time.strftime("%H:%M:%S"))

        self.log("IP:", self.client_address[0])

        self.log("METHOD:", self.command)

        self.log("RAW PATH:", self.path)

        # CLEAN PATH
        raw_path = self.path.split("?")[0]

        clean_path = "/" + re.sub(
            r"/+",
            "/",
            raw_path
        ).lstrip("/")

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

    # GET
    def do_GET(self):

        try:

            self.print_request()

            self.send_ok("OK")

        except Exception as e:

            self.log(traceback.format_exc())

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

            response = {
                "status": "ok"
            }

            self
