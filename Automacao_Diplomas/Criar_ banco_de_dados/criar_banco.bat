@echo off
chcp 65001 > nul
title Automação

:: Executa o script principal do Python
python codigo\main.py

::copia o database.csv gerado pra pasta Criar_diplomas
@REM copy /Y "database.csv" "..\Criar_diplomas\database.csv" > nul

::copia o database.csv gerado pra pasta Verificador
copy /Y "database.csv" "..\Verificador\database.csv" > nul

::copia o livro.pdf gerado pra pasta Verificador
copy /Y "livro_registro.pdf" "..\verificador\livro_registro.pdf" > nul

:: apaga o database.csv da pasta Criar_banco_de_dados
if exist "database.csv" del /Q "database.csv"

echo.
echo =======================================================
echo   Processo finalizado! Pressione qualquer tecla para fechar.
echo =======================================================
pause > nul
