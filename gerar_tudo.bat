@echo off
chcp 65001 > nul
title Automação Completa PROPEPG

echo =======================================================
echo                  AUTOMAÇÃO COMPLETA
echo =======================================================

echo.
echo [PASSO 1/2] Chamando o extrator de banco de dados...
:: Vai direto para a pasta do banco e roda o bat lá de dentro, esperando ele terminar
@REM start /wait "" /d "C:\Users\hally\Downloads\Automatização de diplomas\Criar_ banco_de_dados" Criar_banco.bat
start /wait "" /d "%~dp0Criar_ banco_de_dados" Criar_banco.bat

echo.
echo [PASSO 2/3] Chamando o verificador...
:: Vai direto para a pasta do banco e roda o bat lá de dentro, esperando ele terminar
start /wait "" /d "%~dp0Verificador" Verificar.bat

echo.
echo [PASSO 3/3] Chamando o gerador de diplomas...
:: Vai direto para a pasta de diplomas e roda o bat lá de dentro, esperando ele terminar
start /wait "" /d "%~dp0Criar_diplomas" Criar_diplomas.bat

echo.
echo =======================================================
echo             VISUALIZAÇÃO DOS DOCUMENTOS
echo =======================================================
:: Faz a pergunta ao usuário e guarda a resposta na variável REPOSTA
set /p "RESPOSTA=Deseja abrir todos os PDFs gerados no Google Chrome? (S/N): "

:: Se a resposta for S ou s, força a abertura usando o executável do Chrome
if /I "%RESPOSTA%"=="S" (
    echo Abrindo PDFs no Google Chrome...
    :: Busca na pasta pdfs que o Criar_diplomas.bat acabou de jogar na raiz
    @REM for %%f in ("pdfs\*.pdf") do start "" "chrome.exe" "%%~ff"
    for %%f in ("pdfs\*.pdf") do start "" "chrome.exe" "%%~ff"
)

echo.
echo =======================================================
echo    TODAS AS ETAPAS FORAM CONCLUÍDAS COM SUCESSO!
echo =======================================================
pause