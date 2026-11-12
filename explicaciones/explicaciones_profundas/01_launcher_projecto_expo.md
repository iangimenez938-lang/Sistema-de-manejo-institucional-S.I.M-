# 01. `projecto_expo.py` (lanzador principal)

## Qué es este archivo

Este archivo es el punto de entrada de la aplicación. Es el que se ejecuta cuando abres el programa y el que crea la ventana principal con todas las pestañas.

Su misión no es hacer cálculos en sí mismo, sino orquestar la app:

- preparar rutas,
- importar módulos internos,
- crear la interfaz principal,
- montar las pestañas,
- conectar cada sección con su builder correspondiente,
- y comprobar si hay actualizaciones al arrancar.

---

## 1. Preparación del entorno

El archivo empieza con esto:

- `import sys`
- `from pathlib import Path`
- `import tkinter as tk`
- `from tkinter import ttk`
- `from tkinter import messagebox`

Esto es importante porque la app puede ejecutarse de dos maneras:

- directamente desde el código fuente,
- o desde un ejecutable compilado con PyInstaller.

Por eso se hace esto:

```python
if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
    BASE_DIR = Path(sys._MEIPASS).resolve()
else:
    BASE_DIR = Path(__file__).resolve().parent.parent
```

### ¿Qué significa esto?

Cuando la app está empacada como `.exe`, Python se ejecuta desde un directorio temporal de PyInstaller. En ese caso, `sys._MEIPASS` apunta a la carpeta de recursos. Si no, se usa la carpeta del proyecto real.

Luego añade al `sys.path` rutas para poder hacer imports como:

```python
from general_info_app import build_general_info_ui
from real_informacion_app import build_real_informacion_ui
```

Esto es clave porque la app debe funcionar tanto en el entorno de desarrollo como en la versión compilada.

---

## 2. Importación de los módulos de la interfaz

El archivo importa los builders de cada sección:

- `build_general_info_ui`
- `build_real_informacion_ui`
- `build_creditos_ui`
- `build_matematica_ui`
- `build_quimica_ui`
- `check_for_updates`, `download_and_apply_update`

Esto refleja un patrón muy limpio: cada panel es un módulo independiente y el lanzador solo los monta dentro de la ventana principal.

Es una arquitectura modular, no una app monolítica.

---

## 3. Creación de la ventana principal

Se crea la instancia raíz:

```python
root = tk.Tk()
root.title("Calculadora Expo")
```

Luego se crea un `ttk.Notebook` para tener pestañas:

```python
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")
```

Cada pestaña es un `ttk.Frame`:

- `general_tab`
- `realinfo_tab`
- `matematica_tab`
- `quimica_tab`
- `creditos_tab`

y se agregan al notebook:

```python
notebook.add(general_tab, text="General")
notebook.add(realinfo_tab, text="RealInformacion")
notebook.add(matematica_tab, text="Matematica")
notebook.add(quimica_tab, text="Quimica")
notebook.add(creditos_tab, text="Creditos")
```

Esto es lo que hace que la aplicación tenga la apariencia de una app con varios paneles, cada uno con una responsabilidad distinta.

---

## 4. Conexión de cada sección con su UI

Cada `build_*_ui` recibe el frame de la pestaña y la raíz de la app. Por ejemplo:

```python
build_general_info_ui(general_tab, root)
build_real_informacion_ui(realinfo_tab, root)
build_matematica_ui(matematica_tab, root)
build_quimica_ui(quimica_tab, root)
build_creditos_ui(creditos_tab, root)
```

La idea es clara: cada archivo de la carpeta `app-content` genera su propia interfaz gráfica; el lanzador solo les pasa el contenedor correcto.

---

## 5. Centrado de la ventana

Después de montar todo, el archivo calcula el tamaño real de la ventana y la centra en la pantalla:

```python
root.update()
window_width = root.winfo_width()
window_height = root.winfo_height()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
```

Este paso es muy útil porque sin él la ventana puede abrirse desplazada o en una posición poco natural.

---

## 6. Verificación de actualizaciones al arrancar

La función `check_update_on_start()` se ejecuta tras 1000 ms con `root.after(1000, ...)`.

Su flujo es este:

1. llama a `check_for_updates(current_version=APP_VERSION)`,
2. si hay nueva versión, construye un mensaje,
3. pide confirmación con `messagebox.askyesno`,
4. si el usuario acepta, descarga la actualización,
5. y prepara la instalación.

Esto crea la experiencia de actualización automática sin bloquear la UI de la app principal.

---

## 7. Cómo piensa este archivo

Este módulo hace de "director de orquesta":

- no contiene la lógica específica de química o matemática,
- no guarda la información del usuario,
- no resuelve ecuaciones,
- pero sí coordina todo lo demás.

Es el archivo que conecta la arquitectura completa y hace que cada parte tenga sentido en conjunto.

---

## 8. Si quisieras ampliarlo

Si quieres añadir otra sección, el patrón correcto suele ser:

1. crear un archivo nuevo en `app-content/`,
2. definir una función `build_x_ui(frame, root)`,
3. importarla aqui,
4. crear un nuevo `ttk.Frame`,
5. añadir la pestaña con `notebook.add(...)`,
6. llamar a la función del nuevo módulo.

Ese es el punto de extensión más limpio del proyecto.
