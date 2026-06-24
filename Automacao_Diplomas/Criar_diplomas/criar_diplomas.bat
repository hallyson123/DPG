@echo off
chcp 65001 > nul
title Gerador de Diplomas PROPEPG

:: Garante que o terminal execute exatamente de dentro da pasta Criar_diplomas
cd /d "%~dp0"

echo =======================================================
echo   PASSO 1: GERANDO ARQUIVOS ODT (LIBREOFFICE)
echo =======================================================
python lote_diplomas_definitivo.py

echo.
echo =======================================================
echo   PASSO 2: CONVERTENDO PARA PDF
echo =======================================================
:: Garante que a pasta local pdfs existe antes de tentar salvar
if not exist pdfs mkdir pdfs

:: O LibreOffice agora procura e converte os arquivos .odt
"C:\Program Files\LibreOffice\program\soffice.exe" --headless --convert-to pdf --outdir pdfs docs\*.odt

echo.

:: Apaga de forma silenciosa todos os arquivos ODT temporários de dentro da pasta docs
:: if exist docs\*.odt del /Q docs\*.odt

:: apaga o database.csv da pasta
if exist "database.csv" del /Q "database.csv"

echo.
:: Cria a pasta "pdfs" na raiz (Tarefa 5) se ela não existir
if not exist "..\pdfs" mkdir "..\pdfs"

:: Copia todos os PDFs para a pasta raiz
copy /Y "pdfs\*.pdf" "..\pdfs\" > nul

echo.
:: Cria a pasta "docs" na raiz se ela não existir
if not exist "..\docs" mkdir "..\docs"

:: Copia todos os DOCS para a pasta raiz
copy /Y "docs\*.odt" "..\docs\" > nul

:: Apaga os PDFs originais da pasta atual para não acumular espaço
if exist pdfs\*.pdf del /Q pdfs\*.pdf

:: Apaga os DOCS originais da pasta atual para não acumular espaço
if exist docs\*.odt del /Q docs\*.odt

echo.
echo =======================================================
echo   Processo finalizado! Pressione qualquer tecla para fechar.   
echo =======================================================
pause > nul