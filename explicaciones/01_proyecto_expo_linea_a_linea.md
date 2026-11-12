# `projecto_expo.py` — explicación por bloques

Este archivo es la parte principal de la app. Tiene 3 grandes objetivos:

1. Crear la interfaz visual con Tkinter.
2. Resolver cálculos y ecuaciones.
3. Gestionar una base de datos de elementos químicos y contenidos educativos.

## 1) Bloque inicial: imports y creación de la ventana

### Líneas 1-28

- `import ast` permite analizar expresiones matemáticas como si fueran árboles de sintaxis.
- `import json` sirve para guardar y leer archivos JSON.
- `import tkinter as tk` importa la librería gráfica.
- `from tkinter import ttk` trae los widgets modernos (pestañas, frames, etc.).
- `from tkinter import messagebox, filedialog` usa mensajes emergentes y ventanas de archivo.
- `import re` permite trabajar con expresiones regulares para limpiar cadenas.
- `import math` y `from decimal import Decimal, InvalidOperation` y `from math import gcd` apoyan cálculos exactos y conversiones.
- `from pathlib import Path` permite manejar rutas del sistema.

Además se importa desde `updater.py`:

- `APP_VERSION`
- `check_for_updates`
- `download_and_apply_update`

Esto quiere decir que la app puede comprobar si hay una nueva versión disponible.

### Líneas 30-52

Aquí se crea la ventana principal:

- `root = tk.Tk()` crea la ventana base.
- `notebook = ttk.Notebook(root)` crea una pestaña para organizar contenido.
- `matematica_tab`, `quimica_tab`, `realinfo_tab`, `tab4` son las cuatro pestañas principales.
- Después se crean subpestañas dentro de la parte matemática:
  - `Calculator`
  - `Notas`

Esto convierte la app en un programa con varias secciones, no solo una calculadora.

---

## 2) Pestaña de Notas

### Líneas 53-110

Aquí se construye el cuaderno digital.

- `notes_container` es el contenedor visual.
- `notes_canvas` dibuja el fondo del cuaderno con líneas.
- `notes_left_margin`, `notes_top_margin`, `notes_line_gap`, `notes_line_count` son valores para crear el estilo de hoja de cuaderno.
- `notes_canvas.create_line(...)` dibuja las líneas horizontales.
- `notes_box = tk.Text(...)` crea el área donde el usuario escribe.
- `notes_save_btn`, `notes_load_btn`, `notes_clear_btn` crean los botones de guardar, cargar y limpiar.

### Qué hace esta parte

Es una zona de apuntes, una especie de bloc de notas dentro del mismo programa. No se usa para cálculos, solo para tomar notas rápidas.

---

## 3) Créditos

### Líneas 111-159

Se crea la pestaña de “Créditos”:

- `credits_frame` pinta un fondo oscuro.
- `credits_title` pone el título.
- `credits_card` crea una tarjeta estilizada.
- `credits_text` contiene texto fijo con información del creador y el desarrollo.

Esto es más de presentación y branding del proyecto para una exposición o demo.

---

## 4) Tabla periódica y datos químicos

### Líneas 160-206

Se define la base de datos química principal:

- `PERIODIC_TABLE` guarda cada elemento con: nombre, número atómico y masa atómica.
- `PERIODIC_TABLE_ORDER` ordena los elementos para recorrerlos.
- `PERIODIC_TABLE_LAYOUT` define la posición visual en la tabla periódica.
- `ELEMENT_GROUPS` clasifica cada elemento (metales, no metales, halógenos, gases nobles, etc.).
- `ELEMENT_GROUP_COLORS` define colores para cada categoría.

### Función importante: `get_element_group_color(symbol: str)`

- Devuelve el color según la categoría del elemento.
- Se usa para pintar cada caja de la tabla periódica.

---

## 5) Archivos JSON de almacenamiento

### Líneas 207-311

Aquí empiezan las funciones que leen y escriben archivos JSON:

- `ELEMENT_INFO_FILE = Path(__file__).resolve().with_name("element_info.json")`
- `GENERAL_INFO_FILE = Path(__file__).resolve().with_name("general_info.json")`

Estas rutas apuntan a archivos del mismo directorio. Las funciones:

- `load_element_info_store()`
- `save_element_info_store()`
- `load_general_info_store()`
- `save_general_info_store()`

permiten guardar información sobre elementos y estado general de la interfaz.

Luego están:

- `remember_ui_history(...)`
- `restore_ui_history(...)`
- `ensure_element_info(...)`

Estas funciones guardan el historial visual de la app y aseguran que cada elemento tenga un registro base.

---

## 6) Búsqueda y selección de elementos

### Líneas 316-359

- `search_element_database(query)` busca elementos por símbolo o nombre.
- `refresh_element_browser(query="")` actualiza la lista del navegador.

Esto hace que el usuario pueda buscar químicamente sin mirar toda la tabla.

---

## 7) Cálculo de masa molar y fórmulas químicas

### Líneas 372-775

Aquí hay funciones clave:

- `parse_formula_to_counts(formula: str)`
- `compute_molar_mass(formula: str)`
- `on_calculate_molar()`
- `add_element_to_formula(symbol: str)`
- `build_molecule_formula(elements)`
- `load_saved_molecule_history()`
- `save_molecule_history_to_disk()`
- `add_molecule_to_history(formula: str)`
- `refresh_molecule_history_list()`
- `search_molecule_database(query: str)`
- `refresh_molecule_browser(query: str = "")`
- `load_selected_molecule_from_browser(event=None)`
- `get_molecule_record(formula: str)`
- `refresh_molecule_display()`
- `add_to_molecule(symbol: str)`
- `remove_last_element()`
- `formulate_molecule()`
- `clear_molecule()`
- `show_element_details(symbol: str)`

### Qué hacen estas funciones

Permiten:

- introducir una fórmula química,
- contar átomos por elemento,
- calcular masa molar,
- guardar el historial,
- navegar por la tabla periódica y mostrar información detallada del elemento.

Es la parte química de la aplicación: no solo resuelve cálculos aritméticos, sino datos y ecuaciones de química.

---

## 8) Sistema de información real / “RealInformacion”

### Líneas 891-1844

Aquí se construye la parte más avanzada de la app para “información real” de elementos.

Se manejan funciones como:

- `open_edit_element_dialog()`
- `refresh_element_reference_selector()`
- `apply_reference_from_selector_to_element()`
- `persist_bulk_delimiter()`
- `apply_bulk_mapping()`
- `switch_realinfo_mode()`
- `create_citation_from_form()`
- `save_element_reference()`
- `refresh_reference_list()`
- `apply_selected_reference_to_definition()`
- `delete_selected_reference()`
- `delete_current_definition()`
- `add_link_to_element()`
- `refresh_link_list()`
- `open_selected_link()`
- `delete_selected_link()`
- `adjust_window_to_active_tab()`
- `save_all_state_on_close()`
- `toggle_fullscreen()`

### Qué hace esta parte

Permite editar definiciones de elementos, añadir referencias, guardar enlaces, crear citaciones y dar un formato más profesional a la información química.

---

## 9) Historias y archivos de cálculo

### Líneas 1886-2109

Estas funciones sirven para guardar lo que el usuario escribe y calcula:

- `load_saved_history()`
- `save_history_to_disk()`
- `save_notes_to_disk()`
- `load_notes_from_disk()`
- `extract_history_expression(entry: str)`
- `load_history_entry(event=None)`

Esto ayuda a que la app recuerde operaciones anteriores y conserve notas.

---

## 10) Matemáticas y resolución de ecuaciones

### Líneas 2127-3236

Es el corazón matemático del proyecto. Aquí se encuentra la resolución de ecuaciones y sistemas.

Funciones principales:

- `select_method(name: str)`
- `perform_igualacion(parts: list)`
- `perform_reduccion(parts: list)`
- `perform_determinante(parts: list)`
- `perform_substitution(parts: list)`
- `normalize_expression(expr: str)`
- `eval_math_expression(expr: str)`
- `parse_linear(expr: str)`
- `parse_system_linear(expr: str)`
- `normalize_system_equation(eq: str)`
- `split_system_equations(display: str)`
- `solve_system(equations)`
- `build_linear_steps(left: str, right: str)`
- `solve_linear_equation(left: str, right: str)`

### Qué hace esta zona

- limpia expresiones,
- convierte variables X/Y y símbolos Unicode,
- interpreta ecuaciones lineales,
- resuelve sistemas con varios métodos,
- genera pasos explicativos para el usuario.

Es el bloque más importante de la lógica matemática.

---

## 11) Conversión fracción <-> decimal

### Líneas 3168-3250

Aquí están:

- `normalize_decimal_text(value)`
- `decimal_to_fraction_text(value: str)`
- `convert_fraction_decimal()`

Estas funciones convierten entre decimal y fracción para que el usuario pueda mezclar ambos formatos.

---

## 12) Lógica del botón de la calculadora

### Líneas 3252-3525

La función más importante del archivo es:

- `button_clicked(value)`

Esta función decide qué ocurre al pulsar cualquier botón. Se encarga de:

- números,
- operadores +, -, ×, ÷, √, ^,
- borrar,
- porcentaje,
- cambiar de signo,
- interpretar ecuaciones,
- resolver sistemas,
- ejecutar cálculos completos.

Es la pieza central que hace que la app “se comporte” como una calculadora.

---

## 13) Cierre de la ventana y actualización automática

### Líneas 3526-3579

- `on_close()` guarda el historial antes de cerrar.
- `root.protocol("WM_DELETE_WINDOW", on_close)` liga el cierre de la ventana a esta función.
- `root.geometry(...)` centra la ventana en pantalla.
- `check_update_on_start()` comprueba si hay una nueva versión.
- `root.after(1000, check_update_on_start)` programa la comprobación.
- `root.mainloop()` mantiene la interfaz abierta.

Esto hace que la app se ejecute continuamente mientras el usuario la usa.

---

## Resumen rápido

Si quieres resumirlo en una frase:

> `projecto_expo.py` es un programa con interfaz gráfica, calculadora, cuaderno, historial, tabla periódica, resolución de ecuaciones y gestión de información química.

La parte difícil del código no está en la UI, sino en la lógica de interpretación matemática y en la manipulación de expresiones complejas.

---

## Ejemplos reales sacados del código

### 1) Creación de la ventana y pestañas

```python
root = tk.Tk()
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

matematica_tab = ttk.Frame(notebook)
quimica_tab = ttk.Frame(notebook)
realinfo_tab = ttk.Frame(notebook)
tab4 = ttk.Frame(notebook)

notebook.add(matematica_tab, text="Matematica")
notebook.add(quimica_tab, text="Quimica")
notebook.add(realinfo_tab, text="RealInformacion")
notebook.add(tab4, text="Creditos")
```

Este bloque crea la ventana principal y las pestañas principales. Si quieres añadir otra sección, solo tendrías que crear un nuevo `ttk.Frame` y hacer `notebook.add(...)`.

### 2) Cuaderno con líneas tipo papel

```python
notes_canvas = tk.Canvas(notes_container, width=760, height=420, bg="#f8f8f8", highlightthickness=0)
notes_canvas.pack(fill="both", expand=True)

for i in range(notes_line_count + 1):
    y = notes_top_margin + i * notes_line_gap
    notes_canvas.create_line(18, y, notes_width - 18, y, fill="#d1d1d1", width=1)
```

Esto dibuja las líneas horizontales del cuaderno. Si quieres cambiar el aspecto, puedes ajustar:

- `notes_line_gap`
- `notes_line_count`
- `notes_width`
- `notes_height`

### 3) Tabla periódica y clasificación por tipo

```python
PERIODIC_TABLE = {
    'H': ("Hydrogen", 1, 1.008), 'He': ("Helium", 2, 4.0026),
    'Li': ("Lithium", 3, 6.94), 'Be': ("Beryllium", 4, 9.0122),
}

ELEMENT_GROUPS = {
    'H': 'nonmetal', 'He': 'noble-gas',
    'Li': 'alkali-metal', 'Be': 'alkaline-earth',
}
```

Este ejemplo muestra la estructura base de cada elemento. Si quieres añadir un elemento nuevo o cambiar un nombre, aquí es donde lo haces.

### 4) Resolver una ecuación lineal

```python
def build_linear_steps(left: str, right: str):
    left = normalize_expression(left)
    right = normalize_expression(right)

    left_coeff, left_const = parse_linear(left)
    right_coeff, right_const = parse_linear(right)

    coef_diff = left_coeff - right_coeff
    const_diff = right_const - left_const
    x_value = const_diff / coef_diff
```

Esto es un ejemplo típico de la lógica que resuelve una ecuación como:

- `3x + 4 = 10`

La app normaliza la expresión, separa coeficientes y constantes, y luego calcula el valor de `x`.

### 5) Resolver un sistema de ecuaciones

```python
def solve_system(equations):
    eqs = []
    for equation in equations:
        clean = normalize_system_equation(equation)
        if not clean or "=" not in clean:
            raise ValueError(f"Each equation must contain '=': {equation!r}")
        left, right = clean.split("=", 1)
        left_a, left_b, left_c = parse_system_linear(left)
        right_a, right_b, right_c = parse_system_linear(right)
        a = left_a - right_a
        b = left_b - right_b
        c = right_c - left_c
        eqs.append((a, b, c))
```

Ejemplo real de entrada:

```python
['3x-2y=7', 'x+3y=17']
```

El programa convierte cada ecuación en coeficientes `a`, `b` y `c`, y luego usa determinantes para resolver.

### 6) Lógica central del botón de la calculadora

```python
def button_clicked(value):
    global right_symbols, top_symbols, label, A, B, operator

    if value in right_symbols:
        if value == "=":
            display = label["text"].strip()
            if "=" in display:
                left, right = display.split("=", 1)
                steps = build_linear_steps(left, right)
```

Esto te da la idea de cómo se maneja cada tecla. Si quieres modificar un botón o crear uno nuevo, normalmente tendrás que cambiar aquí la lógica de `button_clicked`.

### Cómo editar sin miedo

Cuando quieras cambiar algo, busca primero estas tres cosas:

1. la parte visual (`tk.Button`, `tk.Label`, `ttk.Frame`),
2. la lógica del evento (`button_clicked`),
3. la función matemática que resuelve la expresión (`solve_system`, `parse_linear`, `eval_math_expression`).

Si entiendes estas tres zonas, puedes modificar y expandir la app sin tener que revisar todo de golpe.
