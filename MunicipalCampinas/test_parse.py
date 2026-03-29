LAYOUT_T = [
    {"num": 1, "nome": "Identificacao", "tipo": "A", "pi": 1, "pf": 1, "tam": 1, "obrig": "S"},
    {"num": 2, "nome": "Data Emissao", "tipo": "D", "pi": 2, "pf": 11, "tam": 10, "obrig": "S"},
    {"num": 3, "nome": "Data Competencia", "tipo": "D", "pi": 12, "pf": 18, "tam": 7, "obrig": "S"},
    {"num": 4, "nome": "Numero Doc Fiscal", "tipo": "N", "pi": 19, "pf": 33, "tam": 15, "obrig": "S"},
    {"num": 5, "nome": "Serie Doc Fiscal", "tipo": "A", "pi": 34, "pf": 38, "tam": 5, "obrig": "N"},
    {"num": 6, "nome": "Modelo Doc Fiscal", "tipo": "A", "pi": 39, "pf": 40, "tam": 2, "obrig": "S"},
    {"num": 7, "nome": "Tipo Prestador", "tipo": "N", "pi": 41, "pf": 41, "tam": 1, "obrig": "S"},
    {"num": 8, "nome": "CPF/CNPJ", "tipo": "N", "pi": 42, "pf": 55, "tam": 14, "obrig": "S"},
    {"num": 9, "nome": "ID Exterior", "tipo": "N", "pi": 56, "pf": 75, "tam": 20, "obrig": "N"},
    {"num": 10, "nome": "Nome/Razao Social", "tipo": "A", "pi": 76, "pf": 225, "tam": 150, "obrig": "S"},
    {"num": 11, "nome": "Cod Municipio Prestador", "tipo": "A", "pi": 226, "pf": 232, "tam": 7, "obrig": "S"},
    {"num": 12, "nome": "Optante Simples", "tipo": "A", "pi": 233, "pf": 233, "tam": 1, "obrig": "S"},
    {"num": 13, "nome": "MEI", "tipo": "A", "pi": 234, "pf": 234, "tam": 1, "obrig": "S"},
    {"num": 14, "nome": "Estabelecido Municipio", "tipo": "A", "pi": 235, "pf": 235, "tam": 1, "obrig": "S"},
    {"num": 15, "nome": "CEP", "tipo": "N", "pi": 236, "pf": 243, "tam": 8, "obrig": "S"},
    {"num": 16, "nome": "Tipo Logradouro", "tipo": "A", "pi": 244, "pf": 268, "tam": 25, "obrig": "S"},
    {"num": 17, "nome": "Nome Logradouro", "tipo": "A", "pi": 269, "pf": 318, "tam": 50, "obrig": "N"},
    {"num": 18, "nome": "Numero Logradouro", "tipo": "N", "pi": 319, "pf": 328, "tam": 10, "obrig": "N"}, 
    {"num": 19, "nome": "Complemento", "tipo": "A", "pi": 329, "pf": 388, "tam": 60, "obrig": "N"},
    {"num": 20, "nome": "Bairro", "tipo": "A", "pi": 389, "pf": 448, "tam": 60, "obrig": "N"},
    {"num": 21, "nome": "UF", "tipo": "A", "pi": 449, "pf": 450, "tam": 2, "obrig": "S"},
    {"num": 22, "nome": "Pais", "tipo": "N", "pi": 451, "pf": 454, "tam": 4, "obrig": "S"},
    {"num": 23, "nome": "Cidade", "tipo": "A", "pi": 455, "pf": 504, "tam": 50, "obrig": "S"},
    {"num": 24, "nome": "Cod Servico", "tipo": "N", "pi": 505, "pf": 509, "tam": 5, "obrig": "S"},
    {"num": 25, "nome": "Cod Atividade CNAE", "tipo": "N", "pi": 510, "pf": 518, "tam": 9, "obrig": "S"},
    {"num": 26, "nome": "Cod Obra", "tipo": "N", "pi": 519, "pf": 533, "tam": 15, "obrig": "N"},
    {"num": 27, "nome": "Local Prestacao", "tipo": "A", "pi": 534, "pf": 536, "tam": 3, "obrig": "S"},
    {"num": 28, "nome": "Cod Munic Prestacao", "tipo": "A", "pi": 537, "pf": 543, "tam": 7, "obrig": "N"},
    {"num": 29, "nome": "UF Prestacao", "tipo": "A", "pi": 544, "pf": 545, "tam": 2, "obrig": "N"},
    {"num": 30, "nome": "Munic Exterior", "tipo": "A", "pi": 546, "pf": 595, "tam": 50, "obrig": "N"},
    {"num": 31, "nome": "Estado Exterior", "tipo": "A", "pi": 596, "pf": 645, "tam": 50, "obrig": "N"},
    {"num": 32, "nome": "Pais Prestacao", "tipo": "N", "pi": 646, "pf": 649, "tam": 4, "obrig": "N"},
    {"num": 33, "nome": "Local Resultado", "tipo": "A", "pi": 650, "pf": 652, "tam": 3, "obrig": "N"},
    {"num": 34, "nome": "Cod Munic Resultado", "tipo": "A", "pi": 653, "pf": 659, "tam": 7, "obrig": "N"},
    {"num": 35, "nome": "UF Resultado", "tipo": "A", "pi": 660, "pf": 661, "tam": 2, "obrig": "N"},
    {"num": 36, "nome": "Munic Ext Result", "tipo": "A", "pi": 662, "pf": 711, "tam": 50, "obrig": "N"},
    {"num": 37, "nome": "Est Ext Result", "tipo": "A", "pi": 712, "pf": 761, "tam": 50, "obrig": "N"},
    {"num": 38, "nome": "Pais Result", "tipo": "N", "pi": 762, "pf": 765, "tam": 4, "obrig": "N"},
    {"num": 39, "nome": "Motivo Não Retencao", "tipo": "A", "pi": 766, "pf": 766, "tam": 1, "obrig": "N"},
    {"num": 40, "nome": "Exigibilidade", "tipo": "N", "pi": 767, "pf": 767, "tam": 1, "obrig": "S"},
    {"num": 41, "nome": "Tipo Recolhimento", "tipo": "A", "pi": 768, "pf": 770, "tam": 3, "obrig": "S"},
    {"num": 42, "nome": "Aliquota", "tipo": "N", "pi": 771, "pf": 775, "tam": 5, "obrig": "N"},
]

def parse():
    with open('4901662_ST_024_BR13_CAMPINAS_042025_1.txt', 'r', encoding='utf-8') as f:
        linha = f.readlines()[1].strip('\r\n')
    
    for f in LAYOUT_T:
        pi = f['pi'] - 1
        pf = f['pf']
        print(f"{f['num']} {f['nome']}: [{linha[pi:pf]}] len={len(linha[pi:pf])}")

parse()
