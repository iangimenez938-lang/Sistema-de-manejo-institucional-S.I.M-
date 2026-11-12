# 08. `app-content/projecto_expo.py` (wrapper de lanzado)

## Qué hace este archivo

Este archivo es una versión del lanzador principal que está pensada para el contexto del paquete `app-content`.

Su función es muy similar a la principal, pero está adaptada para ejecutarse dentro de una estructura modular donde las pantallas se importan desde la carpeta `app-content`.

Es decir, es un "wrapper" que monta la aplicación usando módulos desarrollados específicamente para esa estructura.

---

## 1. Preparación de rutas

El flujo inicial es prácticamente igual al del lanzador principal:

- detecta si la app se ejecuta desde un entorno congelado,
- calcula la ruta base con `Path(__file__).resolve().parent.parent`,
- y agrega la carpeta base y la carpeta `app-content` a `sys.path`.

Esto permite que los imports funcionen sin depender de la ubicación exacta del archivo.

---

## 2. Importación de módulos

Se importan funciones como:

- `build_general_info_ui`
- `build_real_informacion_ui`
- `build_creditos_ui`
- `build_matematica_ui`
- `build_quimica_ui`

y también se importan funciones del sistema de actualización:

- `APP_VERSION`
- `check_for_updates`
- `download_and_apply_update`

Esto confirma que el proyecto separa muy claramente entre:

- la UI de cada módulo,
- y la lógica global del app.

---

## 3. Construcción del layout principal

Se crea la ventana raíz y un `Notebook` con pestañas. A diferencia de un enfoque totalmente estático, cada sección se monta mediante su builder, lo que deja el diseño muy ordenado.

Las pestañas son:

- General
- RealInformacion
- Matematica
- Quimica
- Creditos

Todo esto se hace al inicio, de forma que la app está lista apenas se carga.

---

## 4. Centrado y comportamiento final

A la hora de terminar la Montaje, el archivo centra la ventana en la pantalla de forma dinámica:

```python
root.update()
window_width = root.winfo_width()
window_height = root.winfo_height()
```

Esto ayuda a que la app se vea bien en distintos monitores o resoluciones.

---

## 5. Actualización automática al iniciar

La última parte llama a `check_update_on_start()`, que revierte a la lógica del updater. Si hay una versión nueva, pregunta al usuario si desea instalarla.

Esto hace que la experiencia se sienta más completa y más preparada para distribución real.

---

## 6. ¿Qué diferencia tiene respecto al lanzador raíz?

La diferencia principal no es conceptual, sino de contexto físico del proyecto:

- un archivo está pensado para ejecutarse desde la raíz del proyecto,
- el otro está pensado para ejecutarse desde dentro de la estructura `app-content`.

Ambos tienen la misma idea: "montar la app y conectar sus módulos".

---

## 7. Resumen

Este archivo sirve como el nodo de coordinación del paquete `app-content`. Es el punto donde se ensamblan todas las secciones visuales y donde se conecta con la lógica de actualización.

Si comprendes este archivo, entiendes muy bien la arquitectura general de la aplicación.
