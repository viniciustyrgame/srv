from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
import traceback

PORT = int(os.environ.get("PORT", 10000))

# O Hash que você encontrou no metadata
LIVE_HASH = "1000678a9449649a1748f16cc0b922eee9c83cea4f3ac6f5981211536ad9fa0db941332ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3"

VERSION = "1.17.1"

class Handler(BaseHTTPRequestHandler):

    def write_log(self):
        print(f"\n[REQUEST] {self.command} {self.path}")

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
            path = self.path
            
            # 1. Resposta para ver.php (O mais importante para o login)
            if "ver.php" in path:
                host = self.headers.get('Host', 'srv-mtei.onrender.com')
                # O formato esperado pela Garena: Versão, CDN1, CDN2, CDN3
                # Colocamos a sua URL do Render como CDN para o jogo continuar pedindo arquivos aqui
                my_url = f"https://{host}/live/"
                response = f"{VERSION},{my_url},{my_url},{my_url}"
                return self.send_text(response)

            # 2. Resposta para versioninfo
            if "versioninfo" in path:
                return self.send_text(VERSION)

            # 3. Redirecionamento de Assets (Se não for ver.php ou versioninfo)
            # Se o jogo pedir um arquivo (ex: .unity3d), mandamos para a CDN oficial
            if "/live/" in path:
                filename = path.split('/')[-1]
                if filename and not filename.endswith('.php'):
                    self.send_response(302)
                    self.send_header("Location", f"https://freefiremobile-a.akamaihd.net/live/{filename}")
                    self.end_headers()
                    return

            # 4. Root / Status
            if path == "/":
                return self.send_json({"status": "online", "server": "Luna Private", "version": VERSION})

            # Caso contrário, 404
            self.send_json({"path": path, "error": "not_found"}, 404)

        except Exception as e:
            print(traceback.format_exc())
            self.send_json({"error": str(e)}, 500)

    def do_POST(self):
        # Para rotas de login/auth se necessário no futuro
        self.write_log()
        self.send_json({"status": "ok", "message": "POST received"})

server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
print(f"SERVER RUNNING ON PORT {PORT}")
server.serve_forever()
