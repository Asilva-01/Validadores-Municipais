#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerador de Arquivo de Remessa SIGISS/SIGCORP

Este modulo gera arquivos de importacao de servicos tomados no formato
exigido pelo sistema SIGCORP/SIGISS utilizado por diversas prefeituras.

Layout do Arquivo (baseado na documentacao SIGCORP):
- Formato: CSV (campos separados por ponto-e-virgula)
- Encoding: Latin-1 (ISO-8859-1) ou UTF-8 (conforme municipio)
- Ordem dos campos fixa

Campos:
1. CPF ou CNPJ do Prestador de Servicos
2. Numero Inicial da Nota Fiscal (apenas numeros)
3. Serie da Nota Fiscal
4. Sub-Serie da Nota Fiscal
5. Dia de Emissao (DD/MM/AAAA)
6. Codigo do Servico (numerico, 4 digitos)
7. Situacao da Nota Fiscal (t=tributada, r=retida, i=isenta, n=nao tributada)
8. Valor do Servico - Base de Calculo (formato brasileiro: 1.234,56)
9. C.C.M do Tomador (inscricao municipal)
10. Tipo de Nota Fiscal (T=Talao, F=Formulario, J=Jogo Solto, R=Recibo, E=NF-e)
11. Aliquota Super-Simples (formato brasileiro, apenas para optantes pelo Simples)

Uso:
    python gerador_sigiss.py --municipio "Itapira-SP" --input dados.json --output remessa.txt
    python gerador_sigiss.py --municipio "Mogi Mirim-SP" --input dados.json --output remessa.txt --verbose
"""

import argparse
import csv
import json
import logging
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


# Configuracao de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


class CNPJValidator:
    """Validador e formatador de CNPJ."""

    @staticmethod
    def calcular_digito(cnpj_base: str) -> str:
        """
        Calcula os digitos verificadores do CNPJ.

        Args:
            cnpj_base: Os 12 primeiros digitos do CNPJ (somente numeros)

        Returns:
            String com os 2 digitos verificadores
        """
        # Calcula primeiro digito
        multiplicadores1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj_base[i]) * multiplicadores1[i] for i in range(12))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto

        # Calcula segundo digito
        multiplicadores2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj_base[i]) * multiplicadores2[i] for i in range(12))
        soma += digito1 * multiplicadores2[12]
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto

        return f"{digito1}{digito2}"

    @staticmethod
    def validar(cnpj: str) -> bool:
        """
        Valida um CNPJ completo.

        Args:
            cnpj: CNPJ com ou sem formatacao

        Returns:
            True se o CNPJ for valido, False caso contrario
        """
        # Remove caracteres nao numericos
        numeros = re.sub(r'[^0-9]', '', cnpj)

        # Verifica tamanho
        if len(numeros) != 14:
            return False

        # Verifica digitos repetidos (ex: 11111111111111)
        if len(set(numeros)) == 1:
            return False

        # Calcula e verifica digitos verificadores
        digitos_calculados = CNPJValidator.calcular_digito(numeros[:12])
        return numeros[12:14] == digitos_calculados

    @staticmethod
    def formatar(cnpj: str) -> str:
        """
        Formata o CNPJ no padrao ##.###.###/####-##.

        Args:
            cnpj: CNPJ com ou sem formatacao

        Returns:
            CNPJ formatado
        """
        numeros = re.sub(r'[^0-9]', '', cnpj)
        if len(numeros) != 14:
            return cnpj
        return f"{numeros[:2]}.{numeros[2:5]}.{numeros[5:8]}/{numeros[8:12]}-{numeros[12:]}"

    @staticmethod
    def somente_numeros(cnpj: str) -> str:
        """Retorna apenas os numeros do CNPJ."""
        return re.sub(r'[^0-9]', '', cnpj)


class CPFValidator:
    """Validador e formatador de CPF."""

    @staticmethod
    def calcular_digito(cpf_base: str) -> str:
        """
        Calcula os digitos verificadores do CPF.

        Args:
            cpf_base: Os 9 primeiros digitos do CPF (somente numeros)

        Returns:
            String com os 2 digitos verificadores
        """
        # Calcula primeiro digito
        soma = sum(int(cpf_base[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto

        # Calcula segundo digito
        soma = sum(int(cpf_base[i]) * (11 - i) for i in range(9))
        soma += digito1 * 2
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto

        return f"{digito1}{digito2}"

    @staticmethod
    def validar(cpf: str) -> bool:
        """
        Valida um CPF completo.

        Args:
            cpf: CPF com ou sem formatacao

        Returns:
            True se o CPF for valido, False caso contrario
        """
        numeros = re.sub(r'[^0-9]', '', cpf)

        if len(numeros) != 11:
            return False

        # Verifica digitos repetidos
        if len(set(numeros)) == 1:
            return False

        digitos_calculados = CPFValidator.calcular_digito(numeros[:9])
        return numeros[9:11] == digitos_calculados

    @staticmethod
    def formatar(cpf: str) -> str:
        """
        Formata o CPF no padrao ###.###.###-##.

        Args:
            cpf: CPF com ou sem formatacao

        Returns:
            CPF formatado
        """
        numeros = re.sub(r'[^0-9]', '', cpf)
        if len(numeros) != 11:
            return cpf
        return f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"

    @staticmethod
    def somente_numeros(cpf: str) -> str:
        """Retorna apenas os numeros do CPF."""
        return re.sub(r'[^0-9]', '', cpf)


class GeradorSIGISS:
    """
    Gerador de arquivo de remessa no formato SIGISS/SIGCORP.

    Esta classe e responsavel por:
    - Carregar configuracoes do municipio
    - Validar dados de entrada
    - Gerar arquivo no formato correto
    - Aplicar regras especificas por municipio
    """

    # Posicoes dos campos no layout
    CAMPOS_LAYOUT = [
        "cpf_cnpj_prestador",  # Campo 1
        "numero_nota",         # Campo 2
        "serie_nota",          # Campo 3
        "subsérie_nota",       # Campo 4
        "dia_emissao",         # Campo 5
        "codigo_servico",      # Campo 6
        "situacao_nota",       # Campo 7
        "valor_servico",       # Campo 8
        "ccm_tomador",         # Campo 9
        "tipo_nota",           # Campo 10
        "aliquota_simples"     # Campo 11
    ]

    # Mapeamento de situacoes
    SITUACOES = {
        't': 'Tributada',
        'r': 'Retida',
        'i': 'Isenta',
        'n': 'Nao Tributada'
    }

    # Mapeamento de tipos de nota
    TIPOS_NOTA = {
        'T': 'Talao',
        'F': 'Formulario',
        'J': 'Jogo Solto',
        'R': 'Recibo',
        'E': 'NFe'
    }

    def __init__(self, municipio: str, config_path: Optional[str] = None):
        """
        Inicializa o gerador com as configuracoes do municipio.

        Args:
            municipio: Nome do municipio (ex: "Itapira-SP")
            config_path: Caminho para o arquivo de configuracao JSON
                         (padrao: municipios_config.json no mesmo diretorio)

        Raises:
            ValueError: Se o municipio nao for encontrado na configuracao
            FileNotFoundError: Se o arquivo de configuracao nao existir
        """
        self.municipio_nome = municipio
        self.config = self._carregar_configuracao(config_path)

        if municipio not in self.config.get('municipios', {}):
            municipios_disponiveis = list(self.config.get('municipios', {}).keys())
            raise ValueError(
                f"Municipio '{municipio}' nao encontrado na configuracao. "
                f"Municipios disponiveis: {', '.join(municipios_disponiveis)}"
            )

        self.mun_config = self.config['municipios'][municipio]
        logger.info(f"Gerador inicializado para: {municipio}")

    def _carregar_configuracao(self, config_path: Optional[str]) -> Dict:
        """
        Carrega o arquivo de configuracao JSON.

        Args:
            config_path: Caminho para o arquivo JSON

        Returns:
            Dicionario com as configuracoes
        """
        if config_path is None:
            # Procura no mesmo diretorio do script
            script_dir = Path(__file__).parent
            config_path = script_dir / "municipios_config.json"

        config_file = Path(config_path)

        if not config_file.exists():
            raise FileNotFoundError(
                f"Arquivo de configuracao nao encontrado: {config_path}"
            )

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Erro ao parsear arquivo JSON: {e}")

    def _validar_documento(self, documento: str) -> Tuple[bool, str, str]:
        """
        Valida se o documento e CPF ou CNPJ valido.

        Args:
            documento: Numero do documento (CPF ou CNPJ)

        Returns:
            Tupla: (valido, tipo, documento_limpo)
        """
        numeros = re.sub(r'[^0-9]', '', documento)

        if len(numeros) == 11:
            if CPFValidator.validar(numeros):
                return True, 'CPF', numeros
            return False, 'CPF', numeros
        elif len(numeros) == 14:
            if CNPJValidator.validar(numeros):
                return True, 'CNPJ', numeros
            return False, 'CNPJ', numeros
        else:
            return False, 'INVALIDO', numeros

    def _validar_campo(self, campo: str, valor: Any, linha: int) -> List[str]:
        """
        Valida um campo especifico conforme regras do layout.

        Args:
            campo: Nome do campo
            valor: Valor do campo
            linha: Numero da linha (para mensagens de erro)

        Returns:
            Lista de erros encontrados
        """
        erros = []

        # Campo 1: CPF/CNPJ do Prestador (obrigatorio)
        if campo == "cpf_cnpj_prestador":
            if not valor or str(valor).strip() == '':
                erros.append(f"Linha {linha}: CPF/CNPJ do prestador eh obrigatorio")
            else:
                valido, tipo, limpo = self._validar_documento(str(valor))
                if not valido:
                    erros.append(f"Linha {linha}: CPF/CNPJ do prestador invalido: {valor}")

        # Campo 2: Numero da Nota (obrigatorio, apenas numeros)
        elif campo == "numero_nota":
            if not valor or str(valor).strip() == '':
                erros.append(f"Linha {linha}: Numero da nota eh obrigatorio")
            else:
                if not re.match(r'^\d+$', str(valor)):
                    erros.append(f"Linha {linha}: Numero da nota deve conter apenas numeros: {valor}")

        # Campo 5: Dia de Emissao (formato DD/MM/AAAA)
        elif campo == "dia_emissao":
            if valor and str(valor).strip() != '':
                try:
                    datetime.strptime(str(valor), '%d/%m/%Y')
                except ValueError:
                    erros.append(f"Linha {linha}: Data de emissao invalida (use DD/MM/AAAA): {valor}")

        # Campo 6: Codigo do Servico (obrigatorio, numerico)
        elif campo == "codigo_servico":
            obrigatorio = self.mun_config.get('codigos_servico', {}).get('obrigatorio', True)
            if obrigatorio and (not valor or str(valor).strip() == ''):
                erros.append(f"Linha {linha}: Codigo do servico eh obrigatorio")
            elif valor and not re.match(r'^\d{1,4}$', str(valor)):
                erros.append(f"Linha {linha}: Codigo do servico deve ser numerico com ate 4 digitos: {valor}")

        # Campo 7: Situacao da Nota (obrigatorio, valores validos)
        elif campo == "situacao_nota":
            if not valor or str(valor).strip() == '':
                erros.append(f"Linha {linha}: Situacao da nota eh obrigatoria")
            else:
                situacoes_permitidas = self.mun_config.get('situacoes_permitidas', ['t', 'r', 'i', 'n'])
                if str(valor).lower() not in situacoes_permitidas:
                    erros.append(f"Linha {linha}: Situacao invalida. Valores permitidos: {', '.join(situacoes_permitidas)}. Valor: {valor}")

        # Campo 8: Valor do Servico (obrigatorio, formato brasileiro)
        elif campo == "valor_servico":
            if not valor or str(valor).strip() == '':
                erros.append(f"Linha {linha}: Valor do servico eh obrigatorio")
            else:
                valor_str = str(valor).strip()
                # Tenta converter valor numerico (aceita varios formatos)
                try:
                    # Se for numero Python (ex: 2500.50), converte
                    if isinstance(valor, (int, float)):
                        # Valor numerico valido
                        pass
                    else:
                        # String - remove separadores de milhar e converte
                        # Formatos aceitos: 2500,50 | 2.500,50 | 2500.50 | 2500
                        valor_limpo = valor_str.replace('.', '').replace(',', '.')
                        v = float(valor_limpo)
                        if v < 0:
                            erros.append(f"Linha {linha}: Valor do servico deve ser positivo: {valor}")
                except ValueError:
                    erros.append(f"Linha {linha}: Valor do servico invalido: {valor}")

        # Campo 9: CCM do Tomador
        elif campo == "ccm_tomador":
            campos_obrigatorios = self.mun_config.get('campos_obrigatorios', [])
            if "ccm_tomador" in campos_obrigatorios:
                if not valor or str(valor).strip() == '':
                    erros.append(f"Linha {linha}: CCM do tomador eh obrigatorio para este municipio")

        # Campo 10: Tipo de Nota
        elif campo == "tipo_nota":
            campos_obrigatorios = self.mun_config.get('campos_obrigatorios', [])
            if valor and str(valor).strip() != '':
                tipos_permitidos = self.mun_config.get('tipos_nota_permitidos', ['T', 'F', 'J', 'R', 'E'])
                if str(valor).upper() not in tipos_permitidos:
                    erros.append(f"Linha {linha}: Tipo de nota invalido. Valores permitidos: {', '.join(tipos_permitidos)}: {valor}")
            elif "tipo_nota" in campos_obrigatorios:
                erros.append(f"Linha {linha}: Tipo de nota eh obrigatorio para este municipio")

        # Campo 11: Aliquota Simples (opcional, formato brasileiro)
        elif campo == "aliquota_simples":
            if valor and str(valor).strip() != '':
                try:
                    valor_float = float(str(valor).replace('.', '').replace(',', '.'))
                    aliquotas = self.mun_config.get('aliquotas', {})
                    minima = aliquotas.get('minima', 0)
                    maxima = aliquotas.get('maxima', 100)
                    if valor_float < minima or valor_float > maxima:
                        erros.append(f"Linha {linha}: Aliquota fora do intervalo permitido ({minima}% - {maxima}%): {valor}")
                except ValueError:
                    erros.append(f"Linha {linha}: Aliquota invalida: {valor}")

        return erros

    def _formatar_valor(self, valor: Any, campo: str) -> str:
        """
        Formata o valor do campo conforme regras do layout.

        Args:
            valor: Valor original
            campo: Nome do campo

        Returns:
            String formatada
        """
        if valor is None:
            return ''

        valor_str = str(valor).strip()

        # Campo 8 e 11: Valores - garante formato com virgula decimal
        if campo in ["valor_servico", "aliquota_simples"]:
            if valor_str:
                # Se ja estiver formatado brasileiro (com virgula), mantem
                if ',' in valor_str:
                    return valor_str.replace('.', '')  # Remove separador de milhar
                # Se for formato americano ou numero puro
                try:
                    num = float(valor_str)
                    return f"{num:,.2f}".replace('.', '#').replace(',', '.').replace('#', ',')
                except ValueError:
                    return valor_str
            return ''

        return valor_str

    def validar_dados(self, dados: List[Dict[str, Any]]) -> Tuple[bool, List[str]]:
        """
        Valida todos os dados antes da geracao.

        Args:
            dados: Lista de dicionarios com os registros

        Returns:
            Tupla: (valido, lista_de_erros)
        """
        erros = []

        if not dados:
            return False, ["Nenhum registro fornecido para geracao"]

        campos_obrigatorios = self.mun_config.get('campos_obrigatorios', [])

        for i, registro in enumerate(dados, start=1):
            # Verifica campos obrigatorios definidos no config
            for campo_obrigatorio in campos_obrigatorios:
                if campo_obrigatorio not in registro or not str(registro.get(campo_obrigatorio, '')).strip():
                    erros.append(f"Linha {i}: Campo obrigatorio '{campo_obrigatorio}' nao fornecido")

            # Valida cada campo do registro
            for campo in self.CAMPOS_LAYOUT:
                valor = registro.get(campo)
                erros_campo = self._validar_campo(campo, valor, i)
                erros.extend(erros_campo)

        return len(erros) == 0, erros

    def gerar(self, dados: List[Dict[str, Any]], output_path: str) -> bool:
        """
        Gera o arquivo de remessa no formato SIGISS.

        Args:
            dados: Lista de dicionarios com os registros
            output_path: Caminho do arquivo de saida

        Returns:
            True se o arquivo foi gerado com sucesso, False caso contrario

        Raises:
            ValueError: Se houver erros de validacao nos dados
        """
        # Valida os dados
        valido, erros = self.validar_dados(dados)
        if not valido:
            for erro in erros:
                logger.error(erro)
            raise ValueError(f"Validacao falhou com {len(erros)} erro(s). Verifique os logs.")

        # Obtem configuracoes de encoding e separador
        encoding = self.mun_config.get('configuracoes', {}).get('encoding', 'latin-1')
        separador = self.mun_config.get('configuracoes', {}).get('separador', ';')

        logger.info(f"Gerando arquivo: {output_path}")
        logger.info(f"Encoding: {encoding}, Separador: '{separador}'")
        logger.info(f"Total de registros: {len(dados)}")

        try:
            with open(output_path, 'w', encoding=encoding, newline='') as f:
                writer = csv.writer(f, delimiter=separador, lineterminator='\r\n')

                linhas_geradas = 0
                for registro in dados:
                    linha = []
                    for campo in self.CAMPOS_LAYOUT:
                        valor = registro.get(campo, '')
                        valor_formatado = self._formatar_valor(valor, campo)
                        linha.append(valor_formatado)

                    writer.writerow(linha)
                    linhas_geradas += 1

            logger.info(f"Arquivo gerado com sucesso: {output_path}")
            logger.info(f"Total de linhas escritas: {linhas_geradas}")
            return True

        except Exception as e:
            logger.error(f"Erro ao gerar arquivo: {e}")
            raise


def carregar_dados_json(input_path: str) -> List[Dict[str, Any]]:
    """
    Carrega dados de entrada a partir de um arquivo JSON.

    Estrutura esperada:
    [
        {
            "cpf_cnpj_prestador": "12345678000195",
            "numero_nota": "1234",
            "serie_nota": "1",
            "subsérie_nota": "0",
            "dia_emissao": "15/03/2026",
            "codigo_servico": "1701",
            "situacao_nota": "t",
            "valor_servico": "1000,00",
            "ccm_tomador": "123456789",
            "tipo_nota": "T",
            "aliquota_simples": "3,00"
        },
        ...
    ]

    Args:
        input_path: Caminho para o arquivo JSON

    Returns:
        Lista de dicionarios com os dados
    """
    input_file = Path(input_path)

    if not input_file.exists():
        raise FileNotFoundError(f"Arquivo de entrada nao encontrado: {input_path}")

    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        if not isinstance(dados, list):
            raise ValueError("Arquivo JSON deve conter uma lista de registros")

        return dados
    except json.JSONDecodeError as e:
        raise ValueError(f"Erro ao parsear arquivo JSON: {e}")


def main():
    """Funcao principal de execucao via linha de comando."""
    parser = argparse.ArgumentParser(
        description="Gerador de arquivo de remessa SIGISS/SIGCORP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  %(prog)s --municipio "Itapira-SP" --input dados.json --output remessa.txt
  %(prog)s --municipio "Chapeco-SC" --input dados.json --output remessa.txt --verbose
  %(prog)s --municipio "Mogi Mirim-SP" --input dados.json --output remessa.txt --config meu_config.json
        """
    )

    parser.add_argument(
        '--municipio', '-m',
        required=True,
        help='Nome do municipio (ex: "Itapira-SP", "Chapeco-SC")'
    )

    parser.add_argument(
        '--input', '-i',
        required=True,
        help='Caminho do arquivo JSON de entrada com os dados'
    )

    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Caminho do arquivo de saida (remessa)'
    )

    parser.add_argument(
        '--config', '-c',
        default=None,
        help='Caminho para o arquivo de configuracao JSON (padrao: municipios_config.json)'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Ativa saida detalhada (verbose)'
    )

    args = parser.parse_args()

    # Configura nivel de log
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        # Carrega dados de entrada
        logger.info(f"Carregando dados de: {args.input}")
        dados = carregar_dados_json(args.input)

        # Inicializa gerador
        gerador = GeradorSIGISS(
            municipio=args.municipio,
            config_path=args.config
        )

        # Gera arquivo
        gerador.gerar(dados, args.output)

        logger.info("Processo concluido com sucesso!")
        sys.exit(0)

    except FileNotFoundError as e:
        logger.error(f"Arquivo nao encontrado: {e}")
        sys.exit(1)
    except ValueError as e:
        logger.error(f"Erro de validacao: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erro inesperado: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
