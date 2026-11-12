# Flujo de ejecución de la app

Este archivo explica el recorrido normal que sigue la aplicación desde que se abre hasta que se cierra.

## 1) Inicio

Cuando ejecutas la app:

- Python carga `projecto_expo.py`.
- Se crean las ventanas y pestañas.
- Se inicializa la interfaz de la calculadora.
- Se crean los botones, cajas de texto y paneles.

## 2) Carga de datos

Durante la carga, la app intenta leer:

- `element_info.json`
- `general_info.json`
- `calculator_history.json`
- `molecule_history.json`

Esto permite:

- mostrar historial previo,
- restaurar estados,
- cargar definiciones de elementos,
- mantener información entre ejecuciones.

## 3) Interacción con el usuario

Cuando el usuario pulsa un botón, la lógica entra en `button_clicked(value)`.

Ejemplos:

- si pulsa `7`, escribe el número,
- si pulsa `+`, guarda el operador,
- si pulsa `=`, ejecuta la operación,
- si escribe una ecuación, la resuelve,
- si el usuario pone `{3x-2y=7, x+3y=17}`, resuelve el sistema.

## 4) Resolución matemática

La app usa varias funciones para convertir lo que escribe el usuario en una expresión válida:

- `normalize_expression()`
- `parse_linear()`
- `parse_system_linear()`
- `solve_linear_equation()`
- `solve_system()`

Los pasos se almacenan en `process_history` y luego se muestran en la pestaña de proceso.

## 5) Guardado de historial

Cada operación correcta se guarda con:

- `add_calc_history(...)`
- `save_history_to_disk()`

Esto hace que el historial de operaciones se conserve en JSON.

## 6) Cierre

Al cerrar la ventana:

- `on_close()` guarda los estados
- `root.destroy()` cierra la interfaz
- la app no se pierde la última información

## 7) Actualización

Antes de que la ventana abra por completo, se ejecuta:

- `check_update_on_start()`

Esto compara la versión con una remota y, si hay nueva versión, lanza un mensaje para descargarla.

---

## Resumen visual

La ejecución general es así:

1. abrir la app
2. cargar datos y UI
3. recibir input del usuario
4. analizar la expresión
5. resolverla
6. guardar resultado
7. mostrar historial y pasos
8. cerrar con guardado
9. comprobar si hay actualización

Esto hace que la app no sea solo una “calculadora”, sino un conjunto de herramientas interactivas con almacenamiento y lógica avanzada.

---

## Ejemplos reales sacados del código

### 1) Flujo de una suma básica

```python
if value in right_symbols:
    if value == "=":
        display = label["text"].strip()
        if A is not None and operator is not None:
            B = display
            numA = eval_math_expression(A)
            numB = eval_math_expression(B)
            result = numA + numB
            label["text"] = remove_decimal(result)
```

Ejemplo de entrada real:

```python
A = "8"
operator = "+"
B = "3"
```

Resultado:

```python
8 + 3 = 11
```

### 2) Flujo de una ecuación lineal

```python
if "(=)" in display or "=" in display:
    eq = display.replace("(=)", "=")
    left, right = eq.split("=", 1)
    steps = build_linear_steps(left, right)
    status, sol = solve_linear_equation(left, right)
```

Ejemplo de entrada:

```python
"3x+2=14"
```

La lógica hace esto:

- separa lado izquierdo y derecho,
- simplifica términos,
- mueve constantes,
- despeja `x`.

### 3) Flujo de un sistema de ecuaciones

```python
system_like = (
    ("{" in display or "}" in display or "," in display or "\n" in display)
    and "=" in display
)

if system_like:
    cleaned = display.strip().strip("{}")
    parts = split_system_equations(cleaned)
    result = solve_system(parts)
```

Ejemplo real de entrada:

```python
'{3x-2y=7, x+3y=17}'
```

La app identifica que hay dos ecuaciones, las separa, y luego resuelve el sistema completo.

### 4) Cierre de la app

```python
def on_close():
    save_history_to_disk()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)
```

Esto es importante porque antes de cerrar la ventana la app guarda el historial del usuario. Si lo quitas, se pueden perder entradas recientes.

### Regla útil para editar

Si quieres cambiar comportamiento, intenta seguir este orden:

1. identifica qué entrada recibe el usuario,
2. ve qué función la procesa,
3. comprueba qué función la resuelve,
4. mira cómo se guarda el resultado.

Eso te permite entender cualquier parte de la app sin leer todo de una vez.
