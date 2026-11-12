# run_projecto_expo.ps1
# Ejecuta projecto_expo.py desde el directorio del script, manejando rutas con espacios.
# Si PowerShell bloquea scripts, usa: powershell -NoProfile -ExecutionPolicy Bypass -File .\run_projecto_expo.ps1

$script = Join-Path $PSScriptRoot 'projecto_expo.py'
$workspaceRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$venvPython = Join-Path $workspaceRoot '.venv\Scripts\python.exe'

if (Test-Path $venvPython) {
    & $venvPython "$script"
} elseif (Get-Command python -ErrorAction SilentlyContinue) {
    & python "$script"
} elseif (Get-Command py -ErrorAction SilentlyContinue) {
    & py -3 "$script"
} else {
    Write-Error "Python no está disponible. Instala Python o activa el entorno .venv antes de ejecutar la app."
}
