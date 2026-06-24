@echo off
chcp 65001 > nul
title remover tudo

:: Apaga os PDFs originais da pasta atual para não acumular espaço
if exist pdfs\*.pdf del /Q pdfs\*.pdf

:: Apaga os DOCS originais da pasta atual para não acumular espaço
if exist docs\*.odt del /Q docs\*.odt

echo.
echo =======================================================
echo                   TUDO FOI REMOVIDO
echo =======================================================
pause