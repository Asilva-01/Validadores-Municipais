 
 
Nota Fiscal de Serviços Eletrônica  
NFS-e 
Layout de importação de 
Serviços Tomados  
 
 
IMA - Informática de Municípios Associados . É permitida a reprodução total ou parcial deste 
documento sem o pagamento de direitos autorais, contanto que as cópias sejam feitas e 
distribuídas sem fins lucrativos. O autor lembra que o título e a data da publicação devem constar 
na cópia e deve constar que a cópia foi feita com a permissão do autor. Além disso, toda 
reprodução deve citar a fonte. Caso contrário, a cópia ou a reprodução requer o pagamento de 
taxas e/ou a permissão por escrito.  
  

 
 
C A M P I N A S  – N F S e  – L a y o u t  d e  I m p o r t a ç ã o  d e  S e r v i ç o s  T o m a d o s  
P á g i n a  2 | 16 
I M A  - I n f o r m á t i c a  d e  M u n i c í p i o s  A s s o c i a d o s  202 4 Importação de Serviços Tomados de Outros Municípios  
Layout de Importação de dados de nota(s) de serviço(s) tomado(s) de prestadores de outro 
município. Neste manual encontram -se as instruções para a correta importação de dados oriundos 
de documentos fiscais de serviços tomados de prestadores de outro municí pio para o sistema de 
Nota Fiscal Eletrônica de Serviços – NFS-e.  
Tipo de Registros  
O arquivo a ser gerado para importação deverá estar no formato texto, e conter os seguintes tipos, 
sendo o tipo “D” opcional:  
TIPOS DE REGISTROS:  
• Registro tipo “H” - Identificação (Header)  
• Registro tipo “T” - Notas Tomadas  
• Tipos de Dados:  
• A - Alfanuméricos  
• D - Data  
• N - Numérico  
Observações:  
• O primeiro registro deve ser, obrigatoriamente, um registro do tipo “H”. Este registro deverá 
ser único no arquivo.  
• A inscrição municipal indicada no registro H (header) do arquivo deve ser a mesma inscrição 
do tomador de serviços declarado na nota.  
• Este arquivo deve ser gerado pelo sistema exportador no formato texto (extensão .txt) e 
conter os registros segundo layout pré -definido constante neste manual. O nome do arquivo 
criado pode receber qualquer nome com ‘.txt’.  Ex.: IMPORTA.TXT  
  
 
 
C A M P I N A S  – N F S e  – L a y o u t  d e  I m p o r t a ç ã o  d e  S e r v i ç o s  T o m a d o s  
P á g i n a  3 | 16 
I M A  - I n f o r m á t i c a  d e  M u n i c í p i o s  A s s o c i a d o s  202 4 Estrutura Header  
 
 
Layout dos Serviços Tomados  
 
Nº Nome do Campo  TP PI PF Tam . Obg. Descrição  
01 Identificação do 
registro  A 1 1 1 S Caractere  fixo "T" Notas Tomadas  
02 Data de emissão do 
documento fiscal  D 2 11 10 S Indica a data de emissão do documento 
fiscal  Data no formato DD/MM/YYYY"  
03 Data Competência  D 12 18 7 S Mês  e ano da competência da prestação  de 
serviço  (MM/ YYYY)  
04 Número de 
identificação 
documento fiscal  N 19 33 15 S Permitir somente números EX: 
000000000000001  
Alinhar o número à esquerda e preencher 
os espaços restantes com espaços.  
05 Série do documento 
fiscal  A 34 38 5 N Indica o número de série do documento 
fiscal . Alinhar o número à esquerda e 
preencher os espaços restantes com 
espaços.  
06 Modelo do 
documento fiscal  A 39 40 2 S • RD – Recibo/Diversos   
• A – NF de Serviços  
• E – NF Série Única  
• A1 – NF Série   
• A1 F – Cupom Fiscal  
• BB – Boleto Bancário   
• CE – Carnê Escolar  
• G – Contribuintes Dispensados de 
Utilizar  
• AV – NF Avulsa  
• RP – Recibo Provisório de Serviços (RPS)  
• OT – Outros Documentos (Pessoa 
Jurídica)  
• R – RPA ou Recibo (Pessoa Física)  
• OM – NF de Outro Município  Nome do Campo  TP PI PF Tam . Descrição  
Identificação do registro  A 1 1 1 Caractere fixo “H“ Header  
Inscrição para indicar empresa  A 2 31 30 Número da inscrição municipal da 
empresa  
 
 
C A M P I N A S  – N F S e  – L a y o u t  d e  I m p o r t a ç ã o  d e  S e r v i ç o s  T o m a d o s  
P á g i n a  4 | 16 
I M A  - I n f o r m á t i c a  d e  M u n i c í p i o s  A s s o c i a d o s  202 4 Nº Nome do Campo  TP PI PF Tam . Obg. Descrição  
07 Tipo do 
prestador  N 41 41 1 S Tipo da pessoa do prestador  
• 1 - Nacional  
• 2 - Exterior  
08 CPF /CNPJ do 
prestador  N 42 55 14 S Número do CPF ou CNPJ do prestador 
de serviços, informar somente números;  
• Pessoa Jurídica - preencher o campo 
com 14 posições;  
• Pessoa Física - preencher o campo com 
11 posições;  
• Prestador do Exterior - preencher com 
zeros.  
09 Documento de 
identificação 
prestador do exterior  N 56 75 20 N Número do documento de identificação do 
prestador do exterior . Preencher somente 
quando se tratar de prestador do exterior  
Quando não houver, preencher com 
espaço em  branco.  
10 Nome/Razão social 
do prestador de 
serviços  A 76 225 150 S Nome ou razão social do prestador de 
serviços  
11 Código do município  
do prestador de 
serviços"  A 226 232 7 S Código do município onde  o serviço  foi 
prestado (tabela do IBGE), para prestador 
de serviços do exterior  colocar "9999999". 
Alinhar o código à esquerda e preencher os 
espaços restantes com espaços."  
12 Prestador 
optante do 
simples 
nacional  A 233 233 1 S Define se o prestador é enquadrado no 
Simples Nacional:  
• S - Sim (Enquadrado como simples 
nacional) ; 
• N - Não (Não enquadrado como simples 
nacional) . 
• Caso o prestador seja enquadrado no 
MEI, o valor deste campo deve ser N . 
13 Prestador enquadrado 
no MEI  A 234 234 1 S Define se o prestador é enquadrado no 
MEI:  
• S - Sim (Enquadrado como MEI)  
• N - Não (Não enquadrado  como MEI)  
14 Prestador 
estabelecido no 
município  A 235 235 1 S Define se o prestador é estabelecido no 
município:  
• S - Sim 
• N - Não  
15 Cep do endereço do 
prestador  N 236 243 8 S Número do CEP do logradouro do 
prestador .  
Informar somente números  
 
 
C A M P I N A S  – N F S e  – L a y o u t  d e  I m p o r t a ç ã o  d e  S e r v i ç o s  T o m a d o s  
P á g i n a  5 | 16 
I M A  - I n f o r m á t i c a  d e  M u n i c í p i o s  A s s o c i a d o s  202 4 Nº Nome do Campo  TP PI PF Tam . Obg. Descrição  
16 Tipo de logradouro 
do prestador  A 244 268 25 S Tipo do logradouro do endereço do 
prestador . EX: Rua, Avenida, Via. "  
17 Nome do logradouro 
do prestador  A 269 318 50 N Nome do logradouro do endereço do 
prestador  
18 Número do 
logradouro do 
prestador  N 319 328 10 N Número do logradouro do endereço do 
prestador  
19 Complemento do 
prestador  A 329 388 60 N Complemento do logradouro 
conforme os tipos definidos  na aba 
Padrão  complemento  
20 Bairro prestador  A 389 448 60 N Nome do bairro referente ao logradouro do 
prestador  
21 UF do prestador  A 449 450 2 S Sigla do estado referente ao logradouro do 
prestador  
22 País do 
prestador  N 451 454 4 S Código do país da prestação  do serviço 
(Tabela do BACEN).  
Preencher somente quando o País do 
presta do for "  Exterior "; 
https://w ww.bcb .gov.br/rex/Censo2000/por
t/ Manual/Pais.asp?frame=1  
23 Cidade do prestador  A 455 504 50 S Cidade referente ao logradouro do 
prestador  
24 Código do serviço 
prestado  N 505 509 5 S Código do serviço prestado  
25 Código da Atividade 
CNAE relacionada ao 
serviço  N 510 518 9 S Código da CNAE prestada na nota fiscal  
Número no formato 999999999  
O código da atividade poderá ser 
consultado na página : 
https://homol -
nfse.ima.sp.gov.br/notafiscal/paginas/por
tal/#/tabela  
 
26 Código Obra  N 519 533 15 N Código da obra previamente já cadastrado 
no Sistema . 
Alinhar o código da obra à esquerda e 
preencher os espaços restantes com espaços.  
Quando não houver, preencher com espaço 
em branco.  
27 Local da prestação 
do serviço  A 534 536 3 S Local da prestação do serviço  
• LOC - Local  
• EXT - Exterior  
 
 
C A M P I N A S  – N F S e  – L a y o u t  d e  I m p o r t a ç ã o  d e  S e r v i ç o s  T o m a d o s  
P á g i n a  6 | 16 
I M A  - I n f o r m á t i c a  d e  M u n i c í p i o s  A s s o c i a d o s  202 4 Nº Nome do Campo  TP PI PF Tam . Obg. Descrição  
28 "Código do 
município do  
Local da Prestação 
do Serviço.  " A 537 543 7 N Código do município onde foi prestado o 
serviço. (tabela do IBGE), para prestador de 
serviços do exterior  colocar "9999999". 
Alinhar o código à esquerda e preencher os 
espaços restantes com espaço em branco.  
29 UF prestação serviço  A 544 545 2 N Sigla do estado da prestação do serviço . 
Preencher somente quando a prestação for 
"LOC - Local "; 
Quando não houver, preencher com 
espaço em  branco."  
30 Municipio exterior 
prestação do serviço  A 546 595 50 N Nome do município do exterior.  
Preencher somente quando o local da 
prestação for " EXT - Exterior "; 
Quando não houver, preencher com espaço 
em branco . 
31 Estado exterior 
prestação do 
serviço  A 596 645 50 N Nome do estado do exterior.  
Preencher somente quando o local da 
prestação for " EXT - Exterior "; 
Quando não houver, preencher com 
espaço em  branco.  
32 País da prestação 
do serviço  N 646 649 4 N Código do país da prestação do serviço 
(Tabela do BACEN). Preencher somente 
quando o local da prestação for " EXT - 
Exterior "; 
https://w ww.bcb .gov.br/rex/Censo2000/por
t/ Manual/Pais.asp?frame=1  
Quando não houver, preencher com espaço 
em branco.  
33 Local do resultado da 
prestação do serviço  A 650 652 3 N Local do resultado da prestação do 
serviço:  
• EXT - Exterior  
• BRA – Brasil  
34 Código do 
município do 
Local do 
resultado da 
Prestação  do 
Serviço."  A 653 659 7 N Código do município onde foi o resultado 
da prestado o serviço (tabela do  IBGE),  para  
prestador  de serviços  do exterior  colocar 
"9999999 ". 
Alinhar o código à esquerda e preencher os 
espaços restantes com espaços."  
35 UF do resultado da 
prestação serviço  A 660 661 2 N Sigla do estado do resultado da prestação 
do serviço  
Preencher somente quando o resultado da 
prestação  for " BRA - Brasil "; 
Quando não houver, preencher com 
espaço em  branco.  
 
 
C A M P I N A S  – N F S e  – L a y o u t  d e  I m p o r t a ç ã o  d e  S e r v i ç o s  T o m a d o s  
P á g i n a  7 | 16 
I M A  - I n f o r m á t i c a  d e  M u n i c í p i o s  A s s o c i a d o s  202 4 Nº Nome do Campo  TP PI PF Tam . Obg. Descrição  
36 Município  exterior 
do resultado 
prestação serviço  A 662 711 50 N "Nome do município  do exterior.  
Preencher somente quando o resultado da 
prestação  for " EXT - Exterior ";  
Quando não houver, preencher com espaço 
em branco.  
37 Estado exterior do 
resultado prestação 
serviço  A 712 761 50 N Nome do estado do exterior.  
Preencher somente quando o resultado da 
prestação  for " EXT - Exterior ";  
Quando não houver, preencher com espaço 
em branco.  
38 País do resultado da 
prestação do 
serviço  N 762 765 4 N Código do país onde é o resultado da 
prestação do serviço (Tabela do BACEN). 
Preencher somente quando o resultado da  
prestação for " EXT - Exterior "; 
https://w ww.bcb .gov.br/rex/Censo2000/port
/ Manual/Pais.asp?frame=1  
Quando não houver, preencher com espaço 
em branco.  
39 Motivo da não 
retenção  A 766 766 1 N Indica o motivo da não retenção  
• A - Não Incidência  no Município  
• B - Não Tributável  
• C - Pago pelo Prestador/ Não Incidente  
• D - Imune E - Isento  
• F - Sociedade de Profissionais  
• G - Profissional Autônomo Inscrito  
• H - Estimativa  
• I - Depósito em Juízo  
• J - Medida Liminar/Cautelar  
• V - Valor de Serviços Menor que o 
Mínimo  
Preencher somente quando o campo 41 for 
= RNF (Retido na Fonte)  
Quando não houver,  preencher com espaço  
40 Exigibilidade  do ISS N 767 767 1 S Exigibilidade do ISS : 
1. Exigível  
2. Não incidência  
3. Isenção  
4. Exportação  
5. Imunidade  
6. Exigibilidade Suspensa por Decisão 
Judicial  
7. Exigibilidade Suspensa por 
Processo Administrativo  
 
 
C A M P I N A S  – N F S e  – L a y o u t  d e  I m p o r t a ç ã o  d e  S e r v i ç o s  T o m a d o s  
P á g i n a  8 | 16 
I M A  - I n f o r m á t i c a  d e  M u n i c í p i o s  A s s o c i a d o s  202 4 Nº Nome do Campo  TP PI PF Tam . Obg. Descrição  
41 Tipo recolhimento 
imposto  N 768 770 3 S Responsável pelo recolhimento do 
imposto:  
• RPP – A recolher pelo prestador  
• RNF  – Retido na fonte  
• NAP  - Não se aplica (este deve ser 
informado quando  a exigibilidade  for 
Isenção,  Imunidade , Exigibilidade 
Suspensa por Decisão Judicial ou 
Exigibilidade Suspensa por Processo 
Administrativo ) 
42 Alíquota  de ISS  N 771 775 5 N Identifica a alíquota do ISS  
Número no formato 99.99   
Se não for utilizado todo  o tamanho do 
campo, complete o restante com espaços.  
Não informar quando Exigibilidade for 3, 
4, 5, 6 ou 7.  
Preencher o campo com zero.  
É obrigatório preencher quando 
Exigibilidade for 1 ou 2 (Intervalo entre 2% 
e 5%).  
43 Valor do serviço da 
nota fiscal  N 776 790 15 S Quando não houver, preencher com zeros.  
44 Valor das deduções  N 791 805 15 N Valor das deduções para Redução da 
Base de Cálculo  
Número no formato 999999999999.99  
Preencher quando Tipo da dedução  for 
diferente de "0";  
Alinhar à esquerda e preencher os espaços 
restantes com espaços.  
Quando não houver, preencher com zeros.  
45 Desconto 
incondicionado  N 806 820 15 N Valor do desconto incondicionado 
Número no formato 999999999999.99  
Alinhar à esquerda e preencher os espaços 
restantes com espaços.  
Quando não houver, preencher com zeros.  
46 Desconto 
condicionado  N 821 835 15 N Valor do desconto condicionado 
Número no formato 999999999999.99  
Alinhar à esquerda e preencher os espaços 
restantes com espaços. Quando não houver, 
preencher com zeros.  
47 Base de cálculo  N 836 850 15 S Valor da base de cálculo (Valor  de 
Servi ços – Valor  de Dedu ções – 
Desconto  Incondicionado)  
A Base de cálculo deve ser igual ou menor 
que o valor da nota fiscal.  
 
 
C A M P I N A S  – N F S e  – L a y o u t  d e  I m p o r t a ç ã o  d e  S e r v i ç o s  T o m a d o s  
P á g i n a  9 | 16 
I M A  - I n f o r m á t i c a  d e  M u n i c í p i o s  A s s o c i a d o s  202 4 Nº Nome do Campo  TP PI PF Tam . Obg. Descrição  
48 Valor PIS  N 851 865 15 N Valor da retenção do PIS Número no 
formato 999999999999.99  
Alinhar à esquerda e preencher os espaços 
restantes com espaços.  
Quando não houver, preencher com zeros.  
49 Valor COFINS  N 866 880 15 N Valor da retenção do COFINS  
Número no formato 999999999999.99  
Alinhar o código à esquerda e preencher os 
espaços restantes com espaços.  
Quando não houver,  preencher com zeros.  
50 Valor INSS  N 881 895 15 N Valor da retenção do INSS Número no 
formato 999999999999.99  
Alinhar o código à esquerda e preencher os 
espaços restantes com espaços.  
Quando não houver, preencher com zeros.  
51 Valor IR  N 896 910 15 N "Valor da retenção do IR Número no 
formato 999999999999.99  
Alinhar à esquerda e preencher os espaços 
restantes com espaços.  
Quando não houver, preencher com zeros.  
52 Valor CSLL  N 911 925 15 N Valor da retenção do CSLL Número no 
formato 999999999999.99  
Alinhar o código à esquerda e preencher os 
espaços restantes com espaços.  
Quando não houver, preencher com zeros.  
53 Outras 
retenções  N 926 940 15 N "Valor outras retenções na Fonte  
Número no formato 999999999999.99  
Alinhar à esquerda e preencher os espaços 
restantes com espaços. Quando não houver, 
preencher com zeros.  
 
 
C A M P I N A S  – N F S e  – L a y o u t  d e  I m p o r t a ç ã o  d e  S e r v i ç o s  T o m a d o s  
P á g i n a  10 | 16 
I M A  - I n f o r m á t i c a  d e  M u n i c í p i o s  A s s o c i a d o s  202 4 Nº Nome do Campo  TP PI PF Tam . Obg. Descrição  
54 Valor do ISS  N 941 955 15 N Valor do ISS devido Número  no 
formato 999999999999.99  
Alinhar à esquerda e preencher os espaços 
restantes com espaços. Quando não 
houver, preencher com zeros.  
Não informar quando Exigibilidade for 3, 4, 
5, 6 ou 7.  
Preencher o campo com zero.  
É obrigatório preencher quando 
Exigibilidade for 1 ou 2.  
Valor deve ser maior que zero.  
Valor deve ser o resultado do campo 47 * 
campo 42.  
55 Descriminação dos 
serviços da Nota 
Fiscal  A 956 2955  2000  N Discriminação do conteúdo da nota fiscal . 
Quando não houver, preencher com espaço 
em branco.  
 
  
 
 
C A M P I N A S  – N F S e  – L a y o u t  d e  I m p o r t a ç ã o  d e  S e r v i ç o s  T o m a d o s  
P á g i n a  11 | 16 
I M A  - I n f o r m á t i c a  d e  M u n i c í p i o s  A s s o c i a d o s  202 4 Padrão Complemento  
1. Para cada tipo definido deverá ser informado um valor inserindo o caractere (:) EX: 
“ANDAR:  6º”; 
2. Se for inserido mais de um tipo no complemento, inserir o caractere (,) para finalizar 
um tipo e iniciar um novo tipo EX: “ANDAR:6º,  APT:24 ” 
 
TIPO  DESCRIÇÃO  
ANDAR  ANDAR  
ANEXO  ANEXO  
APT APARTAMENTO  
ARMZ  ARMAZEM  
BANCA  BANCA  
BLOCO  BLOCO  
BOX  BOX  
BRCAO  BARRACÃO  
CAIS  CAIS  
CASA  CASA  
COND  CONDOMINIO  
CONJ  CONJUNTO  
CXPST  CAIXA POSTAL  
EDIF  EDIFICIO  
FUNDOS  FUNDOS  
GALPAO  GALPAO  
GARAGE  GARAGEM  
KM KM 
LETRA  LETRA  
LOJA  LOJA  
LOTE  LOTE  
MZNINO  MEZANINO  
NIVEL  NIVEL  
PAVLH  PAVILHAO  
PAVMTO  PAVIMENTO  
PLTIS  PILOTIS  
QUADRA  QUADRA  
QUIOSQ  QUIOSQUE  
SALA  SALA  
SETOR  SETOR  
SLJ SOBRELOJA  
STAND  STAND  
SUBSL  SUBSOLO  
 
 
 
C A M P I N A S  – N F S e  – L a y o u t  d e  I m p o r t a ç ã o  d e  S e r v i ç o s  T o m a d o s  
P á g i n a  12 | 16 
I M A  - I n f o r m á t i c a  d e  M u n i c í p i o s  A s s o c i a d o s  202 4 Validação dos Serviços Tomados  
 
No. Erro  Observação  
1 Informe o Prestador de Serviços  O campo 08 não está preenchido.  
2 Tomador  de Serviços  não poder  ser utilizado  
como  Prestador de Serviços  No campo 08 foi indicado o mesmo CNPJ da 
empresa declarante.  
3 Informe a Data de Emissão  O campo 02 não está preenchido  
4 Data de Emissão maior que o Mês Atual  Não é permitido  o lançamento  de notas  
com  data superior ao mês  atual  
6 Data da Competência maior que Data de 
Emissão  O campo 03 está com data superior à data do 
campo 02.  
7 Informe a data da competência  O campo 03 não está preenchido  
8 Número da NF menor que 0  Não é permitido no campo 04 números  
com valor negativo.  
9 Informe o modelo do documento fiscal  O campo 06 não está preenchido  
10 Documento fiscal inválido  A informação indicada no campo 06 não 
condiz com os modelos de documentos 
válidos  
11 Documento  "Nota  Fiscal  Avulsa"  não 
pode  ter o Imposto Retido  Quando for indicada a opção AV no campo 
06, não poderá  ser preenchido  com  valor  o 
campo  42 (Alíquota ) 
12 Recibo/RPA somente para Prestador de 
Serviços Pessoa Física  "O documento  informado  no campo  06 
somente  será permitido  
quando for indicado o campo 08 com valor 
de CPF  
para pessoa física"  
13 Informe o Código do município do prestador  O campo 11 não está preenchido  
14 Pessoa  Física  pode  utilizar  somente  os 
Documentos:  R-RPA Recibo (Pessoa Física) 
ou AV-NF Avulsa  Quando  o campo  08 for informado  com  
valor  de CPF para pessoa física, o campo 
06 somente pode ser preenchido  com  as 
opções  R ou AV 
15 Informe CPF/CNPJ do prestador  O campo 08 não está preenchido  
16 CPF ou CNPJ do prestador inválido  Quando  o campo  07 for "1 - Nacional",  o 
campo  08 deve ser preenchido  com  uma  
numeração  válida;  
17 Informe Nome/Razão social  O campo 10 não está preenchido  
18 Para  prestador  de serviços  não 
estabelecido  no Brasil  não existe  
CPF/CNPJ  Quando  no campo  07 for indicada  a opção  "2 - 
Exterior", o campo  08 deve  ser preenchido  
com  zeros.  
19 Documento  de identificação  não deve  ser 
preenchido  para prestador  nacional  Quando no campo 07 for indicada a opção "1 
- Nacional", o campo 9 não deve ser 
preenchido.  
20 Somente  uma  das opções  Simples  ou MEI 
deve  possuir  o valor  SIM Somente  um dos campos  12 e 13 deve  
estar  com  o valor  Sim.  
21 Prestador estabelecido no município  não 
informado  Deve ser definido um valor para o campo 14  
 
 
C A M P I N A S  – N F S e  – L a y o u t  d e  I m p o r t a ç ã o  d e  S e r v i ç o s  T o m a d o s  
P á g i n a  13 | 16 
I M A  - I n f o r m á t i c a  d e  M u n i c í p i o s  A s s o c i a d o s  202 4 No. Erro  Observação  
22 UF do prestador  deve  ser preenchido  
para  prestador nacional  Quando o campo 07 for "1 - Nacional", é 
necessário preencher o campo 21  
23 Cidade  do prestador  deve  ser preenchido  
para  prestador nacional  Quando o campo 07 for "1 - Nacional", é 
necessário preencher o campo 23  
24 Tipo logradouro informado inválido  Tipo logradouro do campo 16 não 
cadastrado.  
25 Complemento não está  preenchido 
corretamente  Campo 19 não este seguindo o 
padrão de preenchimento  do 
complemento  
26 Tipo do complemento inválido  Campo  19 não está  seguindo  o padrão  
para  tipo de complemento  
27 Informe  NF de Outro  Município  somente  
para  Prestadores localizados em outro  
município  Quando  o campo  06 for preenchido  com  a 
opção  OM, será  necessário  preencher  o 
campo  11 com  código  que identifique  
município  diferente  do tomador  declarante  
28 O Motivo da não retenção inválida  A informação indicada no campo 39 não 
condiz com os motivos de retenções válidos  
29 Informe o Valor dos serviços da NF  O campo 43 não está preenchido  
30 Informe um Valor para a Alíquota do ISS O campo 42 não está preenchido.  
   
31 Alíquota do ISS inválida  A informação  indicada  no campo  42 
está  fora do padrão  definido  
32 Alíquota  de Retenção  na Fonte  somente  
sobre  Valor  de Serviços  Quando o campo 43 for igual a 0 (zero), o 
campo 42 não poderá ser maior que zero  
33 O Tomador  é um Substituto  Tributário  
deve  reter  o ISS na Fonte  No cadastro da empresa consta a informação 
de Substituto Tributário. Neste caso deverá ser 
indicada a retenção na fonte através do campo 
41 com valor "RNF  
– Retido na fonte" e campo 42.  
34 Retenção na Fonte já cadastrada!  Nota já cadastrada  
35 Esta Atividade é uma Atividade de Grupo  Atividade com menos de 9 caracteres  
36 Atividade não cadastrada  Atividade  (vinculada  ao serviço)  informada  
no campo 25 não  cadastrada.  
37 Atividade informada não pertence ao serviço 
informado  Atividade  do campo  25 não está  relacionada  
ao serviço campo  24 
38 Informe o código do Serviço  No campo 11, quando o código do município 
corresponde  a um município  diferente  do 
município  do tomador  é necessário  
preencher  o campo  24 
39 Este Serviço é um Serviço de Grupo  Serviço com menos de quatro caracteres  
40 Serviço não cadastrado  O serviço informado do campo 24 não 
cadastrada.  
41 Informe  o campo  Motivo  não retenção  
somente  para  NF não retidas  Quando o campo 39 for preenchido, o campo 
(ALIQUOTA) não poderá ser maior que zero.  
 
 
C A M P I N A S  – N F S e  – L a y o u t  d e  I m p o r t a ç ã o  d e  S e r v i ç o s  T o m a d o s  
P á g i n a  14 | 16 
I M A  - I n f o r m á t i c a  d e  M u n i c í p i o s  A s s o c i a d o s  202 4 No. Erro  Observação  
42 Município  da prestação  deve  ser preenchido  
para  prestação do serviço  local  No campo  27, quando  estiver  preenchido  
com  "Local"  o campo  28 deve  ser preenchido  
com  valor  diferente  de " 9999999 " 
43 Código do município  da prestação serviço 
inválido  Código do município campo 28 não 
encontrado.  
44 UF da prestação  deve  ser preenchido  
para  prestação  do serviço  local  No campo  27, quando  estiver  preenchido  
com  "Local"  o campo 29 deve ser  preenchido  
45 Município  exterior  prestação  do serviço  deve  
ser preenchido para prestação no  exterior  No campo 27, quando estiver 
preenchido com "Exterior", o campo 
30 deve ser preenchido  
46 Estado exterior prestação do serviço deve 
ser preenchido para prestação no exterior  No campo 27, quando estiver 
preenchido com "Exterior", o campo 
31 deve ser preenchido  
47 Pais da prestação  do serviço  deve  ser 
preenchido  para prestação no  exterior  No campo 30, quando estiver 
preenchido com "Exterior", o campo 
32 deve ser preenchido  
48 Município  do resultado  da prestação  deve  
ser preenchido para  resultado  prestação  
do serviço  local  No campo  33, quando  estiver  preenchido  com  
"Brasil"  o campo 34 deve ser preenchido com 
valor diferente de " 9999999 " 
49 Código  do município  do resultado  prestação  
serviço  inválido  Código do município campo 34 não 
encontrado.  
50 UF do resultado  da prestação  deve  ser 
preenchido  para resultado prestação do 
serviço  local  No campo  33, quando  estiver  preenchido  com  
"Brasil"  o campo 35 deve ser  preenchido  
51 Município  exterior  do resultado  prestação  
do serviço  deve ser  preenchido  para  
resultado  prestação  no exterior  No campo 33, quando estiver 
preenchido com "Exterior", o campo 
36 deve ser preenchido  
52 Estado  exterior  do resultado  prestação  do 
serviço  deve  ser preenchido  para  resultado  
prestação  no exterior  No campo 33, quando estiver 
preenchido com "Exterior", o campo 
37 deve ser preenchido  
53 Pais do resultado  da prestação  deve  ser 
preenchido  para Resultado da prestação 
no exterior  No campo 33, quando estiver 
preenchido com "Exterior", o campo 
38 deve ser preenchido  
54 Código do País do prestador é inválido  Código do país campo 22 não cadastrado.  
55 Código do País da prestação do serviço é 
inválido  Código do país campo 32 não cadastrado.  
56 Código  do País do resultado  da 
prestação  do serviço  é inválido  Código do país campo 38 não cadastrado.  
57 Informe o valor da dedução  No campo  25, quando  atividade  permite  
dedução  por mapa,  e possuir  deduções  de 
mapa,  o campo  44 deve ser  preenchido  com  
valor  maior  que zero  
58 Atividade não permite informar valor 
dedução  A atividade  do campo  25 não permite  
dedução,  o campo  44 deve  ser 
preenchido  com  zero.  
 
 
C A M P I N A S  – N F S e  – L a y o u t  d e  I m p o r t a ç ã o  d e  S e r v i ç o s  T o m a d o s  
P á g i n a  15 | 16 
I M A  - I n f o r m á t i c a  d e  M u n i c í p i o s  A s s o c i a d o s  202 4 No. Erro  Observação  
59 Não encontrado declaração de mapa de 
materiais  Para  atividade  do campo  25 com  dedução  
por mapa, valor da dedução informado, 
não foi encontrado declaração  de mapa  de 
materiais  que correspondam aos campos 
04, 08 e  44 
60 Valor da dedução diferente do valor 
deduzido na NF  No campo 44, o valor da dedução 
informado é diferente  do total  de valor  
deduzido  nesta  nota  e/ou  declaração do 
mapa de  materiais  
61 O somat ório das deduções e desconto 
incondicionado maior que valor do serviço  O somatório  do valor  dos campos  44 e 45 
não pode  ser maior ao valor do campo  43 
62 O somat ório dos descontos, retenções federais 
e ISSQN  retido maior que valor do serviço  O somatório dos campos 45, 46, 48, 49, 50, 51, 
52, 53 e 54 (ISS Retido na fonte) não pode ser 
maior que o valor do campo 43  
63 Informe o valor da base de cálculo  O campo 47 não está preenchido  
64 Base de cálculo maior que o valor do serviço  Valor  do campo  47 não pode  ser maior  que 
o Valor  do campo  43 
65 Valor  do ISS não pode  ser informado  
para  o tipo de recolhimento do 
imposto da  Nota  No campo 41, quando estiver preenchido 
com valor "NAP  - Não se aplica",  o campo  54 
deve  ser preenchido com  zero  
66 Tipo  de recolhimento  do imposto  
inválido  para  a exigibilidade da  
nota  O campo  40, quando  estiver  preenchido  
com  valor  3, 5,  6 e 7, o campo  41 deve  ser 
preenchido  com  o valor "NAP - Não se  
aplica"  
67 Obra informada não cadastrada  Código da obra do campo 26 não cadastrada.  
68 A alíquota  não deve  ser informada  
quando  não permite calcular  imposto  Para  os dados  informados  a regra  de 
tributação  não permite calcular o 
imposto, o campo 42 deve ser 
preenchido com  zero  
69 O tipo de recolhimento,  exigibilidade  e 
alíquota  não estão  de acordo com a regra de  
tributação  Os campos 40, 41 não está de acordo com a 
regra de tributação para esta nota.  
70 O valor do ISS está inválido para a alíquota 
informada  O cálculo  do valor  do campo  42 * 47 está  
inválido  para o campo  54, considerando  a 
dedução  (44) e desconto incondicionado  
(45).  
71 Alíquota informada indevidamente  "A alíquota do ISS só deve ser informada 
quando:  
O tipo do recolhimento do ISS for a recolher 
pelo prestador ou o prestador do serviço for 
optante pelo Simples Nacional ou MEI ou 
quando a exigibilidade for não  incidência . Em 
outras situações a alíquota a ser aplicada será  
determinada pela Prefeitura."  
72 Alíquota Serviços fora do intervalo de 2% e 
5% Quando o local da prestação do serviço for 
diferente deste  município,  o campo  42 deve  
ser maior  ou igual  a 2% e menor ou igual a  
5%. 
 
 
C A M P I N A S  – N F S e  – L a y o u t  d e  I m p o r t a ç ã o  d e  S e r v i ç o s  T o m a d o s  
P á g i n a  16 | 16 
I M A  - I n f o r m á t i c a  d e  M u n i c í p i o s  A s s o c i a d o s  202 4 No. Erro  Observação  
73 Alíquota Serviços inválida para o serviço 
informado  Quando o local da prestação do serviço é 
dentro do município,  a alíquota  do campo  
42 deve  ser a alíquota  do serviço/atividade  
estabelecida  pelo  município . 
74 Arquivo inválido  O arquivo  possui  registros  duplicados  
para  Número nota,  Prestador  e Serviço  
ou Atividade  
75 Código do município  do prestador inválido  Código do município campo 11 não 
encontrado.  
76 Alíquota deve ser informada  "Para  o prestador  de serviço  optante  pelo  
Simples Nacional  ou MEI ou quando  a 
exigibilidade  for Não incidência . 
O campo 42 deve ser preenchido com valor 
maior que  
zero."  
77 Configuração de atividade não encontrada  Não foi encontrado  configuração  da 
atividade  para  a data de emissão  
informada  
78 CEP do logradouro do prestador do serviço 
inexistente  Informe corretamente o do campo 15, CEP do 
prestador do serviço  
79 Local do resultado da prestação deve ser 
preenchido para local da prestação do serviço 
exterior  No campo 27, quando estiver preenchido com 
"Exterior" o campo 33 deve ser preenchido  
80 Município do resultado da prestação inválido 
para resultado prestação do serviço Exterior  No campo 33, quando estiver preenchido 
com "Exterior" o campo 34 deve ser 
preenchido com valor "9999999"  
81 UF do resultado da prestação não deve ser 
preenchido para resultado prestação do 
serviço Exterior  No campo 33, quando estiver preenchido 
com "Exterior" o campo 35 deve ser vazio  
82 Município exterior do resultado prestação do 
serviço não deve ser preenchido para 
resultado prestação no Brasil  No campo 33, quando estiver preenchido 
com "Brasil", o campo 36 deve ser vazio  
83 Estado exterior do resultado prestação do 
serviço não deve ser preenchido para 
resultado prestação no Brasil  No campo 33, quando estiver preenchido 
com "Brasil", o campo 37 deve ser vazio  
 
 
