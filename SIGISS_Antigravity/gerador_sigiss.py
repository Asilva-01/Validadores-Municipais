import json
import sys
import re
import argparse
from validador_sigiss import is_valid_cpf, is_valid_cnpj

def format_valor(val):
    # Ensure it's a string, if number convert properly
    s = str(val).replace('.', ',')
    return s

def gerar_linhas(dados, cidade_config):
    linhas = []
    delimitador = cidade_config.get('delimitador', '\t')
    
    for idx, nota in enumerate(dados.get('notas', [])):
        # Campos obrigatórios
        try:
            cpf_cnpj = str(nota['cpf_cnpj'])
            nf = str(nota['nf'])
            serie = str(nota.get('serie', ''))
            sub_serie = str(nota.get('sub_serie', ''))
            dia = str(nota['dia_emissao'])
            cod_serv = str(nota['codigo_servico'])
            sit = str(nota['situacao'])
            valor = format_valor(nota['valor'])
            ccm = str(nota['ccm_tomador'])
            tipo = str(nota['tipo_nf'])
            aliq = format_valor(nota.get('aliquota', ''))
        except KeyError as e:
            print(f"Erro Crítico: Campo obrigatório {e} ausente na nota índice {idx}. Geração abortada.", file=sys.stderr)
            sys.exit(1)
            
        # Validações estritas pre-geracao
        erros = []
        if len(cpf_cnpj) == 11 and not is_valid_cpf(cpf_cnpj):
             erros.append("CPF inválido (DV falhou).")
        elif len(cpf_cnpj) == 14 and not is_valid_cnpj(cpf_cnpj):
             erros.append("CNPJ inválido (DV falhou).")
        elif len(cpf_cnpj) not in [11, 14] or not cpf_cnpj.isdigit():
             erros.append("CPF/CNPJ deve ter 11 ou 14 dígitos numéricos.")
        if not nf.isdigit():
            erros.append("Número da NF deve ser numérico.")
        if not dia.isdigit() or not (1 <= int(dia) <= 31):
            erros.append("Dia de emissão inválido.")
        if not cod_serv or not cod_serv.isdigit():
            erros.append("Código de Serviço obrigatório e deve ser numérico.")
        if sit.lower() not in ['t', 'r', 'i', 'n']:
            erros.append("Situação inválida. Use t, r, i, n.")
        if not (re.match(r'^\d+,\d+$', valor) or valor.isdigit()):
            erros.append(f"Valor com formato inválido (use vírgula): {valor}")
        if not re.match(cidade_config.get('ccm_regex', '.*'), ccm):
            erros.append(f"CCM fora do padrão esperado.")
        if tipo.upper() not in ['T', 'F', 'J', 'R', 'E']:
            erros.append("Tipo de NF inválido.")
            
        if erros:
            print(f"Erro Crítico nas regras de negócio para a nota índice {idx}:", file=sys.stderr)
            for err in erros:
                print(f" - {err}", file=sys.stderr)
            print("Geração abortada.", file=sys.stderr)
            sys.exit(1)
            
        linha = delimitador.join([
            cpf_cnpj, nf, serie, sub_serie, dia, cod_serv, sit, valor, ccm, tipo, aliq
        ])
        linhas.append(linha)
        
    return linhas

def main():
    parser = argparse.ArgumentParser(description="Gerador de arquivo TXT/CSV para SIGISS baseado em JSON")
    parser.add_argument("json_in", help="Arquivo JSON de entrada")
    parser.add_argument("arquivo_out", help="Caminho do arquivo TXT/CSV de saída")
    args = parser.parse_args()
    
    with open(args.json_in, 'r', encoding='utf-8') as f:
        dados = json.load(f)
        
    cidade_nome = dados.get("cidade")
    if not cidade_nome:
        print("Erro: JSON de entrada deve conter a chave 'cidade'.", file=sys.stderr)
        sys.exit(1)
        
    with open("municipios_config.json", "r", encoding='utf-8') as f:
        configs = json.load(f)
        
    if cidade_nome not in configs:
        print(f"Erro: Cidade '{cidade_nome}' não configurada em municipios_config.json", file=sys.stderr)
        sys.exit(1)
        
    cidade_config = configs[cidade_nome]
    linhas = gerar_linhas(dados, cidade_config)
    
    with open(args.arquivo_out, 'w', encoding=cidade_config.get('encoding', 'utf-8')) as f:
        for linha in linhas:
             f.write(linha + "\n")
             
    print(f"Arquivo gerado com sucesso: {args.arquivo_out} ({len(linhas)} registros)")

if __name__ == "__main__":
    main()
