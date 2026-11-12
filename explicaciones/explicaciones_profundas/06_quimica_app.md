# 06. `quimica/quimica_app.py`

## Qué hace este archivo

Este módulo es el cerebro químico de la aplicación. Su propósito es combinar dos cosas:

- un conjunto de datos sobre elementos y sus propiedades,
- y una interfaz visual para trabajar con ellos.

Su funcionalidad principal es ofrecer una herramienta para:

- calcular masa molar de fórmulas químicas,
- mostrar la tabla periódica,
- buscar y guardar información de elementos,
- y gestionar información de moléculas.

---

## 1. La base de datos periódica

En la parte superior del archivo se define `PERIODIC_TABLE`, que es un diccionario con elementos como:

```python
'H': ("Hydrogen", 1, 1.008)
'He': ("Helium", 2, 4.0026)
...
```

Cada entrada contiene:

- nombre,
- número atómico,
- masa atómica.

También hay más listas y diccionarios como:

- `PERIODIC_TABLE_ORDER`
- `PERIODIC_TABLE_LAYOUT`
- `ELEMENT_GROUPS`
- `ELEMENT_GROUP_COLORS`

Esto hace que la app pueda dibujar la tabla periódica con una lógica organizada por grupos y ubicaciones.

---

## 2. Funciones de persistencia

Esta parte del archivo guarda la información química en JSON, siguiendo el patrón de otros módulos del proyecto.

Las funciones importantes son:

- `load_element_info_store()`
- `save_element_info_store()`
- `load_general_info_store()`
- `save_general_info_store()`
- `load_saved_molecule_history()`
- `save_molecule_history()`

Estas funciones permiten conservar:

- información ampliada de elementos,
- historial de moléculas,
- y metadatos del usuario.

La lógica de `legacy` sirve para migrar archivos antiguos que estaban en ubicaciones viejas del proyecto.

---

## 3. Estructura de un elemento químico

La función `ensure_element_info(symbol, element_info)` crea un bloque inicial para cada elemento si aún no existe.

Ese bloque incluye datos como:

- nombre común,
- nombre científico,
- clasificación,
- masa atómica,
- estado estándar,
- configuración electrónica,
- estados de oxidación,
- electronegatividad,
- radio atómico,
- energía de ionización,
- afinidad electrónica,
- densidad,
- año de descubrimiento,
- referencias y notas.

Esto convierte a la app en algo mucho más rico que una simple tabla periódica visual.

---

## 4. Cálculo de masa molar

La parte que más se usa probablemente es la fórmula química:

```python
compute_molar_mass(formula)
```

La lógica se apoya en `parse_formula_to_counts()`, que transforma una fórmula como `H2O` o `Ca(OH)2` en un diccionario con conteos por elemento.

Ejemplo conceptual:

- `H2O` -> `{H: 2, O: 1}`
- `Ca(OH)2` -> `{Ca: 1, O: 2, H: 2}`

Luego `compute_molar_mass` multiplica cada masa atómica por el número de átomos y suma todo.

Esto es la base de la calculadora química del proyecto.

---

## 5. Pestaña de fórmula

La parte de UI para fórmulas crea un cuadro donde el usuario escribe una fórmula química, por ejemplo:

- `H2O`
- `CO2`
- `NaCl`
- `Ca(OH)2`

Al presionar el botón, se ejecuta `on_calculate_molar()`:

1. toma la fórmula,
2. la valida,
3. llama a `compute_molar_mass`,
4. muestra la masa molar total,
5. y renderiza un desglose elemento a elemento.

Es muy útil para aprender química porque muestra no solo el resultado final, sino también cómo se llega a él.

---

## 6. La tabla periódica visual

La pestaña de "Tabla Periódica" genera una cuadrícula donde cada elemento aparece como un botón o bloque con color según su grupo.

Esto se hace usando:

- `PERIODIC_TABLE_LAYOUT` para posición,
- `get_element_group_color(symbol)` para el color,
- y un `Canvas` con scroll para manejar muchos elementos.

La idea es que el usuario pueda pulsar cada elemento y abrir una ficha más detallada con su información.

---

## 7. Gestión de moléculas y búsqueda

La parte de moléculas probablemente usa una base de datos de compuestos y permite buscar fórmulas o nombres comunes.

Las funciones importantes son:

- `build_molecule_formula(elements)`
- `search_molecule_database(query, molecule_database)`
- `load_saved_molecule_history()`
- `save_molecule_history()`

Esto permite:

- reconstruir una fórmula a partir de una lista de elementos,
- buscar moléculas según texto,
- guardar historial de búsquedas o compuestos usados.

---

## 8. Cómo se relaciona con el resto de la app

Esta parte no vive aislada. De hecho, la reutiliza mucho información del proyecto:

- `general_info_app.py` guarda datos generales,
- `real_informacion_app.py` usa la tabla periódica y la información mejorada de elementos,
- y la sección general de la app llama a `build_quimica_ui` desde la navegación principal.

Esto convierte al módulo de química en una pieza central del proyecto, no solo un complemento.

---

## 9. Resumen corto

`quimica_app.py` es un módulo de datos + interfaz + cálculo. Es una de las partes más ricas del sistema porque combina:

- información técnica,
- jerarquía visual,
- almacenamiento persistente,
- y lógica aplicada a fórmulas químicas.

Es un ejemplo muy claro de cómo la app mezcla ciencia, UX y programación funcional.
