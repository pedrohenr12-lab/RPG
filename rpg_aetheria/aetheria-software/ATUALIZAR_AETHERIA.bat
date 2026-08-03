@echo off
setlocal
chcp 65001 >nul
cd /d "%~dp0"
title Aetheria - Atualizador do Nucleo Persistente v2
set "AETHERIA_SCRIPT=%~dp0ATUALIZAR_AETHERIA.py"
set "AETHERIA_LOG=%~dp0ATUALIZACAO_AETHERIA.log"
set "AETHERIA_PYTHON_EXE=C:\Users\Samsung\AppData\Local\Programs\Python\Python312\python.exe"
if defined AETHERIA_PYTHON_OVERRIDE set "AETHERIA_PYTHON_EXE=%AETHERIA_PYTHON_OVERRIDE%"

echo ================================================================
echo AETHERIA - ATUALIZADOR DO NUCLEO PERSISTENTE V2
echo ================================================================
echo.

if not exist "%AETHERIA_SCRIPT%" goto script_missing
if exist "%AETHERIA_PYTHON_EXE%" goto run_python_exe

where py >nul 2>nul
if not errorlevel 1 goto run_py_launcher

where python >nul 2>nul
if not errorlevel 1 goto run_python_command

echo ERRO: Python nao foi encontrado.
echo Execute INSTALAR_DEPENDENCIAS.bat e tente novamente.
goto failed

:run_python_exe
echo Python: %AETHERIA_PYTHON_EXE%
"%AETHERIA_PYTHON_EXE%" -X utf8 "%AETHERIA_SCRIPT%" %* > "%AETHERIA_LOG%" 2>&1
goto show_result

:run_py_launcher
echo Python: py -3.12
py -3.12 -X utf8 "%AETHERIA_SCRIPT%" %* > "%AETHERIA_LOG%" 2>&1
goto show_result

:run_python_command
echo Python: python
python -X utf8 "%AETHERIA_SCRIPT%" %* > "%AETHERIA_LOG%" 2>&1
goto show_result

:show_result
set "AETHERIA_EXIT=%ERRORLEVEL%"
type "%AETHERIA_LOG%"
echo.
if "%AETHERIA_EXIT%"=="0" goto success
echo A atualizacao terminou com erro %AETHERIA_EXIT%.
echo O diagnostico completo foi salvo em:
echo %AETHERIA_LOG%
goto failed

:script_missing
echo ERRO: o atualizador Python nao esta ao lado deste arquivo.
echo Arquivo esperado: %AETHERIA_SCRIPT%
goto failed

:success
echo ATUALIZACAO CONCLUIDA. Agora abra INICIAR_AETHERIA.bat na pasta instalada.
pause
exit /b 0

:failed
echo.
echo A atualizacao NAO foi instalada. A janela ficara aberta para leitura.
pause
exit /b 1
