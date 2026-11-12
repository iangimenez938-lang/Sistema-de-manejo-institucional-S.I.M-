# 02. `real_informacion_app.py`

## Qué hace este archivo

Este archivo es la sección de "RealInformación" de la app. Su objetivo es reunir tres ideas muy relacionadas:

- guardar referencias bibliográficas,
- guardar enlaces útiles,
- y mostrar información estructurada de elementos químicos.

Es una mezcla de panel de notas, gestor de enlaces y buscador de elementos científicos.

---

## 1. Importaciones clave

El módulo importa:

- `tkinter` para crear la interfaz,
- `ttk` para widgets más modernos,
- `messagebox` para mensajes emergentes,
- `webbrowser` para abrir enlaces,
- y varios módulos de química para obtener datos del sistema periódico.

Esto demuestra que la sección no es aislada: reutiliza información que ya existe en otros archivos, especialmente en `quimica/quimica_app.py`.

---

## 2. La función principal: `build_real_informacion_ui`

La pieza central es esta función. Cuando la app crea una pestaña de RealInformación, llama a esta función y ella construye todo el contenido visual.

Su flujo es:

1. cargar la base de datos de información general,
2. cargar la base de datos de elementos químicos,
3. crear la parte superior con selector de categoría y modo,
4. preparar un panel scrollable para contenido largo,
5. construir dos bloques principales:
   - referencias bibliográficas,
   - enlaces externos,
   - y la vista estructurada del elemento.

---

## 3. Gestión de referencias

La primera parte permite al usuario rellenar campos como:

- título,
- autores,
- revista,
- año,
- DOI,
- resumen.

Cuando pulsa "Guardar referencia", se construye un texto de cita y se guarda en un diccionario dentro de `store`:

```python
store.setdefault(category, {"references": [], "links": []})
store[category]["references"].append({ ... })
```

Eso significa que cada categoría tiene su propia lista: General, Química, Matemática, Otro.

### ¿Qué hace `save_general_info_store`?

Guarda toda esta estructura en un archivo JSON para que no se borre al cerrar la app.

### ¿Qué hace `refresh_reference_list`?

Actualiza la `Listbox` lateral para mostrar las referencias guardadas, con un título resumido.

### ¿Qué hace `delete_reference_entry`?

Elimina la referencia seleccionada en la lista y vuelve a guardar el estado.

---

## 4. Gestión de enlaces

La sección también permite introducir una URL y guardarla en la misma estructura de datos.

Flujo:

1. el usuario escribe un enlace,
2. se valida que no esté vacío,
3. se guarda en la categoría seleccionada,
4. se actualiza la lista,
5. el usuario puede abrir el enlace seleccionado con `webbrowser.open(...)`.

Esto convierte la app en un auténtico gestor simple de recursos externos para la investigación.

---

## 5. La parte estructurada de elemento químico

La parte más técnica del módulo es la que muestra datos de un elemento concreto.

Se crean varias variables tipo `StringVar` para cada dato:

- nombre
- símbolo
- número atómico
- protones
- neutrones
- electrones
- masa atómica
- estado
- nombre común
- nombre científico
- clasificación
- electronegatividad
- configuración electrónica
- estados de oxidación
- densidad
- año descubierto
- referencia

Esto convierte la UI en una especie de ficha de elemento.

### `show_element_details(symbol)`

Es la función que recibe un símbolo como `H`, `O`, `Na`, etc., y actualiza todos esos textos.

El flujo es:

1. comprobar que el símbolo existe en `PERIODIC_TABLE`,
2. obtener su nombre y masa,
3. llamar a `ensure_element_info(symbol, element_info)`,
4. mezclar datos base con datos extendidos,
5. rellenar la pantalla con cada valor.

Esto es importante porque el archivo no solo reutiliza la tabla periódica, sino que también complementa sus datos con información extra guardada por el usuario.

---

## 6. Relación con la química

La sección usa varios importados desde `quimica.quimica_app`:

- `PERIODIC_TABLE`
- `PERIODIC_TABLE_ORDER`
- `ELEMENT_GROUPS`
- `get_element_group_color`
- `load_element_info_store`
- `save_element_info_store`
- `ensure_element_info`

Eso quiere decir que la parte de RealInformación depende directamente de la parte química. Es una excelente prueba de que la app está construida por módulos que se integran entre sí.

---

## 7. Qué patrón de diseño sigue

Este módulo usa una estructura muy típica de Tkinter:

- crear frames,
- crear widgets dentro de ellos,
- guardar estado en variables de control,
- actualizar listas cuando cambia la información,
- persistir en JSON cuando el usuario hace una acción.

Es un buen ejemplo de una interfaz donde el estado visual está ligado a datos guardados en memoria y en disco.

---

## 8. Si quieres ampliarlo

Puedes añadir por ejemplo:

- una búsqueda por nombre del elemento,
- un filtro por grupo o periodos,
- una lista de referencia por elemento,
- exportación a PDF o texto,
- o un sistema de etiquetas y categorías para cada referencia.

La lógica ya está preparada para hacerlo con bastante claridad, porque las funciones están separadas por responsabilidad.
