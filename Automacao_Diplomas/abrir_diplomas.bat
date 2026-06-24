@echo off
chcp 65001 > nul
title Abrir Diplomas

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
    for %%f in ("pdfs\*.pdf") do start "" "chrome.exe" "%%~ff"
)