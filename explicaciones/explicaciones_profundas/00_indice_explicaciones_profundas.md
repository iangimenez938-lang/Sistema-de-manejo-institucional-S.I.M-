# Índice de explicaciones profundas

Este directorio está pensado para ir un paso más allá que los documentos básicos de la carpeta `explicaciones/` y explicar la lógica real de cada archivo del proyecto.

La idea es que no solo veas "qué hace la pantalla", sino también:

- qué datos carga,
- dónde los guarda,
- qué funciones son las importantes,
- cómo fluye la información entre pantallas y archivos,
- y cómo puedes ampliar la aplicación sin romper el conjunto.

## Archivos documentados

1. [01_launcher_projecto_expo.md](01_launcher_projecto_expo.md)  
   Explica el archivo principal que lanza la aplicación y monta las pestañas.

2. [02_real_informacion_app.md](02_real_informacion_app.md)  
   Explica la sección de referencias, enlaces y elementos químicos estructurados.

3. [03_general_info_app.md](03_general_info_app.md)  
   Explica la pantalla general de resumen y cómo integra el resto de módulos.

4. [04_creditos_app.md](04_creditos_app.md)  
   Explica la vista de autor y créditos del proyecto.

5. [05_matematica_app.md](05_matematica_app.md)  
   Explica la calculadora, la historia, las notas y los procesos internos del módulo matemático.

6. [06_quimica_app.md](06_quimica_app.md)  
   Explica la tabla periódica, el cálculo de masa molar, la gestión de moléculas y el almacenamiento de datos.

7. [07_updater.md](07_updater.md)  
   Explica el sistema de actualización automática y cómo comprueba si hay una nueva versión.

8. [08_wrapper_app_content_projecto_expo.md](08_wrapper_app_content_projecto_expo.md)  
   Explica el archivo de lanzamiento dentro de la estructura `app-content` y su función de montaje.

9. [09_arquitectura_y_extension.md](09_arquitectura_y_extension.md)  
   Explica cómo pensar la app como sistema modular, cómo crear nuevas materias, cómo conectar UIs y cómo manejar historiales y persistencia.

10. [10_guia_anadir_nueva_materia.md](10_guia_anadir_nueva_materia.md)  
   Guía práctica paso a paso para añadir una nueva materia como ejemplo con Física, incluyendo UI, historial y conexión con el índice.

11. [11_plantilla_modulo_nueva_materia.md](11_plantilla_modulo_nueva_materia.md)  
   Plantilla reutilizable para crear cualquier nueva materia sin partir desde cero.

## Cómo leer estas explicaciones

Lo ideal es seguir este orden:

1. empezar por el lanzador principal,
2. luego por los módulos de interfaz,
3. después por el módulo matemático,
4. luego por el químico,
5. y finalmente por `updater.py`.

Esto te permite entender la app en capas:

- capa de arranque,
- capa de UI,
- capa funcional,
- capa de persistencia,
- capa de actualización.

## Nota importante sobre los archivos vacíos

Los archivos `__init__.py` dentro de `app-content/matematica` y `app-content/quimica` no tienen lógica funcional importante. Su función es marcar esos directorios como paquetes Python para que puedan importarse correctamente.

En otras palabras, no son "módulos con comportamiento", sino "contenedores de importación".

---

Si quieres, el siguiente paso natural es usar estas guías para ampliar una funcionalidad concreta: por ejemplo, añadir una nueva pestaña, crear un nuevo cálculo matemático o incorporar un nuevo dato químico.
