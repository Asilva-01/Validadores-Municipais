import http.server
import socketserver
import json
import logging
import os
import io

# Adicionar caminho para importar validador
import validador_sigiss

PORT = 0
PUBLIC_DIR = os.path.join(os.path.dirname(__file__), 'public')

class NoOpLogger(logging.Logger):
    def __init__(self):
        super().__init__("noop")
    def error(self, msg, *args, **kwargs): pass
    def warning(self, msg, *args, **kwargs): pass
    def info(self, msg, *args, **kwargs): pass
    def critical(self, msg, *args, **kwargs): pass

class SigissHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
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
                    cidade_nome = data.get('cidade')
                    conteudo = data.get('conteudo', '')
                    
                    with open("municipios_config.json", "r", encoding='utf-8') as f:
                        configs = json.load(f)
                        
                    if cidade_nome not in configs:
                        self.send_json({"erro": f"Cidade '{cidade_nome}' não encontrada nas configurações."}, 400)
                        return
                        
                    cidade_config = configs[cidade_nome]
                    
                    linhas = conteudo.splitlines(True) # True keeps line endings if any, but splitlines without true is fine. let's keep True to match readlines() behavior
                    
                    # Usa mock logger para não sujar o stdout do server com os logs de erro do validador.
                    noop_logger = NoOpLogger()
                    memory_list = []
                    
                    sucesso = validador_sigiss.validar_linhas(linhas, cidade_config, None, noop_logger, memory_list)
                    
                    resposta = {
                        "sucesso": sucesso,
                        "ocorrencias": memory_list,
                        "total_linhas": len(linhas) if linhas else 0
                    }
                    self.send_json(resposta, 200)
                    
                except Exception as e:
                    self.send_json({"erro": f"Erro interno: {str(e)}"}, 500)
            else:
                 self.send_json({"erro": "Corpo da requisição vazio."}, 400)
        else:
            self.send_error(404, "Endpoint não encontrado")
            
    def send_json(self, body_dict, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(body_dict).encode('utf-8'))

def run_server():
    os.makedirs(PUBLIC_DIR, exist_ok=True)
    with socketserver.TCPServer(("", PORT), SigissHTTPRequestHandler) as httpd:
        actual_port = httpd.server_address[1]
        print(f"Servidor Web SIGISS rodando na porta http://localhost:{actual_port}")
        print(f"Servindo arquivos da pasta: {PUBLIC_DIR}")
        print("Pressione Ctrl+C para encerrar...")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServidor encerrado.")

if __name__ == '__main__':
    run_server()
