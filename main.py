from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import traceback
import re

PORT = int(os.environ.get("PORT", 10000))
VERSION = "1.17.1"

class Handler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()

    def do_GET(self):
        try:
            # LIMPEZA: Remove barras duplicadas ou extras no início do caminho
            # Ex: /////////live/ver.php -> /live/ver.php
            clean_path = "/" + re.sub(r'/+', '/', self.path).lstrip('/')
            print(f"[CLEAN PATH] {clean_path}")

            # 1. Resposta para ver.php
            if "ver.php" in clean_path:
                host = self.headers.get('Host', 'srv-mtei.onrender.com')
                # Retornamos a URL LIMPA para o jogo não carregar as barras extras nas próximas chamadas
                my_url = f"https://{host}/live/"
                response = f"{VERSION},{my_url},{my_url},{my_url}"
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(response.encode("utf-8"))
                return

            # 2. Resposta para versioninfo
            if "versioninfo" in clean_path:
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(VERSION.encode("utf-8"))
                return

            # 3. Redirecionamento de Assets
            if "/live/" in clean_path:
                filename = clean_path.split('/')[-1]
                # Se houver query params (?), pegamos só o nome do arquivo
                if "?" in filename:
                    filename = filename.split('?')[0]
                
                if filename and not filename.endswith('.php'):
                    self.send_response(302)
                    self.send_header("Location", f"https://freefiremobile-a.akamaihd.net/live/{filename}")
                    self.end_headers()
                    return

            # 4. Root / Status
            if clean_path == "/":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"status": "online", "version": VERSION}).encode("utf-8"))
                return

            self.send_response(404)
            self.end_headers()

        except Exception as e:
            print(traceback.format_exc())
            self.send_response(500)
            self.end_headers()

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok"}).encode("utf-8"))

server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
print(f"SERVER RUNNING ON PORT {PORT}")
server.serve_forever()
