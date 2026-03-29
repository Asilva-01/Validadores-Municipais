# Ferramentas SIGISS / SIGCORP
Este ecossistema permite a conversão de conjuntos de dados para o layout de serviços tomados do provedor SIGISS/SIGCORP e, especialmente, a validação rigorosa dos arquivos recém-criados ou oriundos de outros sistemas.

## Funcionalidades principais:
- **`validador_sigiss.py`**: Motor de validação de layouts textuais.
- **`gerador_sigiss.py`**: Conversor de dados estruturados em JSON para o layout SIGISS delimitado (`.txt`).
- **`municipios_config.json`**: Repositório central com a definição flexível das regras de municípios suportados (atualidade: Itapira-SP e Chapecó-SC).
- Cálculos imutáveis e verificações automáticas de Integridade: DVs de CPF/CNPJ base-11, formatação de decimais e mascaramento.

---

## 1. Como Usar o Validador
O script recebe como primeiro argumento o caminho para o arquivo (`.txt` ou `.csv`) e com o argumento nomeado `--cidade` aponta para uma tabela de regras do município.
A validação emite relatórios robustos de console e, simultaneamente, cria um log persistente de trilha (`nome_do_arquivo.log`).

```bash
python validador_sigiss.py teste_itapira_valido.txt --cidade Itapira
```
*(Se usar Chapecó, substitua `--cidade Itapira` por `--cidade Chapeco`)*

### O que o motor verifica?
1. Layout estrito no modelo SIGCORP.
2. Composição exclusiva por delimitadores `;` ou `\t` (aborto crítico imediato caso falhe).
3. Dígito Verificador Autêntico das chaves CNPJ/CPF (rejeição garantida p/ chaves falsas).
4. Tipagem nativa de dígitos dos campos numéricos, rejeitando a presença de strings.
5. Sistema separador de decimais para alíquotas e Valores, onde a validação atua implacavelmente rejeitando pontos (.) e exigindo vírgulas (,), padrão BR.
6. Tipologia da Nota Fiscal ou mapeamento de AVISO automático e mapeamento silencioso do campo **Situação** (ex: o validador perdoa arquivos de Chapecó que enviam "tt", mapeia nativamente como "t" e relata a tolerância em aviso).
7. Expressão regular rigorosa (`Regex`) exigindo comprimentos idênticos de CCM a depender de qual município foi alimentado no `municipios_config.json`.

---

## 2. Como Usar o Gerador
O script de geração atua como intermediário, lendo um JSON simples e processando os dados para formato de texto de forma resiliente, abortando em caso de dados que não obedecem a lógica central de layout.

**Exemplo:**
```bash
python gerador_sigiss.py modelo.json output.txt
```

### Formato esperado no `modelo.json`

```json
{
  "cidade": "Itapira",
  "notas": [
    {
      "cpf_cnpj": "06012316000180",
      "nf": "584",
      "serie": "20",
      "sub_serie": "",
      "dia_emissao": "10",
      "codigo_servico": "123",
      "situacao": "r",
      "valor": "39209,12",
      "ccm_tomador": "00000000004471",
      "tipo_nf": "E",
      "aliquota": "0,0000"
    }
  ]
}
```

---

## 3. Configurando Novos Municípios
O sistema depende intrinsecamente do arquivo **`municipios_config.json`**.
A arquitetura base isola toda variável e regra geográfica volátil; códigos python contêm regras de unificação federal exclusivas (como validação de CPF ou recusa de pontos flutuantes `10.5`). 

Para introduzir suporte a uma nova cidade SIGISS (Ex: Carapicuíba), basta empurrar este chassi ao JSON:
```json
  "Carapicuiba": {
    "uf": "SP",
    "delimitador": "\t",
    "encoding": "utf-8",
    "ccm_regex": "^\\d{6}$",
    "map_situacao_aviso": {
      "tt": "t",
      "isenta": "i"
    }
  }
```
Isso informará nativamente a engine Python sobre a variação do município.
