@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "AETHERIA_PYTHON=C:\Users\Samsung\AppData\Local\Programs\Python\Python312\python.exe"
if exist "%AETHERIA_PYTHON%" goto instalar
set "AETHERIA_PYTHON=python"
:instalar
echo Instalando a interface e o conector MySQL...
"%AETHERIA_PYTHON%" -m pip install -r requirements.txt
echo.
echo Instalacao concluida. Agora execute INICIAR_AETHERIA.bat.
pause
