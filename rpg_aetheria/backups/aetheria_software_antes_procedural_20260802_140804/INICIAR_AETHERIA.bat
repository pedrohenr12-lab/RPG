@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "AETHERIA_PYTHON=C:\Users\Samsung\AppData\Local\Programs\Python\Python312\python.exe"
if exist "%AETHERIA_PYTHON%" goto iniciar
set "AETHERIA_PYTHON=python"
:iniciar
"%AETHERIA_PYTHON%" iniciar_software.py
if errorlevel 1 pause
