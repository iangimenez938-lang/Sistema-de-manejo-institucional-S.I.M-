# Archivos de prueba y validación

Este proyecto incluye varios scripts que no forman la app principal, pero sirven para comprobar que la lógica funciona y que los arreglos no rompan el sistema.

---

## 1) `debug_system_check.py`

### Qué hace

Este archivo intenta cargar `projecto_expo.py` y probar varios sistemas de ecuaciones para ver si la función `solve_system()` responde correctamente.

### Estructura

- importa `importlib.util`
- define una ruta absoluta a `projecto_expo.py`
- carga el módulo como si fuera un archivo externo
- prueba ejemplos como:
  - `['3x-2y=7', 'x+3y=17']`
  - `['3x-21=7', 'x+3y=17']`
  - `['3x-2y=7,x+3y=17']`
- guarda los resultados en un archivo llamado `debug_system_check_output.txt`

### Importancia

Sirve para depurar la lógica del sistema y comprobar errores de parsing o de formato.

---

## 2) `process_logging_test.py`

### Qué hace

Este archivo simula eventos de la calculadora sin abrir la interfaz real.

### Idea principal

Se crea un “módulo falso” con clases que imitan widgets Tkinter, para poder ejecutar la lógica sin abrir la ventana.

### Qué comprueba

- Que no se registren pasos innecesarios para clics simples.
- Que sí se registren pasos para una operación real.
- Que el historial de cálculo persista entre sesiones.

### Ejemplos

- `test_no_logging_for_simple_button_clicks()`
- `test_does_log_for_real_result_steps()`
- `test_history_persists_between_sessions()`

### Resultado

Escribe el resultado en:

- `process_logging_test_result.txt`

Esto permite saber si los tests pasan o si hay fallos.

---

## 3) `solver_check.py`

### Qué hace

Este archivo es una prueba básica para verificar que la función `solve_system()` puede resolver sistemas de ecuaciones.

### Entradas de ejemplo

- `3x-2y=7` y `x+3y=17`
- una variante de ecuaciones con signos y paréntesis

### Salida

Imprime el resultado con:

- `print('case1=', module.solve_system(...))`
- `print('case2=', ...)`
- `print('norm=', module.normalize_expression(...))`

### Importancia

Es una comprobación rápida de la lógica antes de desplegar una versión más compleja.

---

## 4) `verify_system_fix.py`

### Qué hace

Este archivo comprueba que los cambios del sistema de ecuaciones resuelven varias situaciones problemáticas.

### Casos evaluados

- sistema normal
- ecuación con token `(=)`
- ecuación con llaves y compresión de texto

### Objetivo

Validar que la parte matemática no solo funciona en un caso ideal, sino también cuando el texto llega con formato distinto o con caracteres raros.

### Salida

Escribe los resultados en un archivo llamado:

- `verify_system_fix_output.txt`

---

## Para qué sirven estos archivos

Estos scripts no son la utilidad final del programa, pero son esenciales para:

- ver si la app resuelve bien,
- detectar errores de sintaxis,
- confirmar que la lógica robusta funciona,
- comprobar que un fix (corrección) realmente resuelve lo que estaba roto.

En otras palabras, son la “prueba de salud” del proyecto.

---

## Ejemplos reales sacados del código

### 1) Prueba de sistema de ecuaciones

```python
for case in [
    ['3x-2y=7', 'x+3y=17'],
    ['3x-21=7', 'x+3y=17'],
    ['3x-2y=7,x+3y=17'],
]:
    try:
        lines.append(f'INPUT: {case}')
        lines.append(f'RESULT: {module.solve_system(case)}')
    except Exception as e:
        lines.append(f'ERROR for {case}: {type(e).__name__}: {e}')
```

Este bloque prueba varios formatos de entrada para comprobar que el sistema acepta ecuaciones bien escritas y también casos con formato más extraño.

### 2) Simulación sin interfaz gráfica

```python
def load_module():
    fake_tk = types.ModuleType('tkinter')
    fake_ttk = types.ModuleType('tkinter.ttk')

    class FakeRoot:
        def __init__(self, *args, **kwargs):
            pass

        def mainloop(self):
            pass
```

Esto permite ejecutar la lógica del programa sin abrir una ventana real, lo cual es útil para tests automáticos.

### 3) Comprueba que se registra el proceso correctamente

```python
def test_does_log_for_real_result_steps():
    ns = load_module()
    ns['label'] = {'text': '7'}
    ns['A'] = '7'
    ns['operator'] = '+'
    ns['B'] = '3'
    ns['process_history'] = ['Calculator ready.']

    ns['button_clicked']('=')

    assert any('Operation:' in step for step in ns['process_history']), ns['process_history']
```

Este test verifica que cuando haces una operación real, el programa añade un paso de proceso al historial. Es una prueba muy útil para asegurarte de que la app no se “calla” cuando hace cálculos.

### 4) Comprobación de persistencia del historial

```python
def test_history_persists_between_sessions():
    history_file = Path(r"c:\Users\pc\OneDrive\Documents\tareas de taller\lab.programacion\proyectoEXPO\test_history.json")
    if history_file.exists():
        history_file.unlink()

    ns['HISTORY_FILE'] = history_file
    ns['calc_history'] = ['Calculator ready.', '2 + 2 = 4']
    ns['save_history_to_disk']()
    ns['calc_history'] = []
    loaded = ns['load_saved_history']()

    assert loaded == ['Calculator ready.', '2 + 2 = 4'], loaded
```

Esto comprueba que el historial se guarda y se vuelve a cargar correctamente.

### Cómo usar esos ejemplos al editar

Cuando modifiques la app, te conviene mantener este patrón:

- prueba la entrada nueva,
- prueba un caso normal,
- prueba un caso anómalo,
- comprueba que el resultado se guarda o no se rompe.

Eso te permitirá mantener la app estable sin tener que adivinar.
