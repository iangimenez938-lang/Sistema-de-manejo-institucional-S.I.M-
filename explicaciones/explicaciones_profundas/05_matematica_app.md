# 05. `matematica/matematica_app.py`

## Qué hace este archivo

Este módulo es el corazón funcional de la parte matemática de la aplicación.

Encapsula varias cosas a la vez:

- una calculadora visual con botones,
- historial de operaciones,
- almacenamiento de notas,
- un sistema de "procesos" o explicación del cálculo,
- y una interfaz que permite cargar datos y seguir el flujo de una operación.

En otras palabras, no es solo una calculadora: es una pequeña estación de trabajo matemática dentro de la app.

---

## 1. Estructura general de la UI

La función principal es `build_matematica_ui(matematica_tab, root)`.

Dentro de ella se crean dos pestañas internas:

- `Calculator`
- `Notas`

Esto divide la sección en dos tipos de utilidad:

- realizar cálculos,
- guardar y revisar apuntes matemáticos.

La interfaz del bloque de notas se dibuja en un `Canvas` con cuadrículas, una zona de texto y botones para guardar, cargar y limpiar.

---

## 2. La parte de notas

El archivo crea un área con un `tk.Text` para escribir apuntes. Tiene botones para:

- guardar en disco,
- cargar desde disco,
- limpiar contenido.

Esto es importante porque la sección matemática no está pensada solo para resolver fórmulas; también sirve como cuaderno personal.

La función `save_notes_to_disk(notes_widget)` usa `filedialog.asksaveasfilename` para permitir elegir donde guardar el archivo. Luego escribe el contenido del texto en el disco.

La función `load_notes_from_disk(notes_widget)` hace el proceso inverso: carga un archivo `.txt` y lo coloca dentro del widget.

---

## 3. La calculadora gráfica

La parte principal es una calculadora con `tk.Button` para los números y operadores. Los botones se generan a partir de una matriz llamada `button_values`:

```python
button_values = [
    ["X", "Y", "(", ")", "√"],
    ["AC", "DEL", "+/-", "%", "÷", "}"],
    ["7", "8", "9", "000", "×"],
    ["4", "5", "6", "00", "-"],
    ["1", "2", "3", "0", "+"],
    [".", ",", "(=)", "F↔D", "/"],
]
```

Esto permite crear una pantalla con apariencia de calculadora científica de estilo moderno.

La pantalla principal es un `tk.Label` grande donde se muestra la expresión o resultado actual.

---

## 4. ¿Cómo se interpreta la entrada?

La lógica de cálculo está muy ligada a la UI y a la acción del botón.

El archivo define varias variables globales para mantener el estado como:

- `A`
- `B`
- `operator`

Esto es un patrón clásico de calculadora: se guarda el primer valor, luego el operador, luego el segundo valor.

La función `load_from_entry` permite cargar una operación desde el campo de historial interno. La función `button_clicked(value)` es el punto central de comportamiento del botón; es la que decide si el usuario presionó un número, un operador, una función o el signo `=`.

---

## 5. El historial de cálculo

La calculadora guarda un historial en un archivo JSON:

```python
HISTORY_FILE = Path(... / "Other" / "calculator_history.json")
```

Las funciones `load_saved_history` y `save_history_to_disk` se encargan de:

- leer el historial anterior,
- cargarlo como lista,
- y volver a guardarlo cada vez que cambia.

La interfaz muestra el historial en un `Listbox` y permite cargar una operación previa al hacer click sobre ella.

Esto es muy útil porque convierte el cálculo en una experiencia más interactiva y repetible.

---

## 6. La pestaña de "Proceso"

La parte de cálculo no solo muestra el resultado; también presenta una vista de proceso y una explicación.

Se crean dos widgets:

- `process_text_main`
- `explanation_text`

Estos se actualizan según el flujo de la operación. La idea es que el usuario no solo vea el número final, sino también cómo se llegó a él.

Esto es muy útil para educación y para explicar matemáticas paso a paso.

---

## 7. La lógica de "métodos" y expresiones

La calculadora parece estar pensada para manejar diferentes tipos de operaciones, no solo aritmética simple.

El archivo usa `ast` y funciones de evaluación para manejar expresiones. Además, tiene helpers como:

- `extract_history_expression`
- `load_history_entry`
- `add_calc_history`
- `clear_history`
- `undo_history`

Eso indica que el proyecto quiere conservar la idea de un historial con contexto y explicación, no solo un proceso "pulsar y ver resultado".

---

## 8. Qué hace que este archivo sea importante

Este archivo integra varios paradigmas de programación en una misma pantalla:

- UI con Tkinter,
- persistencia en JSON,
- manipulación de cadenas,
- lógica de estado,
- gestión de historial,
- herramientas de explicación pedagógica.

Es probablemente el módulo más completo y más útil para entender cómo la app combina interfaz y lógica.

---

## 9. Si quieres ampliarlo

Aquí tienes puntos muy naturales para seguir ampliando:

- más funciones matemáticas (derivadas, trigonometría, logaritmos),
- mayor validación de expresiones,
- soporte para ecuaciones algebraicas,
- exportación del historial a archivo,
- o un sistema de problemas con solución paso a paso.

Este módulo ya está muy cerca de ser una mini herramienta matemática, y por eso es un buen sitio para crecer.
