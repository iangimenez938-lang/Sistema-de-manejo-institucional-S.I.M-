# 10. Guía práctica: cómo añadir una nueva materia (ejemplo: Física)

## Objetivo

En esta guía vas a aprender a añadir una materia nueva a la aplicación siguiendo el mismo patrón que usa Matemática y Química.

Vamos a usar un ejemplo concreto: crear una pestaña llamada "Física".

La idea es que entiendas no solo el código, sino también el pensamiento arquitéctonico detrás de la decisión.

---

## 1. Qué implica añadir una nueva materia

Una materia nueva no es simplemente "otra pestaña más".

Debe tener estas partes:

1. un módulo propio
2. una función `build_x_ui(...)`
3. una estructura visual para la interfaz
4. un historial si hace falta
5. almacenamiento si hace falta
6. conexión desde el índice general
7. conexión desde la ventana principal si quieres que exista como pestaña principal

Si sigues ese patrón, la app no se rompe ni se vuelve caótica.

---

## 2. Estructura recomendada para una nueva materia

La estructura más ordenada es esta:

```text
app-content/
    fisica/
        __init__.py
        fisica_app.py
```

O incluso más simple:

```text
app-content/
    fisica_app.py
```

La elección depende de si quieres una carpeta dedicada o un único archivo.

Para este proyecto, la opción más consistente con la estructura actual es usar una carpeta, porque Matemática y Química ya están organizadas así.

---

## 3. Crear la carpeta y el archivo

Primero crea una carpeta llamada `fisica` dentro de `app-content`.

Y dentro crea:

- `__init__.py`
- `fisica_app.py`

### `__init__.py`

Este archivo puede quedar vacío o con un comentario simple:

```python
"""Módulo de física para la aplicación Calculadora Expo."""
```

Eso basta para que Python lo interprete como paquete.

---

## 4. Crear la función principal del módulo

Dentro de `fisica_app.py` debes definir la función base:

```python
import tkinter as tk
from tkinter import ttk


def build_fisica_ui(fisica_tab, root=None):
    title = tk.Label(fisica_tab, text="Física", font=("Arial", 18, "bold"))
    title.pack(anchor="w", padx=12, pady=(12, 8))

    content = tk.Frame(fisica_tab)
    content.pack(fill="both", expand=True, padx=12, pady=(0, 12))

    tk.Label(content, text="Aquí va la calculadora, fórmulas o herramientas de física.",
             font=("Arial", 12)).pack(anchor="w")

    return fisica_tab
```

### ¿Qué hace esta función?

- recibe el frame donde se va a dibujar la materia,
- monta la interfaz,
- y devuelve el frame para que el sistema la pueda integrar.

Ese patrón es el que usa el resto de módulos.

---

## 5. Conectar la materia en el índice general

Ahora hay que decirle a [app-content/general_info_app.py](../../app-content/general_info_app.py) que existe una nueva categoría.

En el bucle principal se ve algo de este estilo:

```python
for label, target_module in [
    ("Matematica", "matematica"),
    ("Quimica", "quimica"),
    ("RealInformacion", "realinfo"),
    ("Creditos", "creditos"),
]:
```

Debes ampliarlo para incluir Física:

```python
for label, target_module in [
    ("Matematica", "matematica"),
    ("Quimica", "quimica"),
    ("Fisica", "fisica"),
    ("RealInformacion", "realinfo"),
    ("Creditos", "creditos"),
]:
```

Y luego añadir el caso:

```python
if target_module == "fisica":
    from fisica.fisica_app import build_fisica_ui
    build_fisica_ui(subframe, root)
```

Con eso, la pantalla general ya tendrá acceso a la materia nueva.

---

## 6. Conectar la materia desde la ventana principal

Si quieres que la materia sea una pestaña principal más en la ventana grande, debes editar [projecto_expo.py](../../projecto_expo.py).

Se hace así:

```python
fisica_tab = ttk.Frame(notebook)
notebook.add(fisica_tab, text="Fisica")
```

Y luego:

```python
build_fisica_ui(fisica_tab, root)
```

Con todo eso, la nueva materia quedará visible como una pestaña de nivel superior.

---

## 7. Cómo pensar en la interfaz de la nueva materia

La mejor estructura para una materia es separar por bloques internos:

### Bloque 1: cabecera

- título
- breve descripción

### Bloque 2: herramientas o formulario

- entrada de datos
- botones
- opciones

### Bloque 3: resultados

- texto del resultado
- labels
- campos de salida

### Bloque 4: historial

- lista de operaciones o cálculos
- botón de borrar o cargar

### Bloque 5: notas o explicación

- para documentar fórmulas, pasos o procedimientos

Por ejemplo, una pantalla de Física puede tener:

- cálculo de fuerza: `F = m * a`
- cálculo de presión: `P = F / A`
- historial de cálculos
- notas de teoría

---

## 8. Añadir historial a la nueva materia

Este patrón se ve en Matemática y en otros módulos.

Si quieres que la materia tenga historial, necesitas:

1. una lista de Python, ejemplo `history = []`
2. un `Listbox` para mostrarlo
3. una función para añadir entradas
4. una función para guardar en JSON
5. una función para cargar al inicio

Ejemplo:

```python
import json
from pathlib import Path

HISTORY_FILE = Path(__file__).resolve().parent.parent / "Other" / "fisica_history.json"


def load_fisica_history():
    if not HISTORY_FILE.exists():
        return []
    try:
        data = json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except Exception:
        return []


def save_fisica_history(items):
    try:
        HISTORY_FILE.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass
```

Luego en la UI:

```python
history_listbox = tk.Listbox(frame)
history_listbox.pack(fill="both", expand=True)
```

Cuando el usuario calcula algo:

```python
entry = "F = 10 * 2 -> 20 N"
history.append(entry)
history_listbox.insert("end", entry)
save_fisica_history(history)
```

Esto hace que el historial persista aunque la app se cierre.

---

## 9. Cómo hacer cálculos en la nueva materia

La mejor idea es que cada materia tenga una lógica separada.

Por ejemplo, para Física podrías definir funciones así:

```python
def calcular_fuerza(masa, aceleracion):
    return masa * aceleracion


def calcular_presion(fuerza, area):
    if area == 0:
        raise ValueError("El área no puede ser cero.")
    return fuerza / area
```

Y luego desde la UI haces:

```python
resultado = calcular_fuerza(masa, aceleracion)
label_resultado.config(text=f"Fuerza: {resultado} N")
```

Esto separa claramente:

- lógica matemática/física
- interfaz gráfica
- almacenamiento

Es un diseño muy limpio.

---

## 10. Cómo no romper la arquitectura

Cuando añadas una nueva materia, evita estas cosas:

- poner cálculo y UI todo en el mismo archivo principal,
- duplicar código de otras materias sin entenderlo,
- guardar datos sin una estructura clara,
- mezclar navegación, lógica y almacenamiento,
- crear una pestaña nueva sin hacerla modular.

La regla general es:

> cada materia debe ser un mini-módulo independiente dentro del sistema global.

---

## 11. Ejemplo completo de estructura mínima

Un ejemplo mínimo de una nueva materia podría quedar así:

```python
# fisica/fisica_app.py
import json
import tkinter as tk
from pathlib import Path

HISTORY_FILE = Path(__file__).resolve().parent.parent / "Other" / "fisica_history.json"


def load_fisica_history():
    if not HISTORY_FILE.exists():
        return []
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def save_fisica_history(history):
    try:
        HISTORY_FILE.write_text(json.dumps(history, ensure_ascii=False), encoding="utf-8")
    except Exception:
        pass


def calcular_fuerza(masa, aceleracion):
    return masa * aceleracion


def build_fisica_ui(fisica_tab, root=None):
    history = load_fisica_history()

    title = tk.Label(fisica_tab, text="Física", font=("Arial", 18, "bold"))
    title.pack(anchor="w", padx=12, pady=(12, 8))

    result_var = tk.StringVar(value="Resultado: ")
    masa_var = tk.StringVar(value="10")
    aceleracion_var = tk.StringVar(value="2")

    form = tk.Frame(fisica_tab)
    form.pack(fill="x", padx=12, pady=8)

    tk.Label(form, text="Masa:").grid(row=0, column=0, padx=4, pady=4)
    tk.Entry(form, textvariable=masa_var).grid(row=0, column=1, padx=4, pady=4)

    tk.Label(form, text="Aceleración:").grid(row=1, column=0, padx=4, pady=4)
    tk.Entry(form, textvariable=aceleracion_var).grid(row=1, column=1, padx=4, pady=4)

    def calcular():
        try:
            masa = float(masa_var.get())
            a = float(aceleracion_var.get())
            valor = calcular_fuerza(masa, a)
            result_var.set(f"Resultado: {valor} N")
            history.append(f"{masa} * {a} = {valor}")
            save_fisica_history(history)
        except Exception:
            result_var.set("Introduce valores válidos")

    tk.Button(form, text="Calcular", command=calcular).grid(row=2, column=0, columnspan=2, pady=8)
    tk.Label(form, textvariable=result_var).grid(row=3, column=0, columnspan=2, pady=4)

    return fisica_tab
```

Esto ya te da una base funcional muy clara.

---

## 12. Siguiente paso recomendado

Si quieres, lo mejor es que te haga una segunda guía aún más útil:

- una versión de ejemplo completa de una materia nueva con:
  - UI visual profesional,
  - historial persistente,
  - carpeta dentro de `app-content`,
  - conexión desde `general_info_app.py`,
  - y conexión desde `projecto_expo.py`.

También puedo dejarte el código exacto listo para copiar en tu proyecto, no solo la explicación conceptual.
