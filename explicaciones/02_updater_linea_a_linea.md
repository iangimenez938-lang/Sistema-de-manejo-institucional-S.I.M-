# `updater.py` — explicación por bloques

Este archivo se encarga de comprobar si hay una actualización disponible para la app y de aplicarla de forma automática.

## 1) Imports y configuración inicial

### Líneas 1-33

- `import json` para leer el archivo `version.json`.
- `import os` permite leer variables de entorno.
- `import re` sirve para comparar versiones tipo `1.2.3`.
- `import shutil`, `subprocess`, `sys`, `tempfile` ayudan a copiar archivos, ejecutar comandos y manejar rutas.
- `from pathlib import Path` trabaja con rutas del sistema.
- `from urllib import error, request` sirve para descargar archivos desde internet.

También hay una constante:

- `APP_NAME = "CalculadoraExpo"`

Esto identifica la app para crear archivos temporales o actualizar el ejecutable.

---

## 2) Carga de la versión local

### Líneas 35-53

La función:

- `load_app_version_from_manifest()`

lee `version.json` y devuelve la versión actual del programa.

### Qué hace exactamente

- Busca el archivo `version.json` dentro de la misma carpeta.
- Si no existe, devuelve `1.0.0` por defecto.
- Si el archivo está mal formado, también devuelve una versión segura por defecto.

Luego:

- `APP_VERSION = load_app_version_from_manifest()`

guarda la versión actual en una variable global que utilizará el resto del programa.

---

## 3) Comparación de versiones

### Líneas 55-85

Estas funciones comparan versiones:

- `parse_version(version)`
- `is_newer_version(remote_version, local_version)`

### Ejemplo

Si la versión remota es `2.0.0` y la local es `1.5.0`, entonces hay una actualización disponible.

La lógica funciona así:

- separa los números,
- convierte cada parte a entero,
- compara cada bloque de la versión,
- devuelve si la remota es mayor que la local.

---

## 4) Buscar el manifiesto de versión

### Líneas 87-129

Hay dos funciones importantes:

- `_candidate_manifest_paths()`
- `_candidate_manifest_urls()`

### Qué hacen

- Buscan el archivo `version.json` local o cercano al ejecutable.
- También buscan una URL remota configurable mediante variables de entorno.

Las variables de entorno son cosas como:

- `CALCULADORA_EXPO_UPDATE_URL`
- `EXPO_UPDATE_URL`

Esto permite cambiar la URL de actualización sin tocar el código.

---

## 5) Leer el JSON desde archivo o internet

### Líneas 131-173

- `_load_json_from_file(path)`
- `_fetch_json_from_url(url)`

Estas dos funciones intentan leer un archivo JSON: uno desde disco y otro desde una web.

### Importante

- solo aceptan URLs con `http://` o `https://`
- si el JSON está mal formado, devuelven `None`
- si la descarga falla, también devuelven `None`

---

## 6) Resolver el manifiesto de actualización

### Líneas 175-194

La función:

- `read_update_manifest()`

intenta leer el manifiesto así:

1. busca archivos locales,
2. si no encuentra, intenta descargar la URL remota,
3. si consigue un JSON válido, lo devuelve.

Si no hay comprobación posible, devuelve `None`.

---

## 7) Verificar si hay actualización

### Líneas 196-221

La función:

- `check_for_updates(current_version=None)`

devuelve un diccionario con esta estructura:

- `has_update`
- `current_version`
- `latest_version`
- `download_url`
- `notes`
- `error`

Esto le sirve a la app para decidir si mostrar un cuadro de diálogo al usuario.

---

## 8) Descargar el archivo de actualización

### Líneas 223-249

La función:

- `_download_file_to_path(download_url, destination_path)`

descarga el archivo de actualización a una ruta temporal.

### Tipos de descarga

- si la URL es web, usa `urllib.request.urlopen()`
- si la URL es local, usa `shutil.copy2()`

Esto permite actualizar desde internet o desde una copia local.

---

## 9) Programar la instalación

### Líneas 251-286

La función:

- `schedule_update_install(new_executable_path, current_executable_path=None)`

crea un `.bat` con instrucciones para:

1. copiar el nuevo ejecutable sobre el actual,
2. reiniciar la app,
3. borrar el archivo temporal.

Esto es clave porque la app no se puede reemplazar mientras está ejecutándose. Por eso se prepara un script para ejecutarse después.

---

## 10) Descarga + aplica actualización

### Líneas 288-301

La función:

- `download_and_apply_update(download_url, current_executable_path=None)`

combina los pasos:

1. descarga el archivo al directorio temporal,
2. prepara la actualización,
3. devuelve `True` o `False` según el resultado.

---

## Resumen rápido

`updater.py` hace esto:

- lee la versión local,
- busca la versión remota,
- compara si hay una nueva,
- descarga el ejecutable nuevo,
- prepara una instalación automática,
- reinicia la app después.

Es el componente que permite que la herramienta se actualice sin tener que reinstalarla manualmente.

---

## Ejemplos reales sacados del código

### 1) Cargar la versión desde el manifest

```python
def load_app_version_from_manifest():
    base_dir = Path(__file__).resolve().parent
    manifest_path = base_dir / "version.json"
    if not manifest_path.exists():
        return "1.0.0"

    try:
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return "1.0.0"

    if not isinstance(payload, dict):
        return "1.0.0"

    version = payload.get("version")
    return str(version) if version else "1.0.0"
```

Esto significa que la app toma la versión desde `version.json` en la misma carpeta. Si ese archivo no existe o está roto, usa `1.0.0` como valor seguro.

### 2) Comparar versiones

```python
def parse_version(version):
    if version is None:
        return ()
    digits = re.findall(r"\d+", str(version))
    if not digits:
        return ()
    return tuple(int(part) for part in digits)


def is_newer_version(remote_version, local_version):
    remote_parts = parse_version(remote_version)
    local_parts = parse_version(local_version)
    max_len = max(len(remote_parts), len(local_parts))
    if len(remote_parts) < max_len:
        remote_parts = remote_parts + (0,) * (max_len - len(remote_parts))
    if len(local_parts) < max_len:
        local_parts = local_parts + (0,) * (max_len - len(local_parts))
    return remote_parts > local_parts
```

La comparación se hace número por número. Por ejemplo:

- local: `1.4.0`
- remota: `1.5.0`

Entonces `1.5.0 > 1.4.0` y la app dira que hay actualización.

### 3) Ver si hay una actualización disponible

```python
def check_for_updates(current_version=None):
    current_version = current_version or APP_VERSION
    manifest = read_update_manifest()
    if not manifest:
        return {
            "has_update": False,
            "current_version": current_version,
            "latest_version": current_version,
            "download_url": "",
            "notes": "",
            "error": "No update manifest found.",
        }
```

Esto devuelve un diccionario con toda la información que necesita la UI para avisar al usuario.

### 4) Descargar el archivo nuevo

```python
def _download_file_to_path(download_url, destination_path):
    if not download_url:
        return False
    destination = Path(destination_path)
    destination.parent.mkdir(parents=True, exist_ok=True)

    if download_url.startswith(("http://", "https://")):
        try:
            with request.urlopen(download_url, timeout=20) as response, open(destination, "wb") as file_handle:
                shutil.copyfileobj(response, file_handle)
            return True
        except (error.URLError, error.HTTPError, TimeoutError, OSError):
            return False
```

Este bloque es el que realmente baja el ejecutable nuevo desde internet.

### 5) Preparar instalación automática

```python
def schedule_update_install(new_executable_path, current_executable_path=None):
    current_executable = Path(current_executable_path or sys.executable).resolve()
    downloaded_exe = Path(new_executable_path).resolve()
    if not downloaded_exe.exists():
        return False

    batch_path = current_executable.parent / "update_calculadora_expo.bat"
    batch_text = (
        "@echo off\n"
        "setlocal\n"
        "ping -n 4 127.0.0.1 > NUL\n"
        f"copy /Y \"{downloaded_exe}\" \"{current_executable}\" > NUL\n"
        f"start \"\" \"{current_executable}\"\n"
        f"del /f /q \"{batch_path}\"\n"
        "exit /b 0\n"
    )
```

Esto crea un archivo `.bat` que se ejecuta más tarde para sustituir el programa actual por la nueva versión.

### Cómo modificarlo en el futuro

Si quieres cambiar la lógica de actualización, normalmente tocarás:

1. `DEFAULT_REMOTE_UPDATE_URL` para cambiar la URL,
2. `check_for_updates()` para cambiar qué se valida,
3. `schedule_update_install()` para cambiar cómo se instala la nueva versión,
4. `download_and_apply_update()` para cambiar el flujo completo.

Es una parte sencilla, pero muy importante: si cambias la URL o el formato del JSON, tendrás que mantener la misma estructura de campos.
