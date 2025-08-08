@echo off
chcp 65001 >nul
title Aviator Bot v3.0 - Execução
echo.
echo =====================================================
echo           AVIATOR BOT v3.0 - EXECUCAO
echo =====================================================
echo.
if not exist "venv" (
  echo Ambiente virtual nao encontrado. Rode: python installer.py
  pause
  exit /b 1
)
call venv\Scripts\python.exe main.py
echo.
echo Finalizado.
pause