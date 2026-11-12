# 09. Arquitectura general del proyecto y cómo ampliar la app

## 1. Idea central: el proyecto está organizado por capas

La aplicación no debe pensarse como una sola pantalla gigante. La forma correcta de verla es como una colección de módulos que cumplen funciones distintas.

La estructura lógica es esta:

1. Capa de arranque
   - [projecto_expo.py](../../projecto_expo.py)
   - crea la ventana principal
   - crea las pestañas
   - importa cada módulo y lo monta

2. Capa de navegación
   - [app-content/general_info_app.py](../../app-content/general_info_app.py)
   - funciona como índice general
   - organiza las materias y subapartados
   - sirve como dashboard central

3. Capa de contenido funcional
   - [app-content/matematica/matematica_app.py](../../app-content/matematica/matematica_app.py)
   - [app-content/quimica/quimica_app.py](../../app-content/quimica/quimica_app.py)
   - [app-content/real_informacion_app.py](../../app-content/real_informacion_app.py)
   - cada uno gestiona un dominio concreto

4. Capa de persistencia
   - JSON, historial, datos de usuario, referencias, elementos, notas
   - guardado local del programa

5. Capa de actualización
   - [updater.py](../../updater.py)
   - comprueba versiones, descarga y prepara instalación

Esto es lo que hace que el programa sea mantenible: cada módulo tiene una responsabilidad.

---

## 2. Cómo debe funcionar general_info_app.py como índice

La idea correcta para [app-content/general_info_app.py](../../app-content/general_info_app.py) es que sea un panel organizador, no un módulo con lógica técnica compleja.

Debe hacer cosas como:

- mostrar una portada del proyecto,
- agrupar materias por categorías,
- ofrecer acceso rápido a cada dominio,
- cargar sub-pantallas dentro de la app,
- dejar claro qué existe y dónde está cada contenido.

### Categorías sugeridas

La mejor forma de pensar en la app es esta:

- Materias
  - Matemática
  - Química
  - Física
  - Programación
  - etc.

- Información
  - RealInformación
  - Créditos
  - Proyecto
  - Documentación

- Herramientas
  - Historial
  - Notas
  - Configuración
  - Exportación

### Regla importante

Cada categoría debe apuntar a un módulo independiente. Es decir:

- Matemática = un módulo de matemáticas
- Química = otro módulo de química
- RealInformación = un módulo de referencias
- Créditos = un módulo de presentación

No se debe meter toda la lógica dentro del índice.

El índice debe actuar como router o hub.

---

## 3. Qué es un routing simple en Tkinter

En este proyecto el patrón es:

- crear un frame para la pestaña,
- crear un sub-notebook
- dentro de cada subframe, cargar un módulo concreto,
- y dejar que ese módulo dibuje su propio contenido.

Por ejemplo, el flujo típico es:

```python
for label, target_module in [
    ("Matematica", "matematica"),
    ("Quimica", "quimica"),
    ("RealInformacion", "realinfo"),
    ("Creditos", "creditos"),
]:
    subframe = ttk.Frame(sections)
    sections.add(subframe, text=label)

    if target_module == "matematica":
        from matematica.matematica_app import build_matematica_ui
        build_matematica_ui(subframe, root)
```

Esto es el patrón base para "navegación por módulos".

La idea es muy clara:

- el índice conoce el nombre del módulo,
- el módulo sabe cómo dibujarse,
- la app principal solo monta y conecta.

---

## 4. Cómo añadir una nueva materia

Supongamos que quieres crear una sección nueva llamada Física.

### Paso 1: Crear una carpeta o archivo nuevo

Puedes hacerlo dentro de app-content, por ejemplo:

- app-content/fisica/
- o un archivo fisica_app.py si quieres algo más simple

### Paso 2: Crear la función del UI

Cada módulo debe tener una función con este patrón:

```python
def build_fisica_ui(fisica_tab, root=None):
    # crear widgets
    # crear paneles
    # devolver el frame
    return fisica_tab
```

Eso es muy importante: la función debe ser independiente y reutilizable.

### Paso 3: Diseñar la estructura interna

Dentro del módulo debes decidir:

- habrá un notebook interno,
- habrá varias pestañas,
- habrá un panel general,
- habrá un historial,
- habrá un formulario,
- habrá un panel de explicación.

### Paso 4: Conectar la nueva materia desde el índice

En [app-content/general_info_app.py](../../app-content/general_info_app.py) tienes que hacer algo parecido a esto:

```python
for label, target_module in [
    ("Matematica", "matematica"),
    ("Quimica", "quimica"),
    ("Fisica", "fisica"),
]:
    subframe = ttk.Frame(sections)
    sections.add(subframe, text=label)

    if target_module == "fisica":
        from fisica.fisica_app import build_fisica_ui
        build_fisica_ui(subframe, root)
```

### Paso 5: Añadir la nueva pestaña al lanzador principal

Si quieres que sea una pestaña principal en la ventana principal, hay que editar [projecto_expo.py](../../projecto_expo.py) con el patrón de:

```python
fisica_tab = ttk.Frame(notebook)
notebook.add(fisica_tab, text="Fisica")
build_fisica_ui(fisica_tab, root)
```

### Regla práctica

Nunca escribas el contenido completo de una nueva materia dentro del archivo principal. Todo debe ir dentro de su propio módulo y ser importado desde allí.

---

## 5. Cómo crear un UI en Tkinter de forma ordenada

Cuando creas un módulo nuevo, lo ideal es seguir siempre esta estructura:

### A. Definir la función principal del UI

```python
def build_mi_modulo_ui(tab, root=None):
    frame = tk.Frame(tab)
    frame.pack(fill="both", expand=True)
    return tab
```

### B. Crear contenedores por responsabilidades

En lugar de mezclar todo en una sola zona, separa:

- cabecera
- filtros
- formularios
- resultados
- historial
- botones de acción

Ejemplo:

```python
header = tk.Frame(frame)
header.pack(fill="x")

form = tk.Frame(frame)
form.pack(fill="x")

results = tk.Frame(frame)
results.pack(fill="both", expand=True)
```

### C. Usar variables de control

Tkinter funciona mejor si usas variables para los valores:

```python
var_nombre = tk.StringVar()
var_resultado = tk.StringVar()
```

Esto permite:

- actualizar textos fácilmente,
- ligar el valor visual a un dato real,
- y centralizar el estado.

### D. Usar Listbox para historial

Si quieres un historial visual, usa Listbox:

```python
history_listbox = tk.Listbox(frame)
history_listbox.pack(fill="both", expand=True)
```

Luego cada vez que se completa una operación, haces:

```python
history_listbox.insert("end", "Texto del historial")
```

---

## 6. Cómo conectar todo: patrón recomendado

La conexión entre módulos debe seguir un patrón simple.

### Patrón base

- cada módulo expone una función `build_x_ui(...)`
- el lanzador principal llama a esas funciones
- la pantalla general llama también a esas funciones si se quiere un índice
- cada módulo usa sus propios datos y archivos

### Dependencias

Si un módulo necesita información de otro, se hace mediante importación:

```python
from quimica.quimica_app import PERIODIC_TABLE
```

Esto es válido siempre que el módulo dependiente esté en la estructura correcta y el `sys.path` haya sido configurado.

### Recomendación

Evita:

- poner toda la lógica dentro del archivo principal,
- duplicar datos entre módulos,
- guardar la misma información en varios sitios sin control,
- y mezclar navegación con cálculo.

---

## 7. Cómo construir sistemas de historial

El historial es una pieza clave para que la app parezca más útil y más profesional.

### Objetivo del historial

Un historial sirve para:

- recordar operaciones pasadas,
- volver a cargar una expresión,
- guardar una decisión del usuario,
- mantener trazabilidad del proceso,
- y reutilizar datos sin repetir trabajo.

### Patrón mínimo que debes seguir

1. crear una lista en memoria
2. mostrarla en un Listbox
3. guardar la lista en un JSON
4. cargarla al inicio
5. ofrecer borrar o deshacer

Ejemplo conceptual:

```python
history = []

def load_history():
    return json.loads(file.read_text()) if file.exists() else []

def save_history(history):
    file.write_text(json.dumps(history, ensure_ascii=False))

def add_history_entry(value):
    history.append(value)
    save_history(history)
```

### Mejor práctica

Haz que cada módulo tenga:

- carga de historial al iniciar,
- guardado automático después de cada acción,
- lista visual para navegar,
- función para borrar o restaurar elementos.

Esto convierte el historial en una funcionalidad real, no solo en una lista sin persistencia.

---

## 8. Cómo guardar información del usuario

El proyecto ya usa JSON como formato de almacenamiento. Eso es una muy buena decisión.

### ¿Por qué JSON?

Porque es:

- simple,
- legible,
- fácil de depurar,
- compatible con Python,
- y suficiente para guardar estructuras complejas como listas y diccionarios.

### Patrón recomendado

Cada módulo puede tener su propia estructura de almacenamiento, por ejemplo:

- `general_info.json`
- `element_info.json`
- `calculator_history.json`
- `molecule_history.json`

Y cada uno puede gestionar sus propios datos de forma independiente.

### Recomendación de diseño

No guardes todo en un único archivo gigante. Es mejor:

- separar datos por dominio,
- usar claves claras,
- tener una función de carga y otra de guardado,
- y mantener compatibilidad con archivos antiguos.

---

## 9. Cómo crear una nueva materia bien hecha

Si quieres crear una nueva materia, usa este checklist:

### Checklist

- [ ] Crear un módulo nuevo o una carpeta nueva
- [ ] Preparar una función `build_x_ui(frame, root)`
- [ ] Dibujar la estructura visual en frames
- [ ] Añadir formularios, resultados y historial
- [ ] Guardar los datos en JSON si hace falta
- [ ] Importarlo desde el índice
- [ ] Añadirlo a la ventana principal si es una pestaña de nivel superior
- [ ] Probar que el UI se abre sin errores

Esto garantiza que la nueva materia se integre bien sin romper el diseño global.

---

## 10. Cómo pensar en la app como un sistema modular

La pregunta clave no es: "¿cómo hago una pantalla?".

La pregunta correcta es:

"¿cómo divido el programa en módulos con una responsabilidad clara?"

En la práctica, cada parte debe responder a una pregunta:

- Matemática: ¿qué cálculo o recurso ofrece?
- Química: ¿qué fórmula, elemento o dato gestiona?
- RealInformación: ¿qué referencias o enlaces almacena?
- Créditos: ¿cómo se presenta el proyecto?
- General: ¿cómo organiza y conecta todo?

Cuando cada módulo responde a una cuestión concreta, el proyecto se vuelve más entendible y ampliable.

---

## 11. Ejemplo de arquitectura ideal para tu proyecto

La estructura mental recomendada es esta:

- General
  - Materias
    - Matemática
    - Química
    - Física
    - Programación
  - Información
    - RealInformación
    - Créditos
    - Documentación
  - Herramientas
    - Historial
    - Notas
    - Configuración

Esto hace que la app sea escalable y que el usuario siempre tenga un punto central desde el que navegar.

---

## 12. Conclusión

El verdadero secreto de este proyecto es que [app-content/general_info_app.py](../../app-content/general_info_app.py) no debe ser solo una pantalla bonita; debe comportarse como un índice inteligente de contenido.

Desde ahí, cada materia debe ser un módulo independiente, con:

- UI propia,
- estado propio,
- historial propio,
- guardado propio,
- y conexión clara con el sistema principal.

Eso es lo que te permite crecer la app sin hacer un monstruo de código.

Si quieres, el siguiente paso ideal es que te haga una guía práctica de ejemplo para:

1. crear una nueva materia llamada Física,
2. montar su UI,
3. conectarla al índice,
4. añadir historial y almacenamiento JSON,
5. y dejarla funcionando dentro del proyecto real.
