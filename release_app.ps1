param(
    [string]$Version = "",
    [string]$OutputDir = "release"
)

# Si PowerShell bloquea scripts en Windows, ejecútalo así:
# powershell -ExecutionPolicy Bypass -File .\release_app.ps1

$ErrorActionPreference = "Stop"

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$workspaceRoot = Split-Path -Parent (Split-Path -Parent $projectDir)
$localVenvPython = Join-Path $projectDir ".venv\Scripts\python.exe"
$parentVenvPython = Join-Path $workspaceRoot ".venv\Scripts\python.exe"
$venvPython = if (Test-Path $localVenvPython) { $localVenvPython } elseif (Test-Path $parentVenvPython) { $parentVenvPython } else { $localVenvPython }

$specPath = Join-Path $projectDir "CalculadoraExpo.spec"
$versionFile = Join-Path $projectDir "version.json"
$distExe = Join-Path $projectDir "dist\CalculadoraExpo.exe"
$releaseFolder = Join-Path $projectDir $OutputDir
$releaseExe = Join-Path $releaseFolder "CalculadoraExpo.exe"

function Resolve-PythonCommand {
    if (Test-Path $venvPython) {
        return @($venvPython, "-m", "PyInstaller", "--clean", "--noconfirm", $specPath)
    }

    if (Get-Command python -ErrorAction SilentlyContinue) {
        $pythonExe = (Get-Command python).Source
        return @($pythonExe, "-m", "PyInstaller", "--clean", "--noconfirm", $specPath)
    }

    if (Get-Command py -ErrorAction SilentlyContinue) {
        $pyExe = (Get-Command py).Source
        return @($pyExe, "-3", "-m", "PyInstaller", "--clean", "--noconfirm", $specPath)
    }

    throw "Python no está disponible. Activa el entorno .venv o instala Python antes de compilar."
}

function Remove-LockedBuildArtifacts {
    $appProcess = Get-CimInstance Win32_Process -Filter "Name = 'CalculadoraExpo.exe'" -ErrorAction SilentlyContinue

    if ($appProcess) {
        foreach ($proc in $appProcess) {
            try {
                Stop-Process -Id $proc.ProcessId -Force -ErrorAction Stop
                Write-Host "Proceso detenido: $($proc.Name) (PID $($proc.ProcessId))"
            }
            catch {
                Write-Warning "No se pudo detener el proceso $($proc.ProcessId): $($_.Exception.Message)"
            }
        }
    }

    foreach ($target in @($distExe, $releaseExe)) {
        if (Test-Path $target) {
            try {
                Remove-Item $target -Force -ErrorAction Stop
                Write-Host "Archivo eliminado: $target"
            }
            catch {
                Write-Warning "No se pudo eliminar $target. Cierra la app y vuelve a intentarlo."
                throw "El EXE anterior está bloqueado por Windows. Cierra la aplicación CalculadoraExpo antes de compilar."
            }
        }
    }

    $buildDir = Join-Path $projectDir "build\CalculadoraExpo"
    if (Test-Path $buildDir) {
        Remove-Item $buildDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}

if (-not (Test-Path $specPath)) {
    throw "No se encontró CalculadoraExpo.spec en $projectDir"
}

if ($Version -ne "") {
    $normalized = $Version.Trim()
    if ($normalized -match '^\d+(\.\d+){0,2}$') {
        $parts = $normalized.Split('.')
        while ($parts.Count -lt 3) { $parts += "0" }
        $normalized = $parts -join '.'
        $manifest = Get-Content $versionFile -Raw | ConvertFrom-Json
        $manifest.version = $normalized
        $manifest | ConvertTo-Json -Depth 5 | Set-Content $versionFile -Encoding utf8
        Write-Host "Versión actualizada a $normalized"
    }
    else {
        throw "La versión debe tener formato como 1.0, 1.1 o 1.1.0"
    }
}

$manifestVersion = (Get-Content $versionFile -Raw | ConvertFrom-Json).version
Write-Host "Compilando versión $manifestVersion"

Remove-LockedBuildArtifacts

Set-Location $projectDir
$pythonCommand = Resolve-PythonCommand
& $pythonCommand[0] @($pythonCommand[1..($pythonCommand.Count - 1)]) | Out-Null

if (-not (Test-Path $distExe)) {
    throw "El EXE no se generó correctamente: $distExe"
}

New-Item -ItemType Directory -Force -Path $releaseFolder | Out-Null

if (Test-Path $releaseExe) {
    Remove-Item $releaseExe -Force
}

Copy-Item $distExe $releaseExe -Force

Write-Host "Nuevo EXE generado y reemplazado en: $releaseExe"
Write-Host "Para publicar una actualización, solo cambia la versión en version.json a 1.1, 1.2, etc."
