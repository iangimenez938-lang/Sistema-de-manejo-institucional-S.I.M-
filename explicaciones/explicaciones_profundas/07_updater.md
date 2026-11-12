# 07. `updater.py`

## Qué hace este archivo

Este módulo es el sistema de actualización automática de la aplicación.

Su misión es comprobar si existe una versión nueva del programa en un manifiesto remoto, descargarla si hace falta, y dejarla lista para instalarse sin que el usuario tenga que hacerlo manualmente.

En un proyecto real, esto es muy útil porque permite publicar correcciones y mejoras sin que el usuario tenga que reinstalar el `.exe` a mano.

---

## 1. La versión actual

La variable `APP_VERSION` se obtiene desde `version.json`:

```python
APP_NAME = "CalculadoraExpo"

def load_app_version_from_manifest():
    base_dir = Path(__file__).resolve().parent
    manifest_path = base_dir / "version.json"
```

Esto asegura que la app tenga una versión registrada en el propio proyecto y que pueda compararla con una versión remota.

---

## 2. Comparación de versiones

La lógica de comparación se hace con `parse_version()` y `is_newer_version()`.

- `parse_version()` extrae números de una cadena como `1.2.3` o `v2.4`,
- devuelve una tupla de enteros, por ejemplo `(1, 2, 3)`,
- y luego compara dos versiones.

Esto permite comparar sin depender de cadenas complejas.

---

## 3. Dónde buscar el manifiesto

La app intenta localizar un archivo `version.json` en varios sitios:

- el directorio del proyecto,
- la carpeta de instalación del programa,
- y, si no existe, en una URL remota.

Hay dos funciones principales:

- `_candidate_manifest_paths()`
- `_candidate_manifest_urls()`

La primera busca archivos locales. La segunda intenta encontrar un enlace remoto y además puede leer una URL configurada por variables de entorno.

Esto es una buena práctica porque la app puede adaptarse a distintos entornos y mecanismos de despliegue.

---

## 4. Carga del JSON remoto

La función `read_update_manifest()` intenta este flujo:

1. buscar un archivo local,
2. si no existe, buscar URL remota,
3. descargar JSON,
4. verificar que sea un diccionario válido.

La carga de la URL usa `urllib.request.urlopen` y hace una lectura segura con timeout:

```python
with request.urlopen(url, timeout=8) as response:
    content = response.read()
```

Esto evita que la comprobación de actualización quede colgada en caso de un problema de red.

---

## 5. `check_for_updates()`

Esta es la función que usa la app principal para saber si hay que notificar al usuario.

Devuelve un diccionario con:

- `has_update`
- `current_version`
- `latest_version`
- `download_url`
- `notes`
- `error`

Es muy útil porque el lanzador solo tiene que comprobar una estructura y decidir si mostrar un aviso.

---

## 6. Descarga del archivo actualizado

La función `_download_file_to_path(download_url, destination_path)` hace la descarga real:

- si la URL es HTTP/HTTPS, usa `urlopen` para guardar el contenido,
- si es una ruta local, hace un `shutil.copy2`.

Esto ofrece flexibilidad para distintas distribuciones del programa.

---

## 7. Instalación programada

La función `schedule_update_install(new_executable_path, current_executable_path=None)` crea un `.bat` temporal que:

1. espera unos segundos,
2. reemplaza el ejecutable actual por el nuevo,
3. vuelve a abrir la aplicación,
4. elimina el script de actualización.

La idea es que la actualización no se aplique mientras la app está en uso; se hace de forma segura al cerrar/reabrir.

Esto es una estrategia muy práctica porque no suele ser seguro reemplazar un `.exe` activo en Windows.

---

## 8. Qué hace `download_and_apply_update()`

Esta es la función de alto nivel. Su flujo es:

1. descargar un archivo temporal,
2. validar que exista,
3. llamar a `schedule_update_install`,
4. devolver `True` si el proceso se preparó bien.

Es la función que usa la pantalla principal cuando el usuario confirma la actualización.

---

## 9. Por qué este archivo importa mucho

Aunque el usuario no lo vea siempre, este módulo hace que la app sea más sostenible.

Permite:

- corregir bugs sin re-entregar el programa completo,
- mejorar la app sin que el usuario tenga que buscar una versión nueva,
- mantener actualizada la distribución final del proyecto.

Es una pieza importantísima si la app se va a usar fuera del entorno de desarrollo.

---

## 10. Resumen corto

`updater.py` es un pequeño sistema de despliegue inteligente: comprueba una versión, descarga el paquete, y prepara una instalación segura en la siguiente ejecución.
