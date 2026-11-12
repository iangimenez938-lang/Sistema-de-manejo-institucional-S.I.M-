@echo off
REM run_projecto_expo.bat - ejecuta projecto_expo.py desde este directorio
REM Uso: doble clic o desde cmd: run_projecto_expo.bat

SET SCRIPT_DIR=%~dp0

REM Intentar python en PATH, si falla usar el lanzador py
python "%SCRIPT_DIR%projecto_expo.py" 2>nul || py -3 "%SCRIPT_DIR%projecto_expo.py"
