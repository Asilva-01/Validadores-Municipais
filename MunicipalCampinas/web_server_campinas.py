import http.server
import socketserver
import json
import os
from io import BytesIO

# Import o seu validador refatorado
import nota_joeense_campinas

PORT = 0
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), 'public')

class CampinasHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLIC_DIR, **kwargs)
        
    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_POST(self):
        if self.path == '/api/validar':
            content_length = int(self.headers.get('Content-Length', 0))
            if content_length > 0:
                body = self.rfile.read(content_length)
                try:
                    data = json.loads(body)
                    conteudo = data.get('conteudo', '')
                    linhas = [linha for linha in conteudo.split('\n')]
                    
                    # Usa nossa nova funcao nativa
                    resposta = nota_joeense_campinas.validar_linhas(linhas, mode='validate')
                    self.send_json(resposta, 200)
                    
                except Exception as e:
                    import traceback
                    print(traceback.format_exc())
                    self.send_json({"erro": f"Erro interno: {str(e)}"}, 500)
            else:
                 self.send_json({"erro": "Corpo da requisicao vazio."}, 400)
        else:
            self.send_error(404, "Endpoint nao encontrado")
            
    def send_json(self, body_dict, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(body_dict).encode('utf-8'))

def run_server():
    os.makedirs(PUBLIC_DIR, exist_ok=True)
    with socketserver.TCPServer(("", PORT), CampinasHTTPRequestHandler) as httpd:
        actual_port = httpd.server_address[1]
        print(f"Servidor Web Nota Joeense rodando na porta http://localhost:{actual_port}")
        print(f"Servindo arquivos da pasta: {PUBLIC_DIR}")
        print("Pressione Ctrl+C para encerrar...")
        with open('server_port.txt', 'w') as f:
            f.write(str(actual_port))
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")

if __name__ == '__main__':
    run_server()
