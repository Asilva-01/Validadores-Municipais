import sys
import os
import re
import json
import logging
import argparse

def is_valid_cpf(cpf):
    if len(cpf) != 11 or not cpf.isdigit() or cpf == cpf[0] * 11:
        return False
    def calc_digit(cpf_str, factor):
        s = sum(int(digit) * weight for digit, weight in zip(cpf_str, range(factor, 1, -1)))
        d = 11 - (s % 11)
        return str(0 if d >= 10 else d)
    d1 = calc_digit(cpf[:9], 10)
    d2 = calc_digit(cpf[:9] + d1, 11)
    return cpf[-2:] == d1 + d2

def is_valid_cnpj(cnpj):
    if len(cnpj) != 14 or not cnpj.isdigit() or cnpj == cnpj[0] * 14:
        return False
    def calc_digit(cnpj_str, weights):
        s = sum(int(d) * w for d, w in zip(cnpj_str, weights))
        d = 11 - (s % 11)
        return str(0 if d >= 10 else d)
    w1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    w2 = [6] + w1
    d1 = calc_digit(cnpj[:12], w1)
    d2 = calc_digit(cnpj[:12] + d1, w2)
    return cnpj[-2:] == d1 + d2

def log_msg(logger, is_error, linha, campo_idx, campo_nome, msg, valor, regra, memory_list=None):
    nivel = "ERRO" if is_error else "AVISO"
    txt = f"[LINHA {linha}] [CAMPO {campo_idx} - {campo_nome}] [{nivel}]: {msg} | Valor: '{valor}' | Regra: {regra}"
    if memory_list is not None:
        memory_list.append({
            "linha": linha,
            "campo": campo_nome,
            "nivel": nivel,
            "mensagem": msg,
            "valor": valor,
            "regra": regra
        })
    if is_error:
        logger.error(txt)
    else:
        logger.warning(txt)

def validar_arquivo(caminho, cidade_config, competencia, logger, memory_list=None):
    erros_encontrados = False
    with open(caminho, 'r', encoding=cidade_config.get('encoding', 'utf-8')) as f:
        linhas = f.readlines()
        
    return validar_linhas(linhas, cidade_config, competencia, logger, memory_list)

def validar_linhas(linhas, cidade_config, competencia, logger, memory_list=None):
    erros_encontrados = False
    if not linhas:
        logger.error("Arquivo vazio.")
        if memory_list is not None: memory_list.append({"linha": 0, "campo": "Arquivo", "nivel": "ERRO", "mensagem": "Arquivo vazio", "valor": "", "regra": ""})
        return False
        
    for i, linha in enumerate(linhas, 1):
        linha_crua = linha.strip('\r\n')
        if not linha_crua:
            continue
            
        sep = ';' if ';' in linha_crua else ('\t' if '\t' in linha_crua else None)
        if not sep:
            logger.critical(f"[LINHA {i}] CRÍTICO: Delimitador não é ';' nem TAB.")
            if memory_list is not None: memory_list.append({"linha": i, "campo": "Delimitador", "nivel": "ERRO", "mensagem": "Delimitador inválido", "valor": "", "regra": "; ou TAB"})
            return False
            
        campos = linha_crua.split(sep)
        # O layout dita 11 campos. Pode haver variação dependendo do trailing sep, ajustaremos p/ 11 se houver menos
        if len(campos) < 11:
             campos.extend([''] * (11 - len(campos)))
             
        # Campo 1: CPF/CNPJ
        cpf_cnpj = campos[0].strip()
        if len(cpf_cnpj) == 11:
            if not is_valid_cpf(cpf_cnpj):
                log_msg(logger, True, i, 1, "CPF/CNPJ", "CPF inválido", cpf_cnpj, "11 dígitos com DV válido", memory_list=memory_list)
                erros_encontrados = True
        elif len(cpf_cnpj) == 14:
            if not is_valid_cnpj(cpf_cnpj):
                log_msg(logger, True, i, 1, "CPF/CNPJ", "CNPJ inválido", cpf_cnpj, "14 dígitos com DV válido", memory_list=memory_list)
                erros_encontrados = True
        else:
            log_msg(logger, True, i, 1, "CPF/CNPJ", "Tamanho incorreto", cpf_cnpj, "Deve ter 11 ou 14 dígitos", memory_list=memory_list)
            erros_encontrados = True
            
        # Campo 2: Nº NF
        nf = campos[1].strip()
        if not nf.isdigit():
            log_msg(logger, True, i, 2, "Nº NF", "Numérico obrigatório", nf, "Apenas números", memory_list=memory_list)
            erros_encontrados = True
            
        # Campo 3: Série
        serie = campos[2].strip()
        if not serie:
             log_msg(logger, False, i, 3, "Série", "Série vazia", serie, "Opcional mas recomendado", memory_list=memory_list)
             
        # Campo 4: Sub-Série
        subserie = campos[3].strip()
        if not subserie:
             log_msg(logger, False, i, 4, "Sub-Série", "Sub-Série vazia", subserie, "Opcional mas recomendado", memory_list=memory_list)
             
        # Campo 5: Dia de Emissão
        dia = campos[4].strip()
        if not dia.isdigit() or not (1 <= int(dia) <= 31):
            log_msg(logger, True, i, 5, "Dia Emissão", "Dia inválido", dia, "Entre 1 e 31", memory_list=memory_list)
            erros_encontrados = True
            
        # Campo 6: Cód Serviço
        cod_servico = campos[5].strip()
        if not cod_servico:
             log_msg(logger, True, i, 6, "Cód. Serviço", "Vazio ou ausente", cod_servico, "Obrigatório (Dígitos)", memory_list=memory_list)
             erros_encontrados = True
        elif not cod_servico.isdigit():
             log_msg(logger, True, i, 6, "Cód. Serviço", "Não numérico", cod_servico, "Requer apenas dígitos", memory_list=memory_list)
             erros_encontrados = True
             
        # Campo 7: Situação
        sit = campos[6].strip().lower()
        mapping = cidade_config.get('map_situacao_aviso', {})
        if sit in mapping:
             log_msg(logger, False, i, 7, "Situação", f"Mapeado automático de '{sit}' para '{mapping[sit]}'", sit, "Desconformidade tolerada por município", memory_list=memory_list)
             sit = mapping[sit]
        if sit not in ['t', 'r', 'i', 'n']:
             log_msg(logger, True, i, 7, "Situação", "Inválido", campos[6].strip(), "Permitidos: t, r, i, n", memory_list=memory_list)
             erros_encontrados = True
             
        # Campo 8: Valor
        valor = campos[7].strip()
        if '.' in valor:
             log_msg(logger, True, i, 8, "Valor", "Uso de ponto como decimal", valor, "Proibido ponto. Usar vírgula", memory_list=memory_list)
             erros_encontrados = True
        elif not re.match(r'^\d+,\d{2,}$', valor) and not re.match(r'^\d+$', valor):
             log_msg(logger, True, i, 8, "Valor", "Formato inválido", valor, "Decimal nacional com vírgula", memory_list=memory_list)
             erros_encontrados = True
             
        # Campo 9: CCM
        ccm = campos[8].strip()
        regex_ccm = cidade_config.get('ccm_regex', '.*')
        if not re.match(regex_ccm, ccm):
             log_msg(logger, True, i, 9, "CCM Tomador", "Fora do padrão do município", ccm, f"Regex esperada: {regex_ccm}", memory_list=memory_list)
             erros_encontrados = True
             
        # Campo 10: Tipo NF
        tipo = campos[9].strip().upper()
        mapping_tipo = cidade_config.get('map_tipo_aviso', {})
        if tipo in mapping_tipo:
             log_msg(logger, False, i, 10, "Tipo NF", f"Mapeado automático de '{tipo}' para '{mapping_tipo[tipo]}'", tipo, "Desconformidade tolerada por município", memory_list=memory_list)
             tipo = mapping_tipo[tipo]
             
        if tipo not in ['T', 'F', 'J', 'R', 'E']:
             log_msg(logger, True, i, 10, "Tipo NF", "Inválido", campos[9].strip(), "Permitidos: T, F, J, R, E", memory_list=memory_list)
             erros_encontrados = True
             
        # Campo 11: Alíquota
        aliq = campos[10].strip()
        if aliq:
            if '.' in aliq:
                log_msg(logger, True, i, 11, "Alíquota Simples", "Uso de ponto como decimal", aliq, "Proibido ponto. Usar vírgula", memory_list=memory_list)
                erros_encontrados = True
            elif not re.match(r'^\d+,\d{2,4}$', aliq) and not re.match(r'^\d+$', aliq):
                log_msg(logger, True, i, 11, "Alíquota Simples", "Formato inválido", aliq, "Decimal nacional com vírgula", memory_list=memory_list)
                erros_encontrados = True
        # If empty, it's allowed according to Chapecó texts, so no warning or error.

    return not erros_encontrados

def main():
    parser = argparse.ArgumentParser(description="Validador SIGISS NFS-e")
    parser.add_argument("arquivo", help="Caminho do arquivo TXT/CSV a validar")
    parser.add_argument("--cidade", required=True, help="Nome da cidade no municipios_config.json")
    parser.add_argument("--competencia", help="Competência (MM/YYYY)", default=None)
    args = parser.parse_args()

    # Logger
    log_file = args.arquivo + ".log"
    logging.basicConfig(level=logging.INFO, format='%(message)s', handlers=[
        logging.FileHandler(log_file, mode='w', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ])
    logger = logging.getLogger("SIGISS")

    with open("municipios_config.json", "r", encoding='utf-8') as f:
        configs = json.load(f)

    if args.cidade not in configs:
        logger.error(f"Erro: Cidade '{args.cidade}' não encontrada no config!")
        sys.exit(1)

    cidade_config = configs[args.cidade]
    logger.info(f"=== INICIANDO VALIDAÇÃO: {args.arquivo} | CIDADE: {args.cidade} ===")
    logger.info(f"Log detalhado salvo em: {log_file}")
    
    sucesso = validar_arquivo(args.arquivo, cidade_config, args.competencia, logger)
    if not sucesso:
        logger.error("\n[!] Validação concluída com ERROS.")
        sys.exit(1)
    else:
        logger.info("\n[+] Validação concluída com SUCESSO. Apenas avisos, se houver.")
        sys.exit(0)

if __name__ == "__main__":
    main()
