# Cómo crear un EXE y cómo actualizar la aplicación

Este archivo recoge la parte práctica del despliegue: cómo generar un ejecutable Windows, cómo dejarlo listo para distribuir, y cómo hacer que la app se actualice sola desde una nueva versión.

## 1. Requisitos previos

Para crear el EXE necesitas:

- Python instalado.
- El entorno virtual del proyecto o un Python con acceso al proyecto.
- PyInstaller instalado.
- El archivo de especificación `CalculadoraExpo.spec` presente en la raíz del proyecto.

El script principal de compilación es:

- `release_app.ps1`

Si lo ejecutas desde PowerShell, normalmente será suficiente:

```powershell
powershell -ExecutionPolicy Bypass -File .\release_app.ps1
```

También se puede ejecutar directamente si la política de PowerShell lo permite:

```powershell
.\release_app.ps1
```

## 2. Qué hace `release_app.ps1`

El script hace varias cosas en orden:

1. Comprueba que existe `CalculadoraExpo.spec`.
2. Busca Python en el entorno `.venv` o en el sistema.
3. Ejecuta PyInstaller con la especificación del proyecto.
4. Genera el EXE en `dist\CalculadoraExpo.exe`.
5. Crea la carpeta `release/` si no existe.
6. Copia el EXE final a `release\CalculadoraExpo.exe`.
7. Si el EXE anterior está bloqueado por Windows, intenta cerrarlo antes de reemplazarlo.

Eso convierte el proyecto en una build lista para enviarse a otra máquina o para publicarla como actualización.

## 3. Cómo compilar el EXE

La forma recomendada es esta:

```powershell
cd ruta\del\proyecto
powershell -ExecutionPolicy Bypass -File .\release_app.ps1
```

El script no necesita más argumentos si usas la versión actual del `version.json`.

También admite una versión manual al lanzar el script:

```powershell
powershell -ExecutionPolicy Bypass -File .\release_app.ps1 -Version 1.3.0
```

Esto actualiza el archivo `version.json` antes de compilar.

## 4. Importancia de `CalculadoraExpo.spec`

El archivo `.spec` define cómo PyInstaller construye el programa. En este proyecto se usa para:

- incluir la app principal,
- empaquetar recursos,
- generar el nombre del EXE,
- controlar la salida dentro de `dist`.

Si cambias el nombre de la aplicación o la ruta principal, también deberías revisar:

- `CalculadoraExpo.spec`
- `release_app.ps1`
- `version.json`

## 5. Cómo se configura la versión

La aplicación guarda la versión en `version.json`:

```json
{
  "version": "1.2.0",
  "download_url": "release/CalculadoraExpo-1.2.0.exe",
  "notes": "Versión de lanzamiento con actualización automática y script de despliegue."
}
```

### Campos importantes

- `version`: versión actual de la app.
- `download_url`: la ruta o URL a la nueva versión.
- `notes`: texto informativo para mostrar al usuario.

Para lanzar una nueva versión, normalmente se cambia la versión en `version.json` o se usa el parámetro `-Version` del script.

Ejemplo:

```json
"version": "1.3.0"
```

## 6. Cómo funciona la actualización automática

La lógica de actualización está en `updater.py` y se invoca desde `projecto_expo.py`.

### Flujo general

1. La app inicia.
2. Comprueba si existe una nueva versión.
3. Lee la versión local y la versión remota desde `version.json`.
4. Si la remota es mayor, pregunta al usuario si quiere actualizar.
5. Si acepta, descarga el `.exe` nuevo.
6. Prepara una sustitución segura del archivo ejecutable.
7. Reinicia la aplicación con la nueva versión.

El punto clave es que Windows normalmente no permite reemplazar un EXE que está en uso. Por eso `updater.py` crea un archivo `.bat` temporal para hacer el cambio cuando la app ya no está ejecutándose.

## 7. Cómo publicar una actualización

El proceso recomendado es este:

1. Mejora o corrige el código.
2. Prueba la app.
3. Genera un nuevo EXE con `release_app.ps1`.
4. Cambia la versión en `version.json`.
5. Guarda el nuevo EXE en la carpeta o URL esperada por la actualización.
6. Publica la nueva versión.

Ejemplo de una versión nueva:

```json
{
  "version": "1.3.0",
  "download_url": "https://github.com/usuario/repositorio/releases/download/v1.3.0/CalculadoraExpo.exe"
}
```

Si `download_url` es una ruta local, hay que dejarla relativa al directorio de la aplicación. Si es una URL remota, debe apuntar al archivo correcto en GitHub, Dropbox, servidor web o similar.

## 8. Buenas prácticas para mantener la app viva

- No cambies la versión sin querer; cada versión debe corresponder a un cambio real.
- Guarda siempre la nueva build en la carpeta o destino que coincida con `download_url`.
- Prueba la actualización en una copia antes de publicarla en producción.
- Cierra la app antes de compilar si Windows está bloqueando el EXE anterior.
- Mantén `version.json` sincronizado con lo que publicas.

## 9. Ruta rápida de referencia

Si solo quieres seguir el camino más corto:

```powershell
# 1. Compilar
powershell -ExecutionPolicy Bypass -File .\release_app.ps1

# 2. Subir el nuevo EXE a la ubicación del release

# 3. Cambiar la versión
# editar version.json

# 4. Probar la actualización ejecutando la app
```

## 9.1. Script de PowerShell para copiar y pegar

Si quieres una versión lista para pegar en PowerShell y no tener que recordar pasos, usa este bloque:

```powershell
Set-Location "C:\Users\pc\OneDrive\Documents\tareas de taller\lab.programacion\proyectoEXPO"

if (-not (Test-Path ".\.venv")) {
    py -m venv .venv
}

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
python -m pip install pyinstaller pyttsx3

.\.venv\Scripts\python.exe -m PyInstaller --clean --noconfirm .\CalculadoraExpo.spec

New-Item -ItemType Directory -Force -Path .\release | Out-Null
Copy-Item .\dist\CalculadoraExpo.exe .\release\CalculadoraExpo.exe -Force

Write-Host "EXE generado en: .\release\CalculadoraExpo.exe"
Write-Host "Si publicas una nueva versión, cambia la versión en version.json"
```

> Si quieres cambiar la versión antes de publicar, edita `version.json` y luego repite el bloque.

## 10. Resumen

El flujo completo es:

- `release_app.ps1` genera el EXE.
- `CalculadoraExpo.spec` define la construcción.
- `version.json` marca la versión y la URL de descarga.
- `updater.py` comprueba si hay una nueva versión y la instala.

Con esto, la aplicación queda preparada tanto para empaquetarse como para actualizarse sin reinstalarla manualmente.
