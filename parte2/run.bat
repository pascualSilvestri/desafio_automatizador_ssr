@echo off
REM === Ir al directorio del script ===
cd /d %~dp0

REM === (Opcional) Crear/activar venv ===
IF NOT EXIST .venv (
  py -3 -m venv .venv
)
call .venv\Scripts\activate

REM === Instalar dependencias ===
python -m pip install --upgrade pip
pip install -r requirements.txt

REM === Variables de entorno (opcional, si no usa .env) ===
REM set DB_HOST=localhost
REM set DB_PORT=3306
REM set DB_USER=root
REM set DB_PASS=example
REM set DB_NAME=boxer

REM === Carpeta de salida por defecto (puede cambiarla) ===
set OUTPUT_DIR=respuestas
if not exist "%OUTPUT_DIR%" mkdir "%OUTPUT_DIR%"

REM === Ejecutar el ETL ===
python script_elt.py "%OUTPUT_DIR%"

REM === Dejar el venv activado o salir ===
REM deactivate
