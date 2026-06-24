@echo off
chcp 65001 > nul
title Verificador

:: Executa o script principal do Python
python main.py

::copia o database.csv gerado pra pasta Verificador
copy /Y "database_corrigido.csv" "..\criar_diplomas\database.csv" > nul

:: apaga o database.csv da pasta Verificador
if exist "database_corrigido.csv" del /Q "database_corrigido.csv"

:: apaga o database.csv da pasta Verificador
if exist "database.csv" del /Q "database.csv"

:: apaga o livro da pasta Verificador
if exist "livro_registro.pdf" del /Q "livro_registro.pdf"

echo.
echo =======================================================
echo   Processo finalizado! Pressione qualquer tecla para fechar.
echo =======================================================
pause > nul
