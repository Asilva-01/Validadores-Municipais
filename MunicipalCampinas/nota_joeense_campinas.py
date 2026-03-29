import os
import re
import sys
import json
import logging
import argparse
from datetime import datetime

LAYOUT_T = [
    {"num": 1, "nome": "Identificacao", "tipo": "A", "pi": 1, "pf": 1, "tam": 1, "obrig": "S", "align": "<", "pad": " "},
    {"num": 2, "nome": "Data Emissao", "tipo": "D", "pi": 2, "pf": 11, "tam": 10, "obrig": "S", "align": "<", "pad": " "},
    {"num": 3, "nome": "Data Competencia", "tipo": "D", "pi": 12, "pf": 18, "tam": 7, "obrig": "S", "align": "<", "pad": " "},
    {"num": 4, "nome": "Numero Doc Fiscal", "tipo": "N", "pi": 19, "pf": 33, "tam": 15, "obrig": "S", "align": "0", "pad": "0"}, # Changed to 0 pad based on rule 4, actually rule 4 says "Alinhar à esquerda e preencher espaços" for Doc Fiscal! Let's follow manual exactly.
    {"num": 5, "nome": "Serie Doc Fiscal", "tipo": "A", "pi": 34, "pf": 38, "tam": 5, "obrig": "N", "align": "<", "pad": " "},
    {"num": 6, "nome": "Modelo Doc Fiscal", "tipo": "A", "pi": 39, "pf": 40, "tam": 2, "obrig": "S", "align": "<", "pad": " "},
    {"num": 7, "nome": "Tipo Prestador", "tipo": "N", "pi": 41, "pf": 41, "tam": 1, "obrig": "S", "align": "<", "pad": " "},
    {"num": 8, "nome": "CPF_CNPJ", "tipo": "N", "pi": 42, "pf": 55, "tam": 14, "obrig": "S", "align": "0", "pad": "0"},
    {"num": 9, "nome": "ID Exterior", "tipo": "A", "pi": 56, "pf": 75, "tam": 20, "obrig": "N", "align": "<", "pad": " "},
    {"num": 10, "nome": "Nome Razao Social", "tipo": "A", "pi": 76, "pf": 225, "tam": 150, "obrig": "S", "align": "<", "pad": " "},
    {"num": 11, "nome": "Cod Municipio Prestador", "tipo": "A", "pi": 226, "pf": 232, "tam": 7, "obrig": "S", "align": "<", "pad": " "},
    {"num": 12, "nome": "Optante Simples", "tipo": "A", "pi": 233, "pf": 233, "tam": 1, "obrig": "S", "align": "<", "pad": " "},
    {"num": 13, "nome": "MEI", "tipo": "A", "pi": 234, "pf": 234, "tam": 1, "obrig": "S", "align": "<", "pad": " "},
    {"num": 14, "nome": "Estabelecido Municipio", "tipo": "A", "pi": 235, "pf": 235, "tam": 1, "obrig": "S", "align": "<", "pad": " "},
    {"num": 15, "nome": "CEP", "tipo": "N", "pi": 236, "pf": 243, "tam": 8, "obrig": "S", "align": "<", "pad": " "},
    {"num": 16, "nome": "Tipo Logradouro", "tipo": "A", "pi": 244, "pf": 268, "tam": 25, "obrig": "S", "align": "<", "pad": " "},
    {"num": 17, "nome": "Nome Logradouro", "tipo": "A", "pi": 269, "pf": 318, "tam": 50, "obrig": "N", "align": "<", "pad": " "},
    {"num": 18, "nome": "Numero Logradouro", "tipo": "A", "pi": 319, "pf": 328, "tam": 10, "obrig": "N", "align": "<", "pad": " "}, 
    {"num": 19, "nome": "Complemento", "tipo": "A", "pi": 329, "pf": 388, "tam": 60, "obrig": "N", "align": "<", "pad": " "},
    {"num": 20, "nome": "Bairro", "tipo": "A", "pi": 389, "pf": 448, "tam": 60, "obrig": "N", "align": "<", "pad": " "},
    {"num": 21, "nome": "UF", "tipo": "A", "pi": 449, "pf": 450, "tam": 2, "obrig": "S", "align": "<", "pad": " "},
    {"num": 22, "nome": "Pais", "tipo": "A", "pi": 451, "pf": 454, "tam": 4, "obrig": "S", "align": "<", "pad": " "},
    {"num": 23, "nome": "Cidade", "tipo": "A", "pi": 455, "pf": 504, "tam": 50, "obrig": "S", "align": "<", "pad": " "},
    {"num": 24, "nome": "Cod Servico", "tipo": "A", "pi": 505, "pf": 509, "tam": 5, "obrig": "N", "align": "<", "pad": " "},
    {"num": 25, "nome": "Cod Atividade CNAE", "tipo": "A", "pi": 510, "pf": 518, "tam": 9, "obrig": "N", "align": "<", "pad": " "},
    {"num": 26, "nome": "Cod Obra", "tipo": "A", "pi": 519, "pf": 533, "tam": 15, "obrig": "N", "align": "<", "pad": " "},
    {"num": 27, "nome": "Local Prestacao", "tipo": "A", "pi": 534, "pf": 536, "tam": 3, "obrig": "S", "align": "<", "pad": " "},
    {"num": 28, "nome": "Cod Munic Prestacao", "tipo": "A", "pi": 537, "pf": 543, "tam": 7, "obrig": "N", "align": "<", "pad": " "},
    {"num": 29, "nome": "UF Prestacao", "tipo": "A", "pi": 544, "pf": 545, "tam": 2, "obrig": "N", "align": "<", "pad": " "},
    {"num": 30, "nome": "Munic Exterior", "tipo": "A", "pi": 546, "pf": 595, "tam": 50, "obrig": "N", "align": "<", "pad": " "},
    {"num": 31, "nome": "Estado Exterior", "tipo": "A", "pi": 596, "pf": 645, "tam": 50, "obrig": "N", "align": "<", "pad": " "},
    {"num": 32, "nome": "Pais Prestacao", "tipo": "A", "pi": 646, "pf": 649, "tam": 4, "obrig": "N", "align": "<", "pad": " "},
    {"num": 33, "nome": "Local Resultado", "tipo": "A", "pi": 650, "pf": 652, "tam": 3, "obrig": "N", "align": "<", "pad": " "},
    {"num": 34, "nome": "Cod Munic Resultado", "tipo": "A", "pi": 653, "pf": 659, "tam": 7, "obrig": "N", "align": "<", "pad": " "},
    {"num": 35, "nome": "UF Resultado", "tipo": "A", "pi": 660, "pf": 661, "tam": 2, "obrig": "N", "align": "<", "pad": " "},
    {"num": 36, "nome": "Munic Ext Result", "tipo": "A", "pi": 662, "pf": 711, "tam": 50, "obrig": "N", "align": "<", "pad": " "},
    {"num": 37, "nome": "Est Ext Result", "tipo": "A", "pi": 712, "pf": 761, "tam": 50, "obrig": "N", "align": "<", "pad": " "},
    {"num": 38, "nome": "Pais Result", "tipo": "A", "pi": 762, "pf": 765, "tam": 4, "obrig": "N", "align": "<", "pad": " "},
    {"num": 39, "nome": "Motivo Nao Retencao", "tipo": "A", "pi": 766, "pf": 766, "tam": 1, "obrig": "N", "align": "<", "pad": " "},
    {"num": 40, "nome": "Exigibilidade", "tipo": "A", "pi": 767, "pf": 767, "tam": 1, "obrig": "S", "align": "<", "pad": " "},
    {"num": 41, "nome": "Tipo Recolhimento", "tipo": "A", "pi": 768, "pf": 770, "tam": 3, "obrig": "S", "align": "<", "pad": " "},
    {"num": 42, "nome": "Aliquota", "tipo": "N", "pi": 771, "pf": 775, "tam": 5, "obrig": "N", "align": "0", "pad": "0"},
    {"num": 43, "nome": "Valor NF", "tipo": "N", "pi": 776, "pf": 790, "tam": 15, "obrig": "S", "align": "0", "pad": "0"},
    {"num": 44, "nome": "Valor Deducoes", "tipo": "N", "pi": 791, "pf": 805, "tam": 15, "obrig": "N", "align": "0", "pad": "0"}, 
    {"num": 45, "nome": "Desc Incondicional", "tipo": "N", "pi": 806, "pf": 820, "tam": 15, "obrig": "N", "align": "0", "pad": "0"},
    {"num": 46, "nome": "Desc Condicionado", "tipo": "N", "pi": 821, "pf": 835, "tam": 15, "obrig": "N", "align": "0", "pad": "0"},
    {"num": 47, "nome": "Base Calculo", "tipo": "N", "pi": 836, "pf": 850, "tam": 15, "obrig": "S", "align": "0", "pad": "0"},
    {"num": 48, "nome": "PIS", "tipo": "N", "pi": 851, "pf": 865, "tam": 15, "obrig": "N", "align": "0", "pad": "0"},
    {"num": 49, "nome": "COFINS", "tipo": "N", "pi": 866, "pf": 880, "tam": 15, "obrig": "N", "align": "0", "pad": "0"},
    {"num": 50, "nome": "INSS", "tipo": "N", "pi": 881, "pf": 895, "tam": 15, "obrig": "N", "align": "0", "pad": "0"},
    {"num": 51, "nome": "IR", "tipo": "N", "pi": 896, "pf": 910, "tam": 15, "obrig": "N", "align": "0", "pad": "0"},
    {"num": 52, "nome": "CSLL", "tipo": "N", "pi": 911, "pf": 925, "tam": 15, "obrig": "N", "align": "0", "pad": "0"},
    {"num": 53, "nome": "Outras Retencoes", "tipo": "N", "pi": 926, "pf": 940, "tam": 15, "obrig": "N", "align": "0", "pad": "0"},
    {"num": 54, "nome": "Valor ISS", "tipo": "N", "pi": 941, "pf": 955, "tam": 15, "obrig": "N", "align": "0", "pad": "0"},
    {"num": 55, "nome": "Descriminacao", "tipo": "A", "pi": 956, "pf": 2955, "tam": 2000, "obrig": "N", "align": "<", "pad": " "}
]

LAYOUT_H = [
    {"num": 1, "nome": "Identificacao", "tipo": "A", "pi": 1, "pf": 1, "tam": 1, "obrig": "S", "align": "<", "pad": " "},
    {"num": 2, "nome": "Inscricao Municipal", "tipo": "A", "pi": 2, "pf": 31, "tam": 30, "obrig": "S", "align": "<", "pad": " "}
]

# Field 4 "Numero Doc Fiscal" needs left space padding explicitly mentioned in manual
LAYOUT_T[3]['align'] = '<'
LAYOUT_T[3]['pad'] = ' '

def parse_line(linha, layout):
    data = {}
    for f in layout:
        pi = f['pi'] - 1
        pf = f['pf']
        val = linha[pi:pf]
        data[f['num']] = {
            "nome": f['nome'],
            "raw": val,
            "val": val.strip() if f['align'] == '<' else (val.lstrip('0') if val.lstrip('0') else '0')
        }
        # keep decimals as standard formatting
        if f['tipo'] == 'N' and '.' in val and f['align'] == '0':
            data[f['num']]['val'] = val.lstrip('0')
            if data[f['num']]['val'].startswith('.'):
                 data[f['num']]['val'] = '0' + data[f['num']]['val']
            if data[f['num']]['val'] == '':
                 data[f['num']]['val'] = '0.00'
    return data

def format_line(data_dict, layout):
    out = ""
    for f in layout:
        val = str(data_dict.get(str(f['num']), ''))
        
        # apply formatting
        if f['align'] == '<':
            # left align, pad with spaces on right
            val = val.ljust(f['tam'], f['pad'])[:f['tam']]
        elif f['align'] == '0':
            # right align, pad with zeros on left
            if f['tipo'] == 'N' and len(val) < f['tam']:
                try:
                    vf = float(val) if '.' in val else float(val.replace(',', '.'))
                    # assuming numbers have 2 decimals if they are values
                    if f['nome'] in ['Valor NF', 'Valor Deducoes', 'Desc Incondicional', 'Desc Condicionado', 'Base Calculo', 'PIS', 'COFINS', 'INSS', 'IR', 'CSLL', 'Outras Retencoes', 'Valor ISS', 'Aliquota']:
                        val = f"{vf:.2f}"
                except ValueError:
                    pass
            val = val.rjust(f['tam'], f['pad'])[:f['tam']]
        out += val
    return out

class ValidatorCampinas:
    def __init__(self, logger):
        self.logger = logger
        self.errors = []
    
    def add_error(self, n_linha, num_regra, msg_regra, campo, valor):
        self.errors.append({
            "linha": n_linha,
            "regra": num_regra,
            "mensagem": msg_regra,
            "campo": campo,
            "valor": valor
        })
        self.logger.error(f"[LINHA {n_linha}] [REGRA {num_regra}] {campo}: {msg_regra} (Valor: '{valor}')")

    def log_fix(self, n_linha, campo, old_val, new_val):
        self.logger.info(f"[LINHA {n_linha}] [CORRECAO] {campo} alterado de '{old_val}' para '{new_val}')")

    def is_valid_cpf(self, cpf):
        if len(cpf) != 11 or not cpf.isdigit() or cpf == cpf[0] * 11: return False
        try:
            d1 = 11 - (sum(int(cpf[i]) * (10 - i) for i in range(9)) % 11)
            d1 = 0 if d1 >= 10 else d1
            d2 = 11 - (sum(int(cpf[i]) * (11 - i) for i in range(10)) % 11)
            d2 = 0 if d2 >= 10 else d2
            return int(cpf[-2]) == d1 and int(cpf[-1]) == d2
        except: return False

    def is_valid_cnpj(self, cnpj):
        if len(cnpj) != 14 or not cnpj.isdigit() or cnpj == cnpj[0] * 14: return False
        try:
            v1 = [5,4,3,2,9,8,7,6,5,4,3,2]
            d1 = 11 - (sum(int(cnpj[i]) * v1[i] for i in range(12)) % 11)
            d1 = 0 if d1 >= 10 else d1
            v2 = [6] + v1
            d2 = 11 - (sum(int(cnpj[i]) * v2[i] for i in range(13)) % 11)
            d2 = 0 if d2 >= 10 else d2
            return int(cnpj[-2]) == d1 and int(cnpj[-1]) == d2
        except: return False

    def check_rules(self, data, i, mode="validate"):
        # Auto-fixing dictionary
        fixed = {str(k): data[k]['val'] for k in data.keys()}
        
        # Regra 1: Informe o prestador de servicos
        if not data[8]['val']:
            self.add_error(i, 1, "Informe o Prestador de Servicos (CPF/CNPJ vazio)", "CPF_CNPJ", "")
        
        # Regra 3, 4: Data Emissao
        dt_emissao = data[2]['val']
        if not dt_emissao:
            self.add_error(i, 3, "Informe a Data de Emissao", "Data Emissao", "")
        else:
            try:
                dt = datetime.strptime(dt_emissao, "%d/%m/%Y")
                if dt > datetime.now():
                    self.add_error(i, 4, "Data de Emissao maior que o Mes Atual", "Data Emissao", dt_emissao)
            except:
                self.add_error(i, 3, "Data de Emissao no formato incorreto (DD/MM/YYYY)", "Data Emissao", dt_emissao)
                if mode == 'fix':
                    # Attempt simple fix for missing slashes e.g. 14032025 -> 14/03/2025
                    if len(dt_emissao) == 8 and dt_emissao.isdigit():
                        fixed['2'] = f"{dt_emissao[:2]}/{dt_emissao[2:4]}/{dt_emissao[4:]}"
                        self.log_fix(i, 'Data Emissao', dt_emissao, fixed['2'])

        # Regra 6, 7: Data Competencia
        dt_comp = data[3]['val']
        if not dt_comp:
            self.add_error(i, 7, "Informe a data da competencia", "Data Competencia", "")
        else:
            try:
                dt_c = datetime.strptime(dt_comp, "%m/%Y")
            except:
                self.add_error(i, 7, "Data de Competencia invalida (MM/YYYY)", "Data Competencia", dt_comp)
        
        # Regra 8: Numero Doc
        num_doc = data[4]['val']
        if num_doc.startswith('-'):
            self.add_error(i, 8, "Numero da NF menor que 0", "Numero Doc Fiscal", num_doc)

        # Regra 9: Modelo do Doc Fiscal
        mod_doc = data[6]['val']
        valid_mods = ['RD','A','E','A1','A1F','BB','CE','G','AV','RP','OT','R','OM']
        if not mod_doc:
            self.add_error(i, 9, "Informe o modelo do documento fiscal", "Modelo Doc Fiscal", "")
        elif mod_doc not in valid_mods and mod_doc.replace(' ','') not in valid_mods:
             # Often has trailing spaces
             mod_doc_c = mod_doc.replace(' ','')
             if mod_doc_c in valid_mods:
                 if mode == 'fix': fixed['6'] = mod_doc_c
             else:
                 self.add_error(i, 10, "Documento fiscal invalido", "Modelo Doc Fiscal", mod_doc)

        # Regra 11: NF Avulsa sem imposto
        if fixed.get('6') == 'AV' and data[42]['raw'].replace('0','').replace('.',''):
            self.add_error(i, 11, "Documento Nota Fiscal Avulsa nao pode ter Imposto Retido", "Aliquota", data[42]['val'])
            if mode == 'fix':
                fixed['42'] = "0.00"
                self.log_fix(i, 'Aliquota', data[42]['val'], "0.00")
            
        # Regra 15, 16: CPF/CNPJ Valido (considering rule 7: Nacional)
        tp_prest = data[7]['val']
        cpf = str(data[8]['raw']) # use raw for size tracking zeros
        if tp_prest == '1': # Nacional
            if len(data[8]['val']) == 0:
                self.add_error(i, 15, "Informe CPF/CNPJ do prestador", "CPF_CNPJ", "")
            else:
                c = cpf.strip().lstrip('0')
                if len(c) > 11:
                    if not self.is_valid_cnpj(c.zfill(14)):
                        self.add_error(i, 16, "CPF ou CNPJ do prestador invalido", "CPF_CNPJ", c)
                    elif mode == 'fix' and len(c) < 14:
                        fixed['8'] = c.zfill(14)
                else:
                    if not self.is_valid_cpf(c.zfill(11)):
                        self.add_error(i, 16, "CPF ou CNPJ do prestador invalido", "CPF_CNPJ", c)
                    elif mode == 'fix' and len(c) < 11:
                        fixed['8'] = c.zfill(11)
        elif tp_prest == '2': # Exterior
            if cpf.strip() != '0' * len(cpf.strip()) and cpf.strip() != '':
                self.add_error(i, 18, "Para prestador Exterior não existe CPF/CNPJ (deve ser zeros)", "CPF_CNPJ", cpf)
                if mode == 'fix': fixed['8'] = "00000000000000"
        
        # Rule 17: Nome Razao
        if not data[10]['val']:
             self.add_error(i, 17, "Informe Nome/Razao social", "Nome Razao Social", "")

        # Regra 12, 14: Relacao Modelo e PF/PJ
        is_pf = len(cpf.strip().lstrip('0')) <= 11 and len(cpf.strip().lstrip('0')) > 0
        if fixed.get('6') == 'R' and not is_pf:
            self.add_error(i, 12, "Recibo/RPA somente para Prestador de Servicos Pessoa Fisica", "Modelo Doc Fiscal", fixed['6'])
        if is_pf and fixed.get('6') not in ['R', 'AV']:
            self.add_error(i, 14, "Pessoa Fisica pode utilizar somente os Documentos: R ou AV", "Modelo Doc Fiscal", fixed['6'])

        # Regras 22, 23: UF e Cidade preenchidos para Nacional
        if tp_prest == '1':
            if not data[21]['val']: self.add_error(i, 22, "UF do prestador deve ser preenchido para prestador nacional", "UF", "")
            if not data[23]['val']: self.add_error(i, 23, "Cidade do prestador deve ser preenchido para prestador nacional", "Cidade", "")

        # Regras 28 a 32 e 39, 41: Retencoes e Valores
        val_nf = float(data[43]['val']) if data[43]['val'] else 0.0
        val_bc = float(data[47]['val']) if data[47]['val'] else 0.0
        val_ded = float(data[44]['val']) if data[44]['val'] else 0.0
        val_desc_inc = float(data[45]['val']) if data[45]['val'] else 0.0
        
        if val_nf <= 0:
            self.add_error(i, 29, "Informe o Valor dos servicos da NF (Deve ser maior que 0)", "Valor NF", str(val_nf))
            
        if val_nf == 0.0 and (float(data[42]['val']) if data[42]['val'] else 0) > 0:
            self.add_error(i, 32, "Aliquota de Retencao na Fonte somente sobre Valor de Servicos maior que 0", "Aliquota", data[42]['val'])

        if data[39]['val'] and (float(data[42]['val']) if data[42]['val'] else 0) > 0:
            self.add_error(i, 41, "Informe o campo Motivo nao retencao somente para NF nao retidas (Aliquota=0)", "Motivo Nao Retencao", data[39]['val'])

        # Regra 61: Valor deducoes + desc incondicionado > valor_nf
        if (val_ded + val_desc_inc) > val_nf:
            self.add_error(i, 61, "O somatorio das deducoes e desconto incondicionado maior que valor do servico", "Deducoes/Descontos", f"{val_ded}+{val_desc_inc}")

        # Regra 63, 64: Base de Calculo
        if val_bc <= 0 and val_nf > 0:
             self.add_error(i, 63, "Informe o valor da base de calculo", "Base Calculo", "0")
        if val_bc > val_nf:
             self.add_error(i, 64, "Base de calculo maior que o valor do servico", "Base Calculo", str(val_bc))

        # Regras 42 a 53: Local de Prestacao (LOC / EXT / VIR)
        local_prest = data[27]['val']
        if local_prest == 'LOC':
             if data[28]['val'] == '9999999': self.add_error(i, 42, "Municipio da prestacao deve ser preenchido (Local = LOC)", "Cod Munic Prestacao", data[28]['val'])
             if not data[29]['val']: self.add_error(i, 44, "UF da prestacao deve ser preenchido", "UF Prestacao", "")
        elif local_prest == 'EXT':
             if not data[30]['val']: self.add_error(i, 45, "Municipio exterior prestacao deve ser preenchido", "Munic Exterior", "")
             if not data[31]['val']: self.add_error(i, 46, "Estado exterior prestacao deve ser preenchido", "Estado Exterior", "")
             if not data[32]['val']: self.add_error(i, 47, "Pais da prestacao deve ser preenchido", "Pais Prestacao", "")

        local_res = data[33]['val']
        if local_res == 'BRA':
             if data[34]['val'] == '9999999': self.add_error(i, 48, "Cod Munic Resultado invalido para Brasil", "Cod Munic Resultado", "9999999")
             if not data[35]['val']: self.add_error(i, 50, "UF do resultado deve ser preenchido para BRA", "UF Resultado", "")
        elif local_res == 'EXT':
             if not data[36]['val']: self.add_error(i, 51, "Municipio exterior resultado obrigatorio", "Munic Ext Result", "")
             if not data[37]['val']: self.add_error(i, 52, "Estado exterior resultado obrigatorio", "Est Ext Result", "")
             if not data[38]['val']: self.add_error(i, 53, "Pais resultado obrigatorio", "Pais Result", "")

        # Regras 65 e 66: Exigibilidade e NAP
        exig = data[40]['val']
        tipo_rec = data[41]['val']
        if exig in ['3', '4', '5', '6', '7']:
             if tipo_rec != 'NAP':
                 self.add_error(i, 66, "Tipo de recolhimento deve ser NAP para a exigibilidade informada", "Tipo Recolhimento", tipo_rec)
                 if mode == 'fix': fixed['41'] = 'NAP'
             if (float(data[54]['val']) if data[54]['val'] else 0) > 0:
                 self.add_error(i, 65, "Valor do ISS deve ser 0 para NAP ou exigibilidade isenta/suspensa", "Valor ISS", data[54]['val'])
                 if mode == 'fix': fixed['54'] = "0.00"

        # Required fields according to layout (S)
        for t in LAYOUT_T:
            if t['obrig'] == 'S' and not data[t['num']]['val']:
                # Skip already handled
                if t['num'] not in [2, 3, 4, 8, 10]:
                    if mode == 'fix' and t['tipo'] == 'N':
                         fixed[str(t['num'])] = "0"
                    else:
                         self.add_error(i, 999, f"Campo obrigatorio nao preenchido: {t['nome']}", t['nome'], "")

        return fixed

def validar_linhas(linhas, mode='validate'):
    # Logger para manter compatibilidade, mas a API consome as vars
    logger = logging.getLogger("CampinasAPI")
    logger.handlers.clear()
    logger.addHandler(logging.NullHandler())
    
    val_eng = ValidatorCampinas(logger)
    
    if not linhas:
         return {"sucesso": False, "ocorrencias": [{"linha": 0, "campo": "Arquivo", "regra": 0, "mensagem": "Arquivo vazio", "valor": ""}], "total_linhas": 0}

    header_data = None
    if linhas[0].startswith('H'):
         header_data = {
             "1": linhas[0][0:1],
             "2": linhas[0][1:31].strip()
         }
    else:
         return {"sucesso": False, "ocorrencias": [{"linha": 1, "campo": "Header", "regra": 0, "mensagem": "Arquivo sem Header (H) valido na primeira linha", "valor": ""}], "total_linhas": len(linhas)}

    has_error = False
    for i, linha in enumerate(linhas[1:], 2):
        if not linha: continue
        if not linha.startswith('T'):
             val_eng.add_error(i, 0, "Linha de detalhe nao inicia com T", "Identificacao", linha[:1])
             continue

        if len(linha) < 2955:
            linha = linha.ljust(2955, " ")
            
        data_dict = parse_line(linha, LAYOUT_T)
        val_eng.check_rules(data_dict, i, mode=mode)

    return {
        "sucesso": len(val_eng.errors) == 0,
        "ocorrencias": val_eng.errors,
        "total_linhas": len(linhas)
    }

def validar_arquivo(file_path, mode, out_path=None):
    logger = logging.getLogger("Campinas")
    log_file = file_path + ".log"
    # Overwrite custom handlers to ensure we write to file + console like sigiss toolkit
    logger.handlers.clear()
    
    formatter = logging.Formatter('%(message)s')
    
    fh = logging.FileHandler(log_file, mode='w', encoding='utf-8')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    
    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    
    logger.setLevel(logging.INFO)

    logger.info(f"=== INICIANDO OPERACAO: {mode.upper()} ===")
    logger.info(f"Arquivo: {file_path}")
    
    val_eng = ValidatorCampinas(logger)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        linhas = [l.strip('\r\n') for l in f.readlines()]

    if not linhas:
         logger.error("Arquivo vazio")
         return False

    # Process H
    header_data = None
    if linhas[0].startswith('H'):
         header_data = {
             "1": linhas[0][0:1],
             "2": linhas[0][1:31].strip()
         }
    else:
         logger.error("Arquivo sem Header (H) valido na primeira linha")
         return False

    out_linhas = []
    # format header using simple dict since LAYOUT_H is simple
    if mode == 'fix':
         out_linhas.append(format_line(header_data, LAYOUT_H) + (" "*(2955 - 31)))  # Pad to 2955 if needed, although Header length is 31 by manual. Will let it be 31 or custom.
         # Actually manual says header type is H (1 var) + Inscricao (30 vars) -> total 31 chars. No padding mentioned for header up to 2955.
         out_linhas[0] = out_linhas[0].strip()

    has_error = False
    for i, linha in enumerate(linhas[1:], 2):
        if not linha: continue
        if not linha.startswith('T'):
             val_eng.add_error(i, 0, "Linha de detalhe nao inicia com T", "Identificacao", linha[:1])
             continue

        # Adjust line length padding
        if len(linha) < 2955:
            linha = linha.ljust(2955, " ")
            if mode == 'fix': val_eng.log_fix(i, "Linha", f"Tamanho {len(linha.strip())}", "Tamanho 2955 (Preenchimento)")

        data_dict = parse_line(linha, LAYOUT_T)
        fixed_dict = val_eng.check_rules(data_dict, i, mode=mode)
        
        if len(val_eng.errors) > 0:
            has_error = True

        if mode == 'fix':
            fixed_line = format_line(fixed_dict, LAYOUT_T)
            # Guarantee exactly 2955 chars (if the builder missed something)
            fixed_line = fixed_line.ljust(2955, " ")[:2955]
            out_linhas.append(fixed_line)

    if mode == 'fix' and out_path:
        with open(out_path, 'w', encoding='utf-8') as f:
            if out_linhas:
                # Add Header correctly
                h_line = 'H' + header_data["2"].ljust(30, " ")
                f.write(h_line + "\n")
                for tl in out_linhas[1:]:
                    f.write(tl + "\n")
        logger.info(f"\n[+] Arquivo corrigido gerado com sucesso em: {out_path}")

    if has_error:
         logger.info("\n[!] Validação concluída. Operação registrou erros verificados conforme o manual.")
    else:
         logger.info("\n[+] Validação concluída com SUCESSO. Nenhuma falha estrutural gravíssima detectada.")

    return not has_error


def json_to_txt(json_path, out_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with open(out_path, 'w', encoding='utf-8') as f:
        # Header
        h = format_line({"1": "H", "2": data['inscricao_municipal']}, LAYOUT_H)
        f.write(h + "\n")
        
        for item in data['notas']:
            item["1"] = "T"
            line = format_line(item, LAYOUT_T)
            f.write(line.ljust(2955, " ")[:2955] + "\n")
    print(f"Arquivo gerado: {out_path}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Nota Joeense Integrator - Campinas")
    parser.add_argument("comando", choices=["validar", "corrigir", "gerar"], help="Acao a realizar")
    parser.add_argument("arquivo", help="Caminho do arquivo de entrada (TXT ou JSON)")
    parser.add_argument("--saida", help="Caminho do arquivo de saida", default=None)
    
    args = parser.parse_args()

    if args.comando == 'validar':
        validar_arquivo(args.arquivo, mode='validate')
    elif args.comando == 'corrigir':
        out = args.saida if args.saida else args.arquivo + ".fixed.txt"
        validar_arquivo(args.arquivo, mode='fix', out_path=out)
    elif args.comando == 'gerar':
        out = args.saida if args.saida else args.arquivo.replace('.json', '.txt')
        json_to_txt(args.arquivo, out)
