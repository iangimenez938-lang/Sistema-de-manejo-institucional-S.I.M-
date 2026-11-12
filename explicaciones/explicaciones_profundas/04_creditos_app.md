# 04. `creditos_app.py`

## Qué hace este archivo

Este módulo crea la pestaña de créditos y reconocimiento del proyecto.

Es una de las partes más simples del programa, pero también una de las más importantes desde el punto de vista de identidad y presentación. Sirve para dejar constancia de:

- quién creó la app,
- para qué fue pensada,
- y que se usó ayuda de herramientas como GitHub Copilot en su desarrollo.

---

## 1. Estructura visual

La función `build_creditos_ui(creditos_tab, root=None)` crea una `Frame` con fondo oscuro:

```python
credits_frame = tk.Frame(creditos_tab, bg="#1a1028")
```

Eso da una apariencia más elegante, casi como una tarjeta de presentación o una sección de "acerca de".

Luego añade:

- un título grande: "Créditos",
- una tarjeta central con fondo más claro,
- y un texto explicativo dentro de esa tarjeta.

---

## 2. El texto principal

La variable `credits_text` contiene el contenido del mensaje:

```python
credits_text = (
    "Creador: Samuel I. G.\n\n"
    "Este programa fue creado por Samuel I. G. como proyecto para la expo técnica de 2026, con ayuda clave de GitHub Copilot para crear, corregir, revisar y testear el código.\n\n"
    "Tiempo estimado de desarrollo: aproximadamente 30 horas de trabajo en total."
)
```

Aquí el proyecto comunica dos cosas importantes:

1. la autoría del trabajo,
2. la colaboración con herramientas de inteligencia artificial para apoyar la creación y revisión del código.

Eso hace que la sección no sea solo estética, sino también contextual.

---

## 3. Cómo se dibuja la interfaz

Se usa `tk.Label` con:

- `justify="center"`
- `font=("Arial", 16)`
- `wraplength=700`
- `bg="#2b173d"`
- `fg="#f7f0ff"`

Esto hace que el texto se vea bien centrado y readable, sin que se desborde de la ventana.

La tarjeta se empaca con `pack(fill="both", expand=True, ...)`, así que se adapta al tamaño del contenido y al ancho de la pestaña.

---

## 4. Qué aporta este archivo a la app

Aunque no tiene cálculo ni lógica compleja, este módulo cumple un papel importante:

- da identidad al proyecto,
- reconoce a los autores,
- contextualiza la creación del software,
- y da una sensación de cierre profesional al recorrido de la app.

Es el tipo de sección que a menudo se omite en proyectos técnicos, pero que ayuda mucho a que la aplicación parezca terminada.

---

## 5. Por qué es importante aunque sea simple

A veces se piensa que las pantallas de créditos "no importan". Pero en proyectos educativos y de expo, sí importan porque permiten explicar:

- qué se hizo,
- quién lo hizo,
- con qué ayuda,
- y en qué contexto se creó.

Esto también facilita la defensa del proyecto ante evaluadores o docentes.

---

## 6. Resumen corto

Este archivo es visual y comunicativo. No resuelve problemas ni manipula datos, pero da a la aplicación un tono más serio, profesional y humano.
