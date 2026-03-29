#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Servidor Web para Validacao de Arquivos SIGISS

Interface web simples para upload e validacao de arquivos SIGISS/SIGCORP
sem dependencias externas (usa apenas biblioteca padrao Python).

Uso:
    python web_validator.py
    python web_validator.py --port 8080

Acesse: http://localhost:8000
"""

import argparse
import http.server
import json
import os
import subprocess
import sys
import tempfile
import urllib.parse
from datetime import datetime
from pathlib import Path


HTML_PAGE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Validador SIGISS - Interface Web</title>
    <style>
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }

        .header h1 {
            font-size: 28px;
            margin-bottom: 10px;
        }

        .header p {
            opacity: 0.9;
            font-size: 14px;
        }

        .content {
            padding: 40px;
        }

        .form-group {
            margin-bottom: 25px;
        }

        label {
            display: block;
            margin-bottom: 8px;
            font-weight: 600;
            color: #333;
            font-size: 14px;
        }

        select, input[type="file"] {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            transition: border-color 0.3s;
            background: white;
        }

        select:focus, input[type="file"]:focus {
            outline: none;
            border-color: #667eea;
        }

        .file-input-wrapper {
            position: relative;
            overflow: hidden;
            display: inline-block;
            width: 100%;
        }

        .file-input-wrapper input[type=file] {
            position: absolute;
            left: 0;
            top: 0;
            opacity: 0;
            cursor: pointer;
            height: 100%;
        }

        .file-input-label {
            display: block;
            padding: 15px 20px;
            background: #f8f9fa;
            border: 2px dashed #ccc;
            border-radius: 8px;
            text-align: center;
            color: #666;
            cursor: pointer;
            transition: all 0.3s;
        }

        .file-input-wrapper:hover .file-input-label {
            background: #e9ecef;
            border-color: #667eea;
            color: #667eea;
        }

        .file-name {
            margin-top: 10px;
            font-size: 13px;
            color: #28a745;
            font-weight: 500;
        }

        .btn-submit {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .btn-submit:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.4);
        }

        .btn-submit:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        .result {
            margin-top: 30px;
            padding: 25px;
            border-radius: 8px;
            display: none;
        }

        .result.success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }

        .result.error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }

        .result.warning {
            background: #fff3cd;
            border: 1px solid #ffeaa7;
            color: #856404;
        }

        .result h3 {
            margin-bottom: 15px;
            font-size: 18px;
        }

        .result-content {
            white-space: pre-wrap;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 13px;
            line-height: 1.6;
            overflow-x: auto;
            max-height: 400px;
            overflow-y: auto;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }

        .stat-box {
            background: rgba(255,255,255,0.5);
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }

        .stat-value {
            font-size: 24px;
            font-weight: bold;
            color: #333;
        }

        .stat-label {
            font-size: 12px;
            color: #666;
            margin-top: 5px;
        }

        .problems-list {
            margin-top: 20px;
        }

        .problem-item {
            background: white;
            border-left: 4px solid;
            padding: 12px 15px;
            margin-bottom: 10px;
            border-radius: 0 8px 8px 0;
            font-size: 13px;
        }

        .problem-item.error {
            border-left-color: #dc3545;
            background: #fff5f5;
        }

        .problem-item.warning {
            border-left-color: #ffc107;
            background: #fffbf0;
        }

        .problem-level {
            font-weight: bold;
            font-size: 11px;
            text-transform: uppercase;
            padding: 2px 8px;
            border-radius: 4px;
            margin-right: 10px;
        }

        .problem-level.error {
            background: #dc3545;
            color: white;
        }

        .problem-level.warning {
            background: #ffc107;
            color: #333;
        }

        .footer {
            text-align: center;
            padding: 20px;
            background: #f8f9fa;
            color: #666;
            font-size: 12px;
        }

        .loading {
            display: none;
            text-align: center;
            padding: 20px;
        }

        .loading-spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 30px;
            height: 30px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📋 Validador SIGISS/SIGCORP</h1>
            <p>Valide arquivos de remessa de Notas Fiscais de Serviço Eletrônicas</p>
        </div>

        <div class="content">
            <form id="uploadForm" enctype="multipart/form-data">
                <div class="form-group">
                    <label for="municipio">🏙️ Município</label>
                    <select name="municipio" id="municipio" required>
                        <option value="">-- Selecione o município --</option>
                        {MUNICIPIOS_OPTIONS}
                    </select>
                </div>

                <div class="form-group">
                    <label>📁 Arquivo de Remessa (.txt)</label>
                    <div class="file-input-wrapper">
                        <input type="file" name="arquivo" id="arquivo" accept=".txt,.csv" required onchange="updateFileName(this)">
                        <div class="file-input-label">
                            Clique aqui para selecionar o arquivo<br>
                            <small>Formatos aceitos: .txt, .csv</small>
                        </div>
                    </div>
                    <div class="file-name" id="fileName"></div>
                </div>

                <button type="submit" class="btn-submit" id="submitBtn">
                    🔍 Validar Arquivo
                </button>
            </form>

            <div class="loading" id="loading">
                <div class="loading-spinner"></div>
                <p>Validando arquivo...</p>
            </div>

            <div class="result" id="result">
                <h3 id="resultTitle"></h3>
                <div class="stats" id="stats"></div>
                <div class="result-content" id="resultContent"></div>
                <div class="problems-list" id="problemsList"></div>
            </div>
        </div>

        <div class="footer">
            Sistema de Validação SIGISS/SIGCORP | Python 3.8+
        </div>
    </div>

    <script>
        function updateFileName(input) {
            const fileName = document.getElementById('fileName');
            if (input.files && input.files[0]) {
                fileName.textContent = '✓ ' + input.files[0].name;
            }
        }

        document.getElementById('uploadForm').addEventListener('submit', async function(e) {
            e.preventDefault();

            const formData = new FormData(this);
            const loading = document.getElementById('loading');
            const result = document.getElementById('result');
            const submitBtn = document.getElementById('submitBtn');

            loading.style.display = 'block';
            result.style.display = 'none';
            submitBtn.disabled = true;

            try {
                const response = await fetch('/validate', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                displayResult(data);
            } catch (error) {
                displayResult({
                    error: true,
                    message: 'Erro ao processar: ' + error.message
                });
            } finally {
                loading.style.display = 'none';
                submitBtn.disabled = false;
            }
        });

        function displayResult(data) {
            const result = document.getElementById('result');
            const resultTitle = document.getElementById('resultTitle');
            const resultContent = document.getElementById('resultContent');
            const stats = document.getElementById('stats');
            const problemsList = document.getElementById('problemsList');

            result.style.display = 'block';
            result.className = 'result';

            if (data.error) {
                result.classList.add('error');
                resultTitle.textContent = '❌ Erro';
                resultContent.textContent = data.message;
                stats.innerHTML = '';
                problemsList.innerHTML = '';
                return;
            }

            if (data.valido) {
                result.classList.add('success');
                resultTitle.textContent = '✅ Arquivo Válido';
            } else {
                result.classList.add('error');
                resultTitle.textContent = '❌ Arquivo Inválido';
            }

            // Stats
            stats.innerHTML = `
                <div class="stat-box">
                    <div class="stat-value">${data.total_linhas}</div>
                    <div class="stat-label">Linhas</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" style="color: ${data.total_erros > 0 ? '#dc3545' : '#28a745'}">${data.total_erros}</div>
                    <div class="stat-label">Erros</div>
                </div>
                <div class="stat-box">
                    <div class="stat-value" style="color: ${data.total_avisos > 0 ? '#ffc107' : '#28a745'}">${data.total_avisos}</div>
                    <div class="stat-label">Avisos</div>
                </div>
            `;

            // Problems
            if (data.problemas && data.problemas.length > 0) {
                problemsList.innerHTML = '<h4 style="margin-bottom: 15px;">Detalhamento dos Problemas:</h4>' +
                    data.problemas.map(p => `
                        <div class="problem-item ${p.nivel.toLowerCase()}">
                            <span class="problem-level ${p.nivel.toLowerCase()}">${p.nivel}</span>
                            <strong>Linha ${p.linha} - ${p.campo}</strong><br>
                            <span style="color: #666;">Valor: '${p.valor_encontrado}'</span><br>
                            ${p.mensagem}
                        </div>
                    `).join('');
            } else {
                problemsList.innerHTML = '<div style="text-align: center; padding: 20px; color: #28a745;">✓ Nenhum problema encontrado!</div>';
            }

            resultContent.textContent = data.relatorio || '';
        }
    </script>
</body>
</html>
"""


class ValidationHandler(http.server.BaseHTTPRequestHandler):
    """Handler para requisicoes HTTP de validacao."""

    def log_message(self, format, *args):
        """Override para log customizado."""
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {args[0]}")

    def do_GET(self):
        """Processa requisicoes GET."""
        if self.path == '/' or self.path == '/index.html':
            self.send_html_page()
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        """Processa requisicoes POST (upload e validacao)."""
        if self.path == '/validate':
            self.handle_validation()
        else:
            self.send_error(404, "Not Found")

    def send_html_page(self):
        """Envia a pagina HTML principal."""
        # Carrega lista de municipios
        municipios = self.load_municipios()
        options = '\n'.join([
            f'<option value="{m}">{m}</option>'
            for m in municipios
        ])

        html = HTML_PAGE.replace('{MUNICIPIOS_OPTIONS}', options)

        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def load_municipios(self):
        """Carrega lista de municipios do arquivo de configuracao."""
        try:
            config_path = Path(__file__).parent / "municipios_config.json"
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return list(config.get('municipios', {}).keys())
        except Exception:
            return ["Itapira-SP", "Mogi Mirim-SP", "Chapeco-SC"]

    def handle_validation(self):
        """Processa upload e validacao do arquivo."""
        try:
            # Parse do formulario multipart
            content_type = self.headers.get('Content-Type', '')
            if not content_type.startswith('multipart/form-data'):
                self.send_json_response({'error': True, 'message': 'Content-Type invalido'})
                return

            # Lê o body da requisicao
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            # Extrai boundary
            boundary = content_type.split('boundary=')[1].encode()

            # Parse manual do multipart
            parts = body.split(b'--' + boundary)

            arquivo_data = None
            arquivo_filename = None
            municipio = None

            for part in parts:
                if b'Content-Disposition' not in part:
                    continue

                # Separa headers do conteudo
                headers_end = part.find(b'\r\n\r\n')
                if headers_end == -1:
                    continue

                headers = part[:headers_end].decode('utf-8', errors='ignore')
                content = part[headers_end + 4:].rstrip(b'\r\n')

                # Extrai nome do campo
                if 'name="municipio"' in headers:
                    municipio = content.decode('utf-8').strip()
                elif 'name="arquivo"' in headers:
                    # Extrai filename
                    filename_match = headers.split('filename="')
                    if len(filename_match) > 1:
                        arquivo_filename = filename_match[1].split('"')[0]
                    arquivo_data = content

            if not arquivo_data or not arquivo_filename:
                self.send_json_response({'error': True, 'message': 'Arquivo nao fornecido'})
                return

            if not municipio:
                self.send_json_response({'error': True, 'message': 'Municipio nao selecionado'})
                return

            # Salva arquivo temporario
            temp_dir = tempfile.mkdtemp()
            temp_path = Path(temp_dir) / arquivo_filename

            with open(temp_path, 'wb') as f:
                f.write(arquivo_data)

            try:
                # Executa validacao
                result = self.run_validation(temp_path, municipio)
                self.send_json_response(result)
            finally:
                # Limpa arquivo temporario
                import shutil
                shutil.rmtree(temp_dir, ignore_errors=True)

        except Exception as e:
            self.send_json_response({'error': True, 'message': str(e)})

    def run_validation(self, arquivo_path, municipio):
        """Executa o validador e retorna resultado em JSON."""
        try:
            # Chama o validador como subprocesso
            script_dir = Path(__file__).parent
            validador_path = script_dir / "validador_sigiss.py"

            cmd = [
                sys.executable,
                str(validador_path),
                '--municipio', municipio,
                '--arquivo', str(arquivo_path),
                '--verbose'
            ]

            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )

            # Analisa saida para extrair dados
            stdout = result.stdout
            stderr = result.stderr

            # Verifica se e valido pelo codigo de retorno
            valido = result.returncode == 0

            # Parse do relatorio para extrair estatisticas
            total_linhas = 0
            total_erros = 0
            total_avisos = 0
            problemas = []

            for line in stdout.split('\n'):
                if 'Total de linhas processadas:' in line:
                    try:
                        total_linhas = int(line.split(':')[1].strip())
                    except:
                        pass
                elif 'Total de ERROS:' in line:
                    try:
                        total_erros = int(line.split(':')[1].strip())
                    except:
                        pass
                elif 'Total de AVISOS:' in line:
                    try:
                        total_avisos = int(line.split(':')[1].strip())
                    except:
                        pass
                elif '[ERRO]' in line or '[AVISO]' in line:
                    # Parse de problemas
                    if 'Linha' in line and 'Campo:' in line:
                        nivel = 'ERRO' if '[ERRO]' in line else 'AVISO'
                        try:
                            linha_match = line.split('Linha ')[1].split(' -')[0]
                            campo_match = line.split('Campo: ')[1].split()[0]
                            valor_match = line.split("Valor encontrado: '")[1].split("'")[0] if "Valor encontrado: '" in line else ''
                            mensagem = line.split('Mensagem: ')[1] if 'Mensagem: ' in line else line

                            problemas.append({
                                'nivel': nivel,
                                'linha': int(linha_match) if linha_match.isdigit() else 0,
                                'campo': campo_match,
                                'valor_encontrado': valor_match,
                                'mensagem': mensagem
                            })
                        except:
                            pass

            return {
                'valido': valido,
                'total_linhas': total_linhas,
                'total_erros': total_erros,
                'total_avisos': total_avisos,
                'problemas': problemas,
                'relatorio': stdout + '\n' + stderr
            }

        except Exception as e:
            return {
                'error': True,
                'message': f'Erro ao executar validacao: {str(e)}'
            }

    def send_json_response(self, data):
        """Envia resposta JSON."""
        self.send_response(200)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))


def run_server(port=8000):
    """Inicia o servidor web."""
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, ValidationHandler)

    print(f"\n{'='*60}")
    print(f"  Validador SIGISS - Interface Web")
    print(f"{'='*60}")
    print(f"  Servidor iniciado em: http://localhost:{port}")
    print(f"  Pressione Ctrl+C para parar")
    print(f"{'='*60}\n")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        httpd.shutdown()


def main():
    """Funcao principal."""
    parser = argparse.ArgumentParser(
        description='Servidor Web para Validacao SIGISS',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Exemplos:
  python web_validator.py
  python web_validator.py --port 8080
  python web_validator.py --port 3000

Depois acesse http://localhost:PORTA no navegador
        '''
    )

    parser.add_argument(
        '--port', '-p',
        type=int,
        default=8000,
        help='Porta do servidor (padrao: 8000)'
    )

    args = parser.parse_args()

    # Verifica se os arquivos necessarios existem
    script_dir = Path(__file__).parent
    if not (script_dir / "validador_sigiss.py").exists():
        print("Erro: validador_sigiss.py nao encontrado!")
        sys.exit(1)

    if not (script_dir / "municipios_config.json").exists():
        print("Erro: municipios_config.json nao encontrado!")
        sys.exit(1)

    run_server(args.port)


if __name__ == '__main__':
    main()
