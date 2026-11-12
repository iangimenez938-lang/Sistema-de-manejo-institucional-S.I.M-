# 03. `general_info_app.py`

## Qué hace este archivo

Este módulo crea la pantalla general de la aplicación: la primera pestaña que se ve al abrir la app y la "puerta de entrada" al resto del proyecto.

Aunque parece una vista simple, tiene una función crítica: centralizar el acceso a la información general de la aplicación.

Su objetivo es:

- mostrar un resumen visual del proyecto,
- ofrecer acceso rápido a Matemática, Química, RealInformación y Créditos,
- mantener almacenamiento persistente para la UI,
- e integrar los módulos principales del programa.

---

## 1. Persistencia de datos y almacenamiento JSON

El archivo define varias rutas:

- `PROJECT_ROOT`
- `OTHER_DIR`
- `GENERAL_INFO_FILE`
- `LEGACY_GENERAL_INFO_FILE`

y funciones de carga/guardado como:

```python
load_general_info_store()
save_general_info_store(store)
remember_ui_history(store, history_key, value, limit)
restore_ui_history(store, history_key, default, limit)
```

### ¿Qué hace esto?

Hace que la aplicación recuerde cosas como:

- historial de interacciones,
- valores o textos introducidos recientemente,
- y otros datos que el usuario ha usado en la UI.

También incluye soporte para archivos antiguos y nuevos, usando una lógica de migración simple:

```python
if primary.exists():
    return primary
if legacy.exists():
    return legacy
return primary
```

Esto evita romper la compatibilidad si hubo un cambio de ubicación de archivos de datos.

---

## 2. La función `build_general_info_ui`

Es la función central de este módulo. Construye la pantalla de bienvenida y contiene una lógica inteligente: crea un `ttk.Notebook` interno para organizar varias subpantallas.

Estas subpantallas son:

- Inicio
- Matemática
- Química
- RealInformacion
- Creditos

Esto permite que la pantalla principal funcione como un “dashboard” del proyecto, sin que cada sección tenga que ser totalmente independiente.

---

## 3. La cabecera del dashboard

La parte superior muestra:

- título: "Calculadora Expo"
- subtítulo: una descripción general del uso de la app

Esto crea la sensación de una aplicación más organizada y profesional, además de facilitar la navegación.

---

## 4. La sección de resumen

Aparece un texto largo que explica que la app reúne información general y da acceso a cada bloque.

Luego crea una serie de "cards" o paneles, cada uno con un nombre y una breve descripción:

- Matemática
- Química
- RealInformación
- Créditos

Estas tarjetas son visualmente útiles, pero también sirven como una forma de orientación al usuario y de presentación del programa.

---

## 5. Integración de otros módulos

La clave real del archivo está aquí:

```python
if target_module == "matematica":
    from matematica.matematica_app import build_matematica_ui
    build_matematica_ui(subframe, root)
```

Es decir, el módulo general no tiene que duplicar la lógica de cada sección. Simplemente llama a la función de cada módulo y la dibuja dentro de un subframe.

Esto es un patrón de composición muy limpio:

- cada módulo sabe cómo dibujar su propia parte,
- la pantalla general solo coordina la presentación.

---

## 6. Cómo ayuda a la arquitectura del proyecto

Este archivo es una pieza muy importante porque da a la app una organización de capas:

- capa de arranque: `projecto_expo.py`
- capa de navegación: `general_info_app.py`
- capa funcional: `matematica_app.py` y `quimica_app.py`
- capa de información: `real_informacion_app.py`
- capa de acreditación: `creditos_app.py`

Sin esta capa global, todo lo demás quedaría muy mezclado y sería mucho más difícil de mantener.

---

## 7. Ventaja de este diseño

La ventaja es que puedes añadir nuevas pantallas o nuevos subsistemas sin tocar la lógica principal del programa.

Solo tendrías que:

1. crear un módulo nuevo,
2. definir una función `build_x_ui`,
3. llamarla desde esta pantalla general,
4. y listo.

Eso es una buena base para construir una app escalable.

---

## 8. Resumen corto

Este archivo no hace cálculos ni resuelve problemas. Su valor está en organizar la aplicación, dar una primera impresión del proyecto y conectar el resto de módulos de forma clara y reutilizable.
