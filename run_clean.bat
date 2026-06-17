@echo off
setlocal enabledelayedexpansion
:: Resolve script directory
set "SCRIPT_DIR=%~dp0"
set "PY=%SCRIPT_DIR%\.venv\Scripts\python.exe"
if not exist "%PY%" (
  echo Virtualenv python not found at %PY%. Create the .venv and install requirements first.
  exit /b 1
)

set "INPUT=%~1"
if "%INPUT%"=="" set "INPUT=%SCRIPT_DIR%sample.csv"
set "OUTPUT=%~2"
if "%OUTPUT%"=="" set "OUTPUT=%SCRIPT_DIR%cleaned.csv"
set "OPEN=%~3"
nif "%OPEN%"=="" (
  "%PY%" "%SCRIPT_DIR%clean_csv.py" "%INPUT%" "%OUTPUT%"
) else (
  "%PY%" "%SCRIPT_DIR%clean_csv.py" "%INPUT%" "%OUTPUT%" %OPEN%
)
endlocal