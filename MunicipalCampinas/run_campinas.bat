@echo off
setlocal

echo ==========================================================
echo        INTEGRADOR NOTA JOEENSE - CAMPINAS
echo ==========================================================
echo.
echo Selecione a opcao desejada:
echo.
echo [1] Validar um Arquivo TXT (Apenas relata erros no log)
echo [2] Corrigir um Arquivo TXT (Auto-repara alinhamentos e zeros)
echo [3] Gerar um Arquivo TXT a partir de JSON
echo.

set /p opcao="Opcao (1, 2 ou 3): "

if "%opcao%"=="1" goto VALIDAR
if "%opcao%"=="2" goto CORRIGIR
if "%opcao%"=="3" goto GERAR
goto FIM

:VALIDAR
echo.
set /p arquivo="Digite o nome/caminho do arquivo TXT para Validar: "
if not exist "%arquivo%" (
    echo Erro: Arquivo nao encontrado!
    goto FIM
)
echo.
python nota_joeense_campinas.py validar "%arquivo%"
echo.
echo Log de validacao salvo em "%arquivo%.log".
goto FIM

:CORRIGIR
echo.
set /p arquivo="Digite o nome/caminho do arquivo TXT para Corrigir: "
if not exist "%arquivo%" (
    echo Erro: Arquivo nao encontrado!
    goto FIM
)
echo.
python nota_joeense_campinas.py corrigir "%arquivo%"
echo.
pause
goto FIM

:GERAR
echo.
set /p arquivo="Digite o nome/caminho do arquivo JSON base: "
if not exist "%arquivo%" (
    echo Erro: Arquivo nao encontrado!
    goto FIM
)
echo.
python nota_joeense_campinas.py gerar "%arquivo%"
echo.
goto FIM

:FIM
echo.
pause
