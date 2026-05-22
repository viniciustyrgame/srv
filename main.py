from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import traceback
import re
import time
import uuid

PORT = int(os.environ.get("PORT", 10000))
VERSION = "1.17.1"

# Seus dados originais
FILEINFO_DATA = """gameassetbundles,mzZtylZ1fawV5N8D8XikRyF+5mY=,12060,0
main/gameentry,DZlCrLRuzwyuNzUZrh+p0QxJCcI=,2018,0
localization/loc,gWXz0dDNM8MJyFcAFhzbqWWqvrY=,632921,0
ingame/avatarmanager,Tjb+QEzOiGwy+DBpxlLrVBZRphA=,1915,0
config/resconf,ysnx0NubzKPaLVGszrP45y9WQH0=,34896,0
avatar/assetindexer,IbV74Hqrb07rdlrKYQx6JZIhZ5M=,74343,0
avatar/uma_dcs,BSJQtQt6qEeFdLv8gsrVtPDQubo=,14523,0"""

class Handler(BaseHTTPRequestHandler):

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/plain")
        self.end_headers()

    def handle_request(self):
        try:
            # LIMPEZA UNIVERSAL: Remove barras extras e lida com query params
            # Ex: /////////live/ver.php?v=1 -> /live/ver.php
            raw_path = self.path.split('?')[0]
            clean_path = "/" + re.sub(r'/+', '/', raw_path).lstrip('/')
            print(f"[{self.command}] Original: {self.path} -> Clean: {clean_path}")

            # 1. VER.PHP (A porta de entrada do jogo)
            if "ver.php" in clean_path:
                host = self.headers.get('Host', 'srv-mtei.onrender.com')
                my_url = f"https://{host}/live/"
                response = f"{VERSION},{my_url},{my_url},{my_url}"
                self.send_response(200)
                self.send_header("Content-Type", "text/plain; charset=utf-8")
                self.end_headers()
                self.wfile.write(response.encode("utf-8"))
                return

            # 2. VERSIONINFO / FILEINFO
            if "versioninfo" in clean_path:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(VERSION.encode("utf-8"))
                return
            
            if "fileinfo" in clean_path:
                self.send_response(200)
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(FILEINFO_DATA.encode("utf-8"))
                return

            # 3. OAUTH / LOGIN (Para passar da tela de login)
            if "/oauth/" in clean_path:
                token = str(uuid.uuid4()).replace("-", "")
                data = {
                    "access_token": token,
                    "refresh_token": token,
                    "expiry_time": int(time.time()) + 86400,
                    "open_id": "123456789",
                    "platform": 0
                }
                # Se for inspect, retorna os dados do token
                if "inspect" in clean_path:
                    data = {"open_id": "123456789", "platform": 0, "expire": int(time.time()) + 86400}
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(data).encode("utf-8"))
                return

            # 4. REDIRECIONAMENTO DE ASSETS (O que não for comando, manda pra CDN)
            if "/live/" in clean_path:
                filename = clean_path.split('/')[-1]
                if filename and not filename.endswith('.php'):
                    self.send_response(302)
                    self.send_header("Location", f"https://freefiremobile-a.akamaihd.net/live/{filename}")
                    self.end_headers()
                    return

            # 5. STATUS / ROOT
            if clean_path == "/":
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"server": "online", "version": VERSION}).encode("utf-8"))
                return

            # 6. CAPTURA TUDO (Fallback)
            # Se o jogo pedir algo que não mapeamos, respondemos 200 OK genérico para não dar erro
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")

        except Exception as e:
            print(traceback.format_exc())
            self.send_response(500)
            self.end_headers()

    def do_GET(self):
        self.handle_request()

    def do_POST(self):
        self.handle_request()

server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
print(f"SERVER UNIVERSAL RUNNING ON PORT {PORT}")
server.serve_forever()
