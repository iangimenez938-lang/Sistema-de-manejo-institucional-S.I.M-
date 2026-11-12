# 11. Plantilla reutilizable para crear una nueva materia

## Objetivo

Esta es una plantilla base para crear un nuevo módulo de materia en la aplicación, con una estructura limpia que puedes copiar y editar.

La idea es que solo tengas que cambiar:

- nombre de la materia,
- fórmulas o lógica,
- labels, entradas y resultados,
- historial y guardado,
- y la conexión desde el índice.

---

## 1. Estructura mínima recomendada

```text
app-content/
    nombre_materia/
        __init__.py
        nombre_materia_app.py
```

### Ejemplo real

```text
app-content/
    fisica/
        __init__.py
        fisica_app.py
```

---

## 2. Plantilla de archivo `__init__.py`

```python
"""Módulo de [Nombre de la materia] para Calculadora Expo."""
```

---

## 3. Plantilla base para `nombre_materia_app.py`

```python
import json
import tkinter as tk
from pathlib import Path

# ----- Ruta de almacenamiento -----
PROJECT_ROOT = Path(__file__).resolve().parents[2]
OTHER_DIR = PROJECT_ROOT / "Other"
HISTORY_FILE = OTHER_DIR / "[nombre_materia]_history.json"


def load_history():
    if not HISTORY_FILE.exists():
        return []
    try:
        loaded = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        return loaded if isinstance(loaded, list) else []
    except (OSError, ValueError, TypeError):
        return []


def save_history(history):
    try:
        OTHER_DIR.mkdir(parents=True, exist_ok=True)
        HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
    except (OSError, TypeError):
        pass


# ----- Lógica de la materia -----

def calcular_edad(valor1, valor2):
    # Cambia esta función por la lógica real de tu materia.
    return valor1 + valor2


def calcular_resultado(entrada_1, entrada_2):
    # Ejemplo base, reemplaza según la materia.
    return calcular_edad(entrada_1, entrada_2)


# ----- UI -----

def build_nombre_materia_ui(nombre_materia_tab, root=None):
    history = load_history()

    title = tk.Label(
        nombre_materia_tab,
        text="[Nombre de la materia]",
        font=("Arial", 18, "bold"),
    )
    title.pack(anchor="w", padx=12, pady=(12, 8))

    subtitle = tk.Label(
        nombre_materia_tab,
        text="Descripción breve de la materia y su uso.",
        font=("Arial", 11),
    )
    subtitle.pack(anchor="w", padx=12, pady=(0, 12))

    # Contenedor de entrada
    form = tk.Frame(nombre_materia_tab)
    form.pack(fill="x", padx=12, pady=(0, 12))

    tk.Label(form, text="Valor 1:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=4)
    value1_var = tk.StringVar(value="10")
    tk.Entry(form, textvariable=value1_var, width=18).grid(row=0, column=1, sticky="w", padx=(0, 12), pady=4)

    tk.Label(form, text="Valor 2:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=4)
    value2_var = tk.StringVar(value="5")
    tk.Entry(form, textvariable=value2_var, width=18).grid(row=1, column=1, sticky="w", padx=(0, 12), pady=4)

    result_var = tk.StringVar(value="Resultado: ")
    tk.Label(form, textvariable=result_var, font=("Arial", 11, "bold")).grid(row=2, column=0, columnspan=2, sticky="w", pady=(8, 0))

    def ejecutar_calculo():
        try:
            valor1 = float(value1_var.get())
            valor2 = float(value2_var.get())
            resultado = calcular_resultado(valor1, valor2)
            result_var.set(f"Resultado: {resultado}")

            entrada = f"{valor1} + {valor2} = {resultado}"
            history.append(entrada)
            save_history(history)

            history_listbox.delete(0, "end")
            for item in history:
                history_listbox.insert("end", item)
        except ValueError:
            result_var.set("Introduce valores numéricos válidos")

    tk.Button(form, text="Calcular", command=ejecutar_calculo, width=18).grid(row=3, column=0, columnspan=2, sticky="w", pady=(12, 0))

    # Historial
    hist_frame = tk.LabelFrame(nombre_materia_tab, text="Historial")
    hist_frame.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    history_listbox = tk.Listbox(hist_frame, height=12)
    history_listbox.pack(fill="both", expand=True, padx=8, pady=8)

    for item in history:
        history_listbox.insert("end", item)

    def limpiar_historial():
        nonlocal history
        history.clear()
        save_history(history)
        history_listbox.delete(0, "end")

    tk.Button(hist_frame, text="Limpiar historial", command=limpiar_historial).pack(anchor="w", padx=8, pady=(0, 8))

    return nombre_materia_tab
```

---

## 4. Cómo cambiarla para tu materia

Solo tienes que sustituir estas partes:

### Cambia el nombre

```python
text="[Nombre de la materia]"
```

por algo así:

```python
text="Física"
```

### Cambia la lógica

```python
def calcular_resultado(entrada_1, entrada_2):
    return calcular_edad(entrada_1, entrada_2)
```

por algo real, por ejemplo:

```python
def calcular_fuerza(masa, aceleracion):
    return masa * aceleracion
```

### Cambia los campos de entrada

```python
Value 1
Value 2
```

por:

```python
Masa
Aceleración
```

o cualquier otro conjunto de parámetros que necesites.

---

## 5. Plantilla para conectarlo al índice general

En [app-content/general_info_app.py](../../app-content/general_info_app.py) añade esto dentro del bucle:

```python
("[Nombre de la materia]", "[nombre_materia]")
```

Y luego añade la condición:

```python
if target_module == "[nombre_materia]":
    from [nombre_materia].[nombre_materia]_app import build_[nombre_materia]_ui
    build_[nombre_materia]_ui(subframe, root)
```

### Ejemplo real

```python
("Fisica", "fisica")
```

```python
if target_module == "fisica":
    from fisica.fisica_app import build_fisica_ui
    build_fisica_ui(subframe, root)
```

---

## 6. Plantilla para añadir una pestaña principal

En [projecto_expo.py](../../projecto_expo.py), crea el frame y lo añades así:

```python
[nombre_materia]_tab = ttk.Frame(notebook)
notebook.add([nombre_materia]_tab, text="[Nombre de la materia]")
build_[nombre_materia]_ui([nombre_materia]_tab, root)
```

### Ejemplo real

```python
fisica_tab = ttk.Frame(notebook)
notebook.add(fisica_tab, text="Fisica")
build_fisica_ui(fisica_tab, root)
```

---

## 7. Plantilla de una materia más profesional

Si quieres una versión más completa, usa esta estructura:

```python
import json
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox

PROJECT_ROOT = Path(__file__).resolve().parents[2]
OTHER_DIR = PROJECT_ROOT / "Other"
HISTORY_FILE = OTHER_DIR / "mi_materia_history.json"


def load_history():
    if not HISTORY_FILE.exists():
        return []
    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_history(history):
    try:
        OTHER_DIR.mkdir(parents=True, exist_ok=True)
        HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


def formula_principal(a, b):
    return a * b


def build_mi_materia_ui(tab, root=None):
    history = load_history()

    top = tk.Frame(tab)
    top.pack(fill="x", padx=12, pady=(12, 8))

    tk.Label(top, text="Mi materia", font=("Arial", 18, "bold")).pack(anchor="w")

    notebook = ttk.Notebook(tab)
    notebook.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    calculo_tab = ttk.Frame(notebook)
    historial_tab = ttk.Frame(notebook)
    notebook.add(calculo_tab, text="Cálculo")
    notebook.add(historial_tab, text="Historial")

    # Calculadora
    result_var = tk.StringVar(value="Resultado: ")
    a_var = tk.StringVar(value="10")
    b_var = tk.StringVar(value="5")

    tk.Label(calculo_tab, text="Entrada A:").grid(row=0, column=0, sticky="w", padx=8, pady=8)
    tk.Entry(calculo_tab, textvariable=a_var).grid(row=0, column=1, padx=8, pady=8)

    tk.Label(calculo_tab, text="Entrada B:").grid(row=1, column=0, sticky="w", padx=8, pady=8)
    tk.Entry(calculo_tab, textvariable=b_var).grid(row=1, column=1, padx=8, pady=8)

    tk.Label(calculo_tab, textvariable=result_var, font=("Arial", 11, "bold")).grid(row=2, column=0, columnspan=2, sticky="w", padx=8, pady=8)

    def calcular():
        try:
            a = float(a_var.get())
            b = float(b_var.get())
            resultado = formula_principal(a, b)
            result_var.set(f"Resultado: {resultado}")
            history.append(f"{a} x {b} = {resultado}")
            save_history(history)
            cargar_historial()
        except ValueError:
            messagebox.showerror("Error", "Introduce valores válidos")

    tk.Button(calculo_tab, text="Calcular", command=calcular).grid(row=3, column=0, columnspan=2, padx=8, pady=(0, 12))

    # Historial
    history_listbox = tk.Listbox(historial_tab)
    history_listbox.pack(fill="both", expand=True, padx=8, pady=8)

    def cargar_historial():
        history_listbox.delete(0, "end")
        for item in history:
            history_listbox.insert("end", item)

    cargar_historial()

    return tab
```

---

## 8. Resumen rápido

Esta plantilla sirve para:

- crear nuevas materias facilmente,
- mantener una estructura uniforme,
- separar lógica y UI,
- guardar historial de forma ordenada,
- y conectar todo con el índice general sin romper la app.

Si quieres, la siguiente cosa útil es una versión todavía más concreta: una plantilla lista para una materia de Física, con fórmulas, entradas y historial ya preparados para copiar directamente.
