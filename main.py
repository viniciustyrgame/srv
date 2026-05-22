from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os

PORT = int(os.environ.get("PORT", 10000))

class LoggerHandler(BaseHTTPRequestHandler):

    def log_request_info(self):
        print("\n========== NOVA REQUISIÇÃO ==========")
        print("IP:", self.client_address[0])
        print("Método:", self.command)
        print("URL:", self.path)

        print("\n--- HEADERS ---")
        for key, value in self.headers.items():
            print(f"{key}: {value}")

        content_length = self.headers.get('Content-Length')

        if content_length:
            body = self.rfile.read(int(content_length))
            print("\n--- BODY ---")

            try:
                print(body.decode())
            except:
                print(body)

        print("=====================================\n")

    def send_json(self, data):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()

        self.wfile.write(json.dumps(data).encode())

    def do_GET(self):
        self.log_request_info()

        if self.path == "/Versioninfo":
            self.send_json({
                "version": "1.17.1"
            })

        elif self.path == "/fileinfo":
            self.send_json({
                "files": [
                    "gameassetbundles",
                    "main/gameentry"
                ]
            })

        else:
            self.send_json({
                "status": "ok",
                "path": self.path
            })

    def do_POST(self):
        self.log_request_info()

        self.send_json({
            "status": "POST recebido"
        })

server = HTTPServer(("0.0.0.0", PORT), LoggerHandler)

print(f"Servidor iniciado porta {PORT}")

server.serve_forever()