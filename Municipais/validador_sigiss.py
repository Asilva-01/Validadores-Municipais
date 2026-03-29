#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Validador de Arquivo SIGISS/SIGCORP

Este modulo valida arquivos de importacao de servicos tomados no formato
exigido pelo sistema SIGCORP/SIGISS utilizado por diversas prefeituras.

Suporta validacao generica (aplicavel a qualquer prefeitura SIGCORP) e
validacao especifica por municipio, com regras customizadas.

Uso:
    python validador_sigiss.py --municipio "Itapira-SP" --arquivo remessa.txt
    python validador_sigiss.py --arquivo remessa.txt --verbose
    python validador_sigiss.py --municipio "Chapeco-SC" --arquivo remessa.txt --output validacao.log
"""

import argparse
import csv
import json
import logging
import os
import re
import sys
from datetime import datetime
from enum import Enum
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


class NivelValidacao(Enum):
    """Niveis de severidade para problemas encontrados."""
    ERRO = "ERRO"
    AVISO = "AVISO"
    INFO = "INFO"


class ResultadoValidacao:
    """Representa o resultado de uma validacao individual."""

    def __init__(self):
        self.problemas: List[Dict[str, Any]] = []
        self.total_linhas = 0
        self.total_erros = 0
        self.total_avisos = 0
        self.valido = True

    def adicionar_problema(
        self,
        nivel: NivelValidacao,
        linha: int,
        campo: str,
        valor_encontrado: str,
        mensagem: str,
        valor_esperado: str = ""
    ):
        """Adiciona um problema ao resultado."""
        problema = {
            "nivel": nivel.value,
            "linha": linha,
            "campo": campo,
            "valor_encontrado": valor_encontrado,
            "mensagem": mensagem,
            "valor_esperado": valor_esperado
        }
        self.problemas.append(problema)

        if nivel == NivelValidacao.ERRO:
            self.total_erros += 1
            self.valido = False
        elif nivel == NivelValidacao.AVISO:
            self.total_avisos += 1

    def __str__(self) -> str:
        """Retorna representacao string do resultado."""
        status = "VALIDO" if self.valido else "INVALIDO"
        return f"[{status}] Linhas: {self.total_linhas}, Erros: {self.total_erros}, Avisos: {self.total_avisos}"


class CNPJValidator:
    """Validador e formatador de CNPJ."""

    @staticmethod
    def calcular_digito(cnpj_base: str) -> str:
        """Calcula os digitos verificadores do CNPJ."""
        multiplicadores1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj_base[i]) * multiplicadores1[i] for i in range(12))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto

        multiplicadores2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        soma = sum(int(cnpj_base[i]) * multiplicadores2[i] for i in range(12))
        soma += digito1 * multiplicadores2[12]
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto

        return f"{digito1}{digito2}"

    @staticmethod
    def validar(cnpj: str) -> bool:
        """Valida um CNPJ completo."""
        numeros = re.sub(r'[^0-9]', '', cnpj)
        if len(numeros) != 14:
            return False
        if len(set(numeros)) == 1:
            return False
        digitos_calculados = CNPJValidator.calcular_digito(numeros[:12])
        return numeros[12:14] == digitos_calculados


class CPFValidator:
    """Validador e formatador de CPF."""

    @staticmethod
    def calcular_digito(cpf_base: str) -> str:
        """Calcula os digitos verificadores do CPF."""
        soma = sum(int(cpf_base[i]) * (10 - i) for i in range(9))
        resto = soma % 11
        digito1 = 0 if resto < 2 else 11 - resto

        soma = sum(int(cpf_base[i]) * (11 - i) for i in range(9))
        soma += digito1 * 2
        resto = soma % 11
        digito2 = 0 if resto < 2 else 11 - resto

        return f"{digito1}{digito2}"

    @staticmethod
    def validar(cpf: str) -> bool:
        """Valida um CPF completo."""
        numeros = re.sub(r'[^0-9]', '', cpf)
        if len(numeros) != 11:
            return False
        if len(set(numeros)) == 1:
            return False
        digitos_calculados = CPFValidator.calcular_digito(numeros[:9])
        return numeros[9:11] == digitos_calculados


class ValidadorSIGISS:
    """
    Validador de arquivos no formato SIGISS/SIGCORP.

    Esta classe e responsavel por:
    - Carregar configuracoes do municipio (opcional)
    - Validar estrutura do arquivo
    - Validar cada campo conforme regras do layout
    - Validar regras especificas por municipio
    - Gerar relatorio de validacao
    """

    # Posicoes dos campos no layout
    CAMPOS_LAYOUT = [
        "cpf_cnpj_prestador",  # Campo 1
        "numero_nota",         # Campo 2
        "serie_nota",          # Campo 3
        "subserie_nota",       # Campo 4
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

    def __init__(self, municipio: Optional[str] = None, config_path: Optional[str] = None):
        """
        Inicializa o validador.

        Args:
            municipio: Nome do municipio (ex: "Itapira-SP") - opcional
            config_path: Caminho para o arquivo de configuracao JSON
        """
        self.municipio_nome = municipio
        self.mun_config = None
        self.config = None

        if municipio:
            self.config = self._carregar_configuracao(config_path)
            if municipio in self.config.get('municipios', {}):
                self.mun_config = self.config['municipios'][municipio]
                logger.info(f"Validador inicializado com configuracoes para: {municipio}")
            else:
                logger.warning(f"Municipio '{municipio}' nao encontrado. Usando validacao generica.")
        else:
            logger.info("Validador inicializado em modo generico (sem regras especificas)")

    def _carregar_configuracao(self, config_path: Optional[str]) -> Dict:
        """Carrega o arquivo de configuracao JSON."""
        if config_path is None:
            script_dir = Path(__file__).parent
            config_path = script_dir / "municipios_config.json"

        config_file = Path(config_path)

        if not config_file.exists():
            logger.warning(f"Arquivo de configuracao nao encontrado: {config_path}")
            return {"municipios": {}}

        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logger.warning(f"Erro ao parsear arquivo JSON: {e}")
            return {"municipios": {}}

    def _validar_cpf_cnpj(self, documento: str, linha: int) -> Tuple[bool, str, List[Dict]]:
        """Valida CPF ou CNPJ."""
        problemas = []
        numeros = re.sub(r'[^0-9]', '', documento)

        if len(numeros) == 11:
            if CPFValidator.validar(numeros):
                return True, "CPF", []
            else:
                problemas.append({
                    "nivel": NivelValidacao.ERRO,
                    "campo": "cpf_cnpj_prestador",
                    "mensagem": "CPF invalido (digitos verificadores incorretos)",
                    "valor_encontrado": documento
                })
                return False, "CPF", problemas
        elif len(numeros) == 14:
            if CNPJValidator.validar(numeros):
                return True, "CNPJ", []
            else:
                problemas.append({
                    "nivel": NivelValidacao.ERRO,
                    "campo": "cpf_cnpj_prestador",
                    "mensagem": "CNPJ invalido (digitos verificadores incorretos)",
                    "valor_encontrado": documento
                })
                return False, "CNPJ", problemas
        else:
            problemas.append({
                "nivel": NivelValidacao.ERRO,
                "campo": "cpf_cnpj_prestador",
                "mensagem": f"Documento deve ter 11 (CPF) ou 14 (CNPJ) digitos, encontrado: {len(numeros)}",
                "valor_encontrado": documento
            })
            return False, "INVALIDO", problemas

    def _validar_campo_generico(self, campo_idx: int, valor: str, linha: int) -> List[Dict]:
        """
        Valida um campo de forma generica (aplicavel a qualquer SIGCORP).

        Args:
            campo_idx: Indice do campo (0-based)
            valor: Valor do campo
            linha: Numero da linha

        Returns:
            Lista de problemas encontrados
        """
        problemas = []
        nome_campo = self.CAMPOS_LAYOUT[campo_idx]

        # Campo 1: CPF/CNPJ do Prestador
        if campo_idx == 0:
            if not valor:
                problemas.append({
                    "nivel": NivelValidacao.ERRO,
                    "campo": nome_campo,
                    "mensagem": "CPF/CNPJ do prestador e obrigatorio",
                    "valor_encontrado": valor
                })
            else:
                valido, tipo, probs = self._validar_cpf_cnpj(valor, linha)
                problemas.extend(probs)

        # Campo 2: Numero da Nota
        elif campo_idx == 1:
            if not valor:
                problemas.append({
                    "nivel": NivelValidacao.ERRO,
                    "campo": nome_campo,
                    "mensagem": "Numero da nota e obrigatorio",
                    "valor_encontrado": valor
                })
            elif not re.match(r'^\d+$', valor):
                problemas.append({
                    "nivel": NivelValidacao.ERRO,
                    "campo": nome_campo,
                    "mensagem": "Numero da nota deve conter apenas numeros",
                    "valor_encontrado": valor
                })

        # Campo 5: Dia de Emissao
        elif campo_idx == 4:
            if valor:
                try:
                    datetime.strptime(valor, '%d/%m/%Y')
                except ValueError:
                    problemas.append({
                        "nivel": NivelValidacao.ERRO,
                        "campo": nome_campo,
                        "mensagem": "Data deve estar no formato DD/MM/AAAA",
                        "valor_encontrado": valor
                    })

        # Campo 6: Codigo do Servico
        elif campo_idx == 5:
            if not valor:
                problemas.append({
                    "nivel": NivelValidacao.ERRO,
                    "campo": nome_campo,
                    "mensagem": "Codigo do servico e obrigatorio",
                    "valor_encontrado": valor
                })
            elif not re.match(r'^\d{1,4}$', valor):
                problemas.append({
                    "nivel": NivelValidacao.ERRO,
                    "campo": nome_campo,
                    "mensagem": "Codigo do servico deve ser numerico com ate 4 digitos",
                    "valor_encontrado": valor
                })

        # Campo 7: Situacao da Nota
        elif campo_idx == 6:
            if not valor:
                problemas.append({
                    "nivel": NivelValidacao.ERRO,
                    "campo": nome_campo,
                    "mensagem": "Situacao da nota e obrigatoria",
                    "valor_encontrado": valor
                })
            elif valor.lower() not in self.SITUACOES:
                problemas.append({
                    "nivel": NivelValidacao.ERRO,
                    "campo": nome_campo,
                    "mensagem": f"Situacao invalida. Valores permitidos: {', '.join(self.SITUACOES.keys())}",
                    "valor_encontrado": valor
                })

        # Campo 8: Valor do Servico
        elif campo_idx == 7:
            if not valor:
                problemas.append({
                    "nivel": NivelValidacao.ERRO,
                    "campo": nome_campo,
                    "mensagem": "Valor do servico e obrigatorio",
                    "valor_encontrado": valor
                })
            else:
                valor_str = valor.replace('.', '').replace(',', '.')
                try:
                    v = float(valor_str)
                    if v < 0:
                        problemas.append({
                            "nivel": NivelValidacao.ERRO,
                            "campo": nome_campo,
                            "mensagem": "Valor do servico deve ser positivo",
                            "valor_encontrado": valor
                        })
                except ValueError:
                    problemas.append({
                        "nivel": NivelValidacao.ERRO,
                        "campo": nome_campo,
                        "mensagem": "Valor do servico deve ser numerico (formato: 1.234,56)",
                        "valor_encontrado": valor
                    })

        # Campo 10: Tipo de Nota
        elif campo_idx == 9:
            if valor and valor.upper() not in self.TIPOS_NOTA:
                problemas.append({
                    "nivel": NivelValidacao.ERRO,
                    "campo": nome_campo,
                    "mensagem": f"Tipo de nota invalido. Valores: {', '.join(self.TIPOS_NOTA.keys())}",
                    "valor_encontrado": valor
                })

        # Campo 11: Aliquota Simples
        elif campo_idx == 10:
            if valor:
                valor_str = valor.replace('.', '').replace(',', '.')
                try:
                    v = float(valor_str)
                    if v < 0 or v > 100:
                        problemas.append({
                            "nivel": NivelValidacao.ERRO,
                            "campo": nome_campo,
                            "mensagem": "Aliquota deve estar entre 0 e 100",
                            "valor_encontrado": valor
                        })
                except ValueError:
                    problemas.append({
                        "nivel": NivelValidacao.ERRO,
                        "campo": nome_campo,
                        "mensagem": "Aliquota deve ser numerica",
                        "valor_encontrado": valor
                    })

        return problemas

    def _validar_regras_municipio(self, campos: List[str], linha: int) -> List[Dict]:
        """Aplica regras especificas do municipio."""
        problemas = []

        if not self.mun_config:
            return problemas

        campos_obrigatorios = self.mun_config.get('campos_obrigatorios', [])

        for campo_obrigatorio in campos_obrigatorios:
            if campo_obrigatorio in self.CAMPOS_LAYOUT:
                idx = self.CAMPOS_LAYOUT.index(campo_obrigatorio)
                if idx < len(campos) and not campos[idx].strip():
                    problemas.append({
                        "nivel": NivelValidacao.ERRO,
                        "campo": campo_obrigatorio,
                        "mensagem": f"Campo obrigatorio para este municipio nao preenchido",
                        "valor_encontrado": ""
                    })

        # Valida aliquotas especificas do municipio
        aliquotas = self.mun_config.get('aliquotas', {})
        if aliquotas and len(campos) > 10 and campos[10]:
            valor_str = campos[10].replace('.', '').replace(',', '.')
            try:
                v = float(valor_str)
                minima = aliquotas.get('minima', 0)
                maxima = aliquotas.get('maxima', 100)
                if v < minima or v > maxima:
                    problemas.append({
                        "nivel": NivelValidacao.AVISO,
                        "campo": "aliquota_simples",
                        "mensagem": f"Aliquota fora do intervalo tipico do municipio ({minima}% - {maxima}%)",
                        "valor_encontrado": campos[10]
                    })
            except ValueError:
                pass

        return problemas

    def validar_arquivo(self, arquivo_path: str) -> ResultadoValidacao:
        """
        Valida um arquivo completo.

        Args:
            arquivo_path: Caminho para o arquivo a ser validado

        Returns:
            ResultadoValidacao com todos os problemas encontrados
        """
        resultado = ResultadoValidacao()
        arquivo = Path(arquivo_path)

        if not arquivo.exists():
            resultado.adicionar_problema(
                NivelValidacao.ERRO,
                0,
                "ARQUIVO",
                arquivo_path,
                "Arquivo nao encontrado",
                ""
            )
            return resultado

        # Detecta encoding
        encoding = self._detectar_encoding(arquivo_path)
        logger.debug(f"Encoding detectado: {encoding}")

        # Obtem separador do config ou usa padrao
        separador = ';'
        if self.mun_config:
            separador = self.mun_config.get('configuracoes', {}).get('separador', ';')

        try:
            with open(arquivo_path, 'r', encoding=encoding, newline='') as f:
                reader = csv.reader(f, delimiter=separador)

                for num_linha, campos in enumerate(reader, start=1):
                    resultado.total_linhas += 1

                    # Valida quantidade de campos
                    if len(campos) != len(self.CAMPOS_LAYOUT):
                        resultado.adicionar_problema(
                            NivelValidacao.ERRO,
                            num_linha,
                            "ESTRUTURA",
                            f"{len(campos)} campos",
                            f"Numero incorreto de campos. Esperado: {len(self.CAMPOS_LAYOUT)}",
                            str(len(self.CAMPOS_LAYOUT))
                        )
                        continue

                    # Valida campos genericos
                    for idx, valor in enumerate(campos):
                        problemas = self._validar_campo_generico(idx, valor.strip(), num_linha)
                        for prob in problemas:
                            resultado.adicionar_problema(
                                prob["nivel"],
                                num_linha,
                                prob["campo"],
                                prob["valor_encontrado"],
                                prob["mensagem"],
                                prob.get("valor_esperado", "")
                            )

                    # Valida regras especificas do municipio
                    problemas_mun = self._validar_regras_municipio([c.strip() for c in campos], num_linha)
                    for prob in problemas_mun:
                        resultado.adicionar_problema(
                            prob["nivel"],
                            num_linha,
                            prob["campo"],
                            prob["valor_encontrado"],
                            prob["mensagem"],
                            prob.get("valor_esperado", "")
                        )

        except Exception as e:
            resultado.adicionar_problema(
                NivelValidacao.ERRO,
                0,
                "ARQUIVO",
                "",
                f"Erro ao ler arquivo: {str(e)}",
                ""
            )

        return resultado

    def _detectar_encoding(self, arquivo_path: str) -> str:
        """Tenta detectar o encoding do arquivo."""
        encodings = ['latin-1', 'utf-8', 'iso-8859-1', 'cp1252']

        for enc in encodings:
            try:
                with open(arquivo_path, 'r', encoding=enc) as f:
                    f.read()
                return enc
            except (UnicodeDecodeError, UnicodeError):
                continue

        return 'latin-1'

    def gerar_relatorio(self, resultado: ResultadoValidacao, output_path: Optional[str] = None) -> str:
        """
        Gera relatorio de validacao.

        Args:
            resultado: Resultado da validacao
            output_path: Caminho para salvar o relatorio (opcional)

        Returns:
            String com o relatorio
        """
        linhas = []
        linhas.append("=" * 80)
        linhas.append("RELATORIO DE VALIDACAO SIGISS/SIGCORP")
        linhas.append("=" * 80)
        linhas.append(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        linhas.append(f"Municipio: {self.municipio_nome or 'Generico (sem regras especificas)'}")
        linhas.append("-" * 80)
        linhas.append(f"STATUS: {'VALIDO' if resultado.valido else 'INVALIDO'}")
        linhas.append(f"Total de linhas processadas: {resultado.total_linhas}")
        linhas.append(f"Total de ERROS: {resultado.total_erros}")
        linhas.append(f"Total de AVISOS: {resultado.total_avisos}")
        linhas.append("=" * 80)

        if resultado.problemas:
            linhas.append("")
            linhas.append("DETALHAMENTO DOS PROBLEMAS:")
            linhas.append("-" * 80)

            for prob in resultado.problemas:
                linhas.append(f"")
                linhas.append(f"[{prob['nivel']}] Linha {prob['linha']} - Campo: {prob['campo']}")
                linhas.append(f"  Valor encontrado: '{prob['valor_encontrado']}'")
                linhas.append(f"  Mensagem: {prob['mensagem']}")
                if prob['valor_esperado']:
                    linhas.append(f"  Valor esperado/regra: {prob['valor_esperado']}")

        linhas.append("")
        linhas.append("=" * 80)
        linhas.append("FIM DO RELATORIO")
        linhas.append("=" * 80)

        relatorio = "\n".join(linhas)

        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(relatorio)
            logger.info(f"Relatorio salvo em: {output_path}")

        return relatorio


def main():
    """Funcao principal de execucao via linha de comando."""
    parser = argparse.ArgumentParser(
        description="Validador de arquivos SIGISS/SIGCORP",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemplos de uso:
  %(prog)s --arquivo remessa.txt
  %(prog)s --municipio "Itapira-SP" --arquivo remessa.txt
  %(prog)s --municipio "Chapeco-SC" --arquivo remessa.txt --output validacao.log
  %(prog)s --arquivo remessa.txt --verbose --config meu_config.json
        """
    )

    parser.add_argument(
        '--arquivo', '-a',
        required=True,
        help='Caminho do arquivo a ser validado'
    )

    parser.add_argument(
        '--municipio', '-m',
        default=None,
        help='Nome do municipio para aplicar regras especificas (ex: "Itapira-SP")'
    )

    parser.add_argument(
        '--config', '-c',
        default=None,
        help='Caminho para o arquivo de configuracao JSON'
    )

    parser.add_argument(
        '--output', '-o',
        default=None,
        help='Caminho para salvar o relatorio de validacao'
    )

    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Ativa saida detalhada'
    )

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        validador = ValidadorSIGISS(
            municipio=args.municipio,
            config_path=args.config
        )

        resultado = validador.validar_arquivo(args.arquivo)

        relatorio = validador.gerar_relatorio(resultado, args.output)
        print(relatorio)

        if resultado.valido:
            logger.info("Arquivo validado com sucesso!")
            sys.exit(0)
        else:
            logger.error(f"Validacao falhou com {resultado.total_erros} erro(s)")
            sys.exit(1)

    except Exception as e:
        logger.error(f"Erro durante validacao: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
