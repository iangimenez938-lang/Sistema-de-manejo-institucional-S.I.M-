# Índice del proyecto

Este directorio recoge una explicación paso a paso de la aplicación para que puedas entender cómo está montada.

## Archivos principales

- `projecto_expo.py` — archivo central. Aquí está la interfaz gráfica, la lógica de la calculadora, los métodos de resolución, la parte química y la parte de información real.
- `updater.py` — sistema de actualización automática de la app.
- `version.json` — versión actual de la aplicación y URL de actualización.
- `element_info.json` — datos guardados de elementos químicos.
- `general_info.json` — historial/persistencia general de la interfaz.
- `calculator_history.json` — historial de cálculos.
- `molecule_history.json` — historial de fórmulas químicas.

## Archivos de pruebas y validación

- `debug_system_check.py` — prueba que carga la app y comprueba sistemas de ecuaciones.
- `process_logging_test.py` — comprueba que se registran pasos del proceso de cálculo.
- `solver_check.py` — ejecuta soluciones de ecuaciones y sistemas.
- `verify_system_fix.py` — verifica que los arreglos del sistema resuelven ejemplos reales.

## Scripts de lanzamiento

- `run_projecto_expo.bat` — abre la app en Windows.
- `run_projecto_expo.ps1` — versión PowerShell para lanzar la aplicación.
- `release_app.ps1` — genera la versión lista para distribución.

## Qué leer primero

1. `01_proyecto_expo_linea_a_linea.md`
2. `02_updater_linea_a_linea.md`
3. `03_archivos_de_prueba_y_verificacion.md`
4. `04_flujo_de_ejecucion.md`
5. `05_crear_exe_y_actualizar_app.md`

> Nota: el archivo principal `projecto_expo.py` es enorme. Por eso la explicación está organizada por bloques de líneas y por funciones, no solo por un único texto largo.
