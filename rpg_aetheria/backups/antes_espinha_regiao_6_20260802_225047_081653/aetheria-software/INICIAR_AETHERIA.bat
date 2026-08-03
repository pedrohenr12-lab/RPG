@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "AETHERIA_PYTHON=C:\Users\Samsung\AppData\Local\Programs\Python\Python312\python.exe"
if exist "%AETHERIA_PYTHON%" goto iniciar
where py.exe >nul 2>nul
if not errorlevel 1 (
  py.exe -3 iniciar_software.py
  goto fim
)
set "AETHERIA_PYTHON=python.exe"
:iniciar
"%AETHERIA_PYTHON%" iniciar_software.py
:fim
if errorlevel 1 (
  echo.
  echo O Aetheria encontrou um erro. A mensagem acima foi mantida para diagnostico.
  pause
)
