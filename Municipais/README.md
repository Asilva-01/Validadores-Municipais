<<<<<<< HEAD
# Validadores-Municipais
Simuladores dos validadores de arquivos obrigações Municipais
=======
# Sistema de Integração SIGISS/SIGCORP - NFS-e

Sistema completo para geração e validação de arquivos de remessa no formato SIGISS (Sistema Integrado de Gerenciamento do ISS) utilizado pelo sistema SIGCORP em diversas prefeituras municipais.

## 📋 Sumário

- [Visão Geral](#visão-geral)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Layout do Arquivo](#layout-do-arquivo)
- [Como Usar o Gerador](#como-usar-o-gerador)
- [Como Usar o Validador](#como-usar-o-validador)
- [Interface Web](#interface-web)
- [Como Adicionar um Novo Município](#como-adicionar-um-novo-município)
- [Descrição dos Campos](#descrição-dos-campos)
- [Exemplos](#exemplos)
- [Tratamento de Erros](#tratamento-de-erros)
- [Municípios Suportados](#municípios-suportados)

## Visão Geral

Este sistema permite:

- **Gerar** arquivos de remessa para importação de serviços tomados no formato SIGISS
- **Validar** arquivos antes do envio, verificando regras genéricas e específicas por município
- **Configurar** regras personalizadas por prefeitura via JSON

O layout do arquivo é baseado na documentação oficial do SIGCORP e utiliza o formato CSV com separador ponto-e-vírgula (`;`).

## Estrutura do Projeto

```
C:\Municipais\
├── gerador_sigiss.py       # Gerador de arquivos de remessa
├── validador_sigiss.py     # Validador de arquivos
├── web_validator.py        # Servidor web para validação via interface
├── municipios_config.json  # Configurações por município
├── exemplo_dados.json      # Exemplo de dados de entrada
├── exemplo_remessa.txt     # Exemplo de arquivo gerado
├── layout_tomador_SIGISS.pdf # Documentação original do layout
└── README.md               # Este arquivo
```

## Requisitos

- **Python 3.8+**
- **Nenhuma dependência externa** - utiliza apenas biblioteca padrão

## Instalação

1. Clone ou copie os arquivos para o diretório desejado
2. Certifique-se de que o Python 3.8+ está instalado:

```bash
python --version
```

3. (Opcional) Configure permissões de execução nos sistemas Unix:

```bash
chmod +x gerador_sigiss.py
chmod +x validador_sigiss.py
```

## Layout do Arquivo

O arquivo segue o formato CSV com os seguintes campos separados por ponto-e-vírgula:

| Pos | Campo | Tipo | Obrigatório | Descrição |
|-----|-------|------|-------------|-----------|
| 1 | CPF/CNPJ Prestador | Alfanumérico | Sim | Documento do prestador de serviços |
| 2 | Número Nota | Numérico | Sim | Número da nota fiscal (apenas números) |
| 3 | Série Nota | Alfanumérico | Não | Série da nota fiscal |
| 4 | Sub-Série Nota | Alfanumérico | Não | Sub-série da nota fiscal |
| 5 | Dia de Emissão | Data | Não | Data no formato DD/MM/AAAA |
| 6 | Código do Serviço | Numérico | Sim | Código do serviço (até 4 dígitos) |
| 7 | Situação da Nota | Alfanumérico | Sim | t=Tributada, r=Retida, i=Isenta, n=Não Tributada |
| 8 | Valor do Serviço | Decimal | Sim | Base de cálculo (formato: 1.234,56) |
| 9 | CCM Tomador | Alfanumérico | Condicional | Inscrição municipal do tomador |
| 10 | Tipo de Nota | Alfanumérico | Condicional | T=Talão, F=Formulário, J=Jogo Solto, R=Recibo, E=NF-e |
| 11 | Alíquota Simples | Decimal | Não | Alíquota do Simples Nacional (formato: 3,00) |

### Encoding

- **Padrão**: Latin-1 (ISO-8859-1)
- **Chapecó-SC**: UTF-8

### Formatos

- **Data**: DD/MM/AAAA
- **Valores decimais**: Separador decimal é vírgula (`,`), separador de milhar é ponto (`.`)
- **CNPJ**: 14 dígitos (com ou sem formatação)
- **CPF**: 11 dígitos (com ou sem formatação)

## Como Usar o Gerador

### Sintaxe

```bash
python gerador_sigiss.py --municipio <MUNICIPIO> --input <ARQUIVO_JSON> --output <ARQUIVO_SAIDA> [OPCOES]
```

### Parâmetros

| Parâmetro | Abreviação | Descrição | Obrigatório |
|-----------|------------|-----------|-------------|
| `--municipio` | `-m` | Nome do município (ex: "Itapira-SP") | Sim |
| `--input` | `-i` | Caminho do arquivo JSON de entrada | Sim |
| `--output` | `-o` | Caminho do arquivo de saída | Sim |
| `--config` | `-c` | Caminho do arquivo de configuração JSON | Não |
| `--verbose` | `-v` | Ativa saída detalhada | Não |

### Exemplos de Uso

```bash
# Gerar remessa para Itapira-SP
python gerador_sigiss.py --municipio "Itapira-SP" --input dados.json --output remessa.txt

# Gerar com modo verbose
python gerador_sigiss.py --municipio "Itapira-SP" --input dados.json --output remessa.txt --verbose

# Usar configuração personalizada
python gerador_sigiss.py --municipio "Chapeco-SC" --input dados.json --output remessa.txt --config config_custom.json
```

### Formato do Arquivo JSON de Entrada

```json
[
  {
    "cpf_cnpj_prestador": "12.345.678/0001-95",
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
  }
]
```

### Códigos de Retorno

- `0` - Sucesso
- `1` - Erro

## Como Usar o Validador

### Sintaxe

```bash
python validador_sigiss.py --arquivo <ARQUIVO> [OPCOES]
```

### Parâmetros

| Parâmetro | Abreviação | Descrição | Obrigatório |
|-----------|------------|-----------|-------------|
| `--arquivo` | `-a` | Caminho do arquivo a validar | Sim |
| `--municipio` | `-m` | Nome do município para regras específicas | Não |
| `--config` | `-c` | Caminho do arquivo de configuração JSON | Não |
| `--output` | `-o` | Caminho para salvar relatório | Não |
| `--verbose` | `-v` | Ativa saída detalhada | Não |

### Exemplos de Uso

```bash
# Validar arquivo genérico
python validador_sigiss.py --arquivo remessa.txt

# Validar com regras específicas de município
python validador_sigiss.py --municipio "Itapira-SP" --arquivo remessa.txt

# Validar e salvar relatório
python validador_sigiss.py --municipio "Chapeco-SC" --arquivo remessa.txt --output validacao.log

# Modo verbose
python validador_sigiss.py --arquivo remessa.txt --verbose
```

### Códigos de Retorno

- `0` - Arquivo válido
- `1` - Arquivo inválido ou erro

### Relatório de Validação

O relatório inclui:
- Status geral (VÁLIDO/INVÁLIDO)
- Total de linhas processadas
- Contagem de erros e avisos
- Detalhamento de cada problema com:
  - Nível de severidade (ERRO/AVISO)
  - Número da linha
  - Nome do campo
  - Valor encontrado
  - Descrição do problema
  - Valor esperado (quando aplicável)

## Interface Web

Para facilitar o uso sem linha de comando, foi criada uma interface web para validação de arquivos.

### Iniciar o Servidor

```bash
python web_validator.py
python web_validator.py --port 8080
```

### Acessar a Interface

Abra o navegador e acesse:
- http://localhost:8000 (padrão)
- http://localhost:PORTA (porta configurada)

### Funcionalidades da Interface

A interface web permite:
- **Seleção do município** via dropdown
- **Upload de arquivo** (.txt ou .csv)
- **Visualização em tempo real** dos resultados
- **Estatísticas** de linhas, erros e avisos
- **Detalhamento visual** dos problemas encontrados
- **Sem necessidade de instalar dependências** - usa apenas biblioteca padrão Python

### Como Usar

1. Inicie o servidor:
   ```bash
   python web_validator.py
   ```

2. Acesse no navegador: `http://localhost:8000`

3. Selecione o município no dropdown

4. Clique na área de upload e selecione o arquivo `.txt`

5. Clique em **"Validar Arquivo"**

6. Veja o resultado:
   - ✅ **Verde**: Arquivo válido
   - ❌ **Vermelho**: Arquivo inválido com erros
   - 📊 Estatísticas de linhas, erros e avisos
   - 🔍 Detalhamento de cada problema

### Screenshots

```
┌─────────────────────────────────────────┐
│  📋 Validador SIGISS/SIGCORP            │
├─────────────────────────────────────────┤
│  🏙️ Município: [Itapira-SP ▼]         │
│                                         │
│  📁 Clique aqui para selecionar         │
│     o arquivo de remessa                │
│                                         │
│  [      🔍 Validar Arquivo      ]       │
├─────────────────────────────────────────┤
│  ✅ Arquivo Válido                      │
│                                         │
│  ┌────────┐ ┌────────┐ ┌────────┐       │
│  │   5    │ │   0    │ │   0    │       │
│  │ Linhas │ │ Erros  │ │ Avisos │       │
│  └────────┘ └────────┘ └────────┘       │
│                                         │
│  ✓ Nenhum problema encontrado!          │
└─────────────────────────────────────────┘
```

### Segurança

- O servidor roda localmente apenas (`localhost`)
- Arquivos são processados temporariamente e excluídos após validação
- Nenhum dado é armazenado permanentemente

## Como Adicionar um Novo Município

Para adicionar um novo município que utilize o SIGCORP/SIGISS, edite o arquivo `municipios_config.json`:

### Estrutura de Configuração

```json
{
  "municipios": {
    "NOME-UF": {
      "codigo": "CODIGO_IBGE",
      "uf": "UF",
      "nome": "Nome do Município",
      "sistema_sigcorp": true,
      "configuracoes": {
        "encoding": "latin-1",
        "separador": ";",
        "formato_data": "DD/MM/AAAA",
        "casas_decimais": 2,
        "separador_decimal": ",",
        "cabecalho_obrigatorio": false,
        "rodape_obrigatorio": false,
        "registro_fixo": false
      },
      "campos_obrigatorios": [
        "cpf_cnpj_prestador",
        "numero_nota",
        "codigo_servico",
        "situacao_nota",
        "valor_servico"
      ],
      "situacoes_permitidas": ["t", "r", "i", "n"],
      "tipos_nota_permitidos": ["T", "F", "J", "R", "E"],
      "aliquotas": {
        "minima": 2.0,
        "maxima": 5.0,
        "padrao": 3.0
      },
      "codigos_servico": {
        "tipo": "numerico",
        "tamanho": 4,
        "obrigatorio": true
      },
      "validacoes_adicionais": [],
      "observacoes": "Descrição das regras específicas"
    }
  }
}
```

### Exemplo de Adição

Para adicionar o município de São Paulo-SP:

```json
"Sao Paulo-SP": {
  "codigo": "355030",
  "uf": "SP",
  "nome": "Sao Paulo",
  "sistema_sigcorp": true,
  "configuracoes": {
    "encoding": "latin-1",
    "separador": ";",
    "formato_data": "DD/MM/AAAA",
    "casas_decimais": 2,
    "separador_decimal": ",",
    "cabecalho_obrigatorio": false,
    "rodape_obrigatorio": false,
    "registro_fixo": false
  },
  "campos_obrigatorios": [
    "cpf_cnpj_prestador",
    "numero_nota",
    "codigo_servico",
    "situacao_nota",
    "valor_servico",
    "ccm_tomador"
  ],
  "situacoes_permitidas": ["t", "r", "i", "n"],
  "tipos_nota_permitidos": ["T", "F", "J", "R", "E"],
  "aliquotas": {
    "minima": 2.0,
    "maxima": 5.0,
    "padrao": 5.0
  },
  "codigos_servico": {
    "tipo": "numerico",
    "tamanho": 4,
    "obrigatorio": true
  },
  "validacoes_adicionais": ["cnpj_prestador_valido"],
  "observacoes": "Maior cidade do Brasil. CCM do tomador obrigatório."
}
```

## Descrição dos Campos

### CPF/CNPJ Prestador (Campo 1)

- Aceita CPF (11 dígitos) ou CNPJ (14 dígitos)
- Aceita formatado ou não
- Dígitos verificadores são validados
- **Exemplos válidos**: `12345678000195`, `12.345.678/0001-95`, `123.456.789-01`

### Número da Nota (Campo 2)

- Apenas números
- Não pode conter letras ou caracteres especiais
- **Exemplo válido**: `1234`

### Série e Sub-Série (Campos 3 e 4)

- Identificam a série da nota fiscal
- Geralmente numéricos, mas aceitam alfanumérico
- **Exemplo**: Série `1`, Sub-Série `0`

### Dia de Emissão (Campo 5)

- Formato: `DD/MM/AAAA`
- **Exemplo válido**: `15/03/2026`

### Código do Serviço (Campo 6)

- Código numérico de até 4 dígitos
- Corresponde à lista de serviços da LC 116/2003
- **Exemplos comuns**:
  - `1701` - Análise e desenvolvimento de sistemas
  - `1706` - Programação
  - `1708` - Processamento de dados

### Situação da Nota (Campo 7)

Valores permitidos:

| Código | Significado | Descrição |
|--------|-------------|-----------|
| `t` | Tributada | Nota tributada normalmente |
| `r` | Retida | ISS retido na fonte |
| `i` | Isenta | Nota isenta de ISS |
| `n` | Não Tributada | Não sujeita a tributação |

### Valor do Serviço (Campo 8)

- Base de cálculo do ISS
- Formato brasileiro: vírgula para decimais, ponto para milhares
- **Exemplos válidos**: `1000,00`, `1.234,56`, `1500`

### CCM do Tomador (Campo 9)

- Inscrição Municipal do tomador de serviços
- Obrigatoriedade varia por município

### Tipo de Nota (Campo 10)

| Código | Significado |
|--------|-------------|
| `T` | Talão |
| `F` | Formulário |
| `J` | Jogo Solto |
| `R` | Recibo |
| `E` | NF-e (Nota Fiscal Eletrônica) |

### Alíquota Simples (Campo 11)

- Alíquota do Simples Nacional (quando aplicável)
- Formato: `3,00` para 3%
- Deixe em branco se não for optante pelo Simples

## Exemplos

### Exemplo 1: Gerar e Validar

```bash
# 1. Gerar o arquivo
python gerador_sigiss.py --municipio "Itapira-SP" --input exemplo_dados.json --output minha_remessa.txt

# 2. Validar o arquivo gerado
python validador_sigiss.py --municipio "Itapira-SP" --arquivo minha_remessa.txt --output validacao.log
```

### Exemplo 2: Ver conteúdo do arquivo gerado

```bash
cat minha_remessa.txt
# ou
type minha_remessa.txt
```

Saída esperada:
```
12345678000195;1234;1;0;15/03/2026;1701;t;1000,00;123456789;T;3,00
98765432000196;1235;1;0;15/03/2026;1701;r;2500,50;987654321;T;
```

### Exemplo 3: Processamento em lote

```bash
#!/bin/bash
# processar_lote.sh

for municipio in "Itapira-SP" "Mogi Mirim-SP" "Chapeco-SC"; do
    echo "Processando $municipio..."
    python gerador_sigiss.py --municipio "$municipio" --input "dados_${municipio}.json" --output "remessa_${municipio}.txt"
    python validador_sigiss.py --municipio "$municipio" --arquivo "remessa_${municipio}.txt" --output "validacao_${municipio}.log"
done
```

## Tratamento de Erros

### Erros Comuns do Gerador

| Erro | Causa | Solução |
|------|-------|---------|
| `Municipio não encontrado` | Nome incorreto ou não cadastrado | Verifique o nome no `municipios_config.json` |
| `CPF/CNPJ inválido` | Dígitos verificadores incorretos | Verifique o documento |
| `Valor do serviço inválido` | Formato incorreto | Use formato `1.234,56` ou `1234,56` |
| `Código do serviço inválido` | Não numérico ou muito longo | Use até 4 dígitos numéricos |

### Erros Comuns do Validador

| Erro | Causa | Solução |
|------|-------|---------|
| `Encoding incorreto` | Arquivo em formato diferente do esperado | Converta para Latin-1 ou UTF-8 conforme município |
| `Número incorreto de campos` | Separador errado ou campos extras | Verifique o separador `;` |
| `Data inválida` | Formato diferente de DD/MM/AAAA | Ajuste o formato da data |

## Municípios Suportados

Atualmente configurados:

| Município | UF | Código IBGE | Observações |
|-----------|-----|-------------|-------------|
| Itapira | SP | 352260 | Configuração padrão SIGCORP |
| Mogi Mirim | SP | 353060 | Exige tipo de nota |
| Chapecó | SC | 420420 | Encoding UTF-8, exige CCM |

## Suporte

Para dúvidas ou problemas:

1. Verifique se o município está configurado em `municipios_config.json`
2. Consulte a documentação oficial do SIGCORP
3. Execute em modo verbose (`-v`) para detalhes adicionais

## Licença

Este é um projeto de código aberto para integração com sistemas municipais de NFS-e.

---

**Versão**: 1.1
**Atualizado**: Março de 2026
**Compatibilidade**: SIGCORP/SIGISS
>>>>>>> 63ec8a5 (Commit Inicial)
