# Guía para ampliar la aplicación con estructura modular

Esta guía está pensada para añadir nuevas materias, pestañas o paneles sin romper la lógica principal de la app.

La arquitectura actual ya no está en un único archivo gigante. Cada materia vive en su propio archivo dentro de app-content y el lanzador solo se encarga de crear las pestañas e importarlas.

La estructura base es esta:

- app-content/projecto_expo.py: lanzador principal de la app
- app-content/general_info_app.py: pestaña General
- app-content/real_informacion_app.py: pestaña RealInformacion
- app-content/creditos_app.py: pestaña Creditos
- app-content/matematica/matematica_app.py: toda la lógica de Matemática
- app-content/quimica/quimica_app.py: toda la lógica de Química
- Other/: datos sueltos, JSON y archivos auxiliares

---

## 1) Cómo funciona el sistema actual

El launcher crea un Notebooks de pestañas principales y luego llama a cada módulo para que monte su contenido:

```python
root = tk.Tk()
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

general_tab = ttk.Frame(notebook)
realinfo_tab = ttk.Frame(notebook)
matematica_tab = ttk.Frame(notebook)
quimica_tab = ttk.Frame(notebook)
creditos_tab = ttk.Frame(notebook)

notebook.add(general_tab, text="General")
notebook.add(realinfo_tab, text="RealInformacion")
notebook.add(matematica_tab, text="Matematica")
notebook.add(quimica_tab, text="Quimica")
notebook.add(creditos_tab, text="Creditos")

build_general_info_ui(general_tab, root)
build_real_informacion_ui(realinfo_tab, root)
build_matematica_ui(matematica_tab, root)
build_quimica_ui(quimica_tab, root)
build_creditos_ui(creditos_tab, root)
```

Esto es importante: cada módulo se encarga de construir su propia UI y su propia lógica, y el launcher solo hace la composición.

---

## 2) Regla para añadir una nueva materia

Si quieres añadir una nueva sección, lo correcto es crear un archivo nuevo dentro de app-content y luego importarlo en el launcher.

### Patrón recomendado

Crea algo como esto:

- app-content/estadistica/estadistica_app.py

Dentro del archivo define una función con este formato:

```python
def build_estadistica_ui(estadistica_tab, root):
    # crear widgets, formularios, botones, textos, etc.
    return estadistica_tab
```

La función debe devolver el frame principal para que el launcher la pueda usar sin problemas.

---

## 3) Cómo conectar la nueva materia al launcher

En app-content/projecto_expo.py añadimos la importación y la pestaña nueva.

### Ejemplo

```python
from estadistica.estadistica_app import build_estadistica_ui
```

Luego creamos el frame y lo añadimos al notebook:

```python
estadistica_tab = ttk.Frame(notebook)
notebook.add(estadistica_tab, text="Estadistica")
```

Y finalmente la montamos:

```python
build_estadistica_ui(estadistica_tab, root)
```

Así queda todo ordenado por materia y no se mezclan cosas del tema nuevo con el resto del programa.

---

## 4) Cómo estructurar cada materia

Cada archivo de materia debe tener una responsabilidad clara:

- crear la UI del tema
- guardar o leer su información si hace falta
- mantener su lógica local
- no mezclar varias materias en el mismo archivo

### Buen patrón

```python
import tkinter as tk
from tkinter import ttk


def build_estadistica_ui(estadistica_tab, root):
    titulo = tk.Label(estadistica_tab, text="Estadística", font=("Arial", 14, "bold"))
    titulo.pack(anchor="w", padx=12, pady=(12, 8))

    panel = tk.Frame(estadistica_tab)
    panel.pack(fill="both", expand=True, padx=12, pady=8)

    entrada = tk.Entry(panel)
    entrada.pack(fill="x", padx=10, pady=10)

    boton = tk.Button(panel, text="Calcular", command=lambda: print("Ejecutado"))
    boton.pack(padx=10, pady=10)

    return estadistica_tab
```

Ves que la lógica queda separada y el launcher no necesita saber detalles internos del tema.

---

## 5) Cómo guardar información de un tema nuevo

Si la materia necesita persistencia, usa archivos separados y no mezcles bases de datos globales con la interfaz.

### Recomendación

- usa archivos JSON en Other para almacenamiento general
- si el tema tiene un historial o configuración propia, crea su propio JSON o usa un diccionario dentro del módulo
- mantén las rutas relativas al proyecto, no al directorio del archivo de la materia si puedes evitarlo

Ejemplo recomendado:

```python
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_FILE = PROJECT_ROOT / "Other" / "estadistica.json"
```

Si quieres evitar errores de importación, nunca dependas de rutas tipo “escritas a mano” dentro de cada ordenador. Usa Path y __file__.

---

## 6) Cómo añadir subpestañas dentro de una materia

Si una materia necesita varias secciones internas, puedes crear un Notebook dentro del frame principal.

### Ejemplo

```python
sub_notebook = ttk.Notebook(estadistica_tab)
sub_notebook.pack(fill="both", expand=True)

panel_principal = ttk.Frame(sub_notebook)
panel_resultados = ttk.Frame(sub_notebook)

sub_notebook.add(panel_principal, text="Datos")
sub_notebook.add(panel_resultados, text="Resultados")
```

Esto es útil para temas como:

- Matemática: Calculator, Notas, Metodos
- Química: Elementos, Moleculas, Historial
- Estadística: Datos, Gráficos, Resumen

---

## 7) Cómo pasar datos entre pestañas y subpestañas

Esta es una de las dudas más comunes cuando una materia tiene varias secciones. Por ejemplo:

- en una subpestaña tienes un historial o una lista de resultados,
- quieres que otro tab muestre ese mismo historial,
- o quieres que una pestaña “reciba” texto, cálculo o información que se ha generado en otra.

La solución recomendada es no depender del orden visual de las pestañas, sino usar un estado compartido o un registro central.

### Opción recomendada: estado compartido

```python
shared_state = {
    "historial": [],
    "ultimo_resultado": ""
}


def guardar_en_historial(valor):
    shared_state["historial"].append(valor)
    shared_state["ultimo_resultado"] = valor


def mostrar_historial_en_otro_tab():
    historial = shared_state["historial"]
    print(historial)
```

Con esto, cualquier pestaña puede leer o escribir en el mismo diccionario y no depende de que una esté “más arriba” en la interfaz.

### Ejemplo real: historial en subpestaña y mostrarlo en otra pestaña

```python
shared_state = {"historial": []}


def guardar_historial(texto):
    shared_state["historial"].append(texto)


def crear_historial_tab(datos_tab):
    historial_listbox = tk.Listbox(datos_tab)
    historial_listbox.pack(fill="both", expand=True)

    def actualizar_historial():
        historial_listbox.delete(0, tk.END)
        for item in shared_state["historial"]:
            historial_listbox.insert(tk.END, item)

    guardar_btn = tk.Button(
        datos_tab,
        text="Guardar en historial",
        command=lambda: (guardar_historial("Operación realizada"), actualizar_historial())
    )
    guardar_btn.pack()

    return historial_listbox


def crear_resumen_tab(resumen_tab):
    label = tk.Label(resumen_tab, text="Historial actual:")
    label.pack()

    def refrescar_resumen():
        texto = "\n".join(shared_state["historial"]) if shared_state["historial"] else "Sin historial"
        label.config(text=texto)

    boton = tk.Button(resumen_tab, text="Actualizar resumen", command=refrescar_resumen)
    boton.pack()
```

En este patrón:

- la subpestaña escribe en shared_state
- la otra pestaña consulta el mismo valor
- al pulsar un botón o al ejecutar una función, la segunda vista se actualiza

### Opción más limpia: usar variables tkinter compartidas

Si una pestaña necesita mostrar un valor en directo, puedes también usar `StringVar`, `IntVar`, `BooleanVar`, etc.

```python
resultado_var = tk.StringVar(value="Sin resultado")


def calcular():
    resultado_var.set("Resultado: 42")


def crear_tab_resultado(tab):
    label = tk.Label(tab, textvariable=resultado_var)
    label.pack()

    btn = tk.Button(tab, text="Calcular", command=calcular)
    btn.pack()
```

Aquí, todas las partes que usen `resultado_var` ven el mismo valor sin necesidad de pasar parámetros complejos.

### Regla práctica

Cuando una pestaña necesita “comunicarse” con otra, suele funcionar bien esta lógica:

1. crear un estado central (`dict`, `StringVar`, `list`)
2. cada pestaña lee y escribe ese estado
3. cada acción actualiza la otra vista con una función de refresco
4. no copies datos por toda la app si puedes centralizarlos

### Ejemplo típico de historial entre tabs

```python
state = {
    "historial": ["Inicio", "Cálculo 1"]
}


def crear_tab_historial(tab):
    listbox = tk.Listbox(tab)
    listbox.pack(fill="both", expand=True)

    def refrescar():
        listbox.delete(0, tk.END)
        for item in state["historial"]:
            listbox.insert(tk.END, item)

    refrescar()
    return listbox, refrescar


def crear_tab_resumen(tab):
    label = tk.Label(tab, text="")
    label.pack()

    def actualizar_resumen():
        texto = "\n".join(state["historial"])
        label.config(text=texto)

    boton = tk.Button(tab, text="Ver historial", command=actualizar_resumen)
    boton.pack()
```

Esto es muy útil para casos reales como:

- historial de cálculos en Matemática
- lista de moléculas en Química
- notas o textos guardados en otra subpestaña
- resultados que se muestran en una vista resumen y luego deben aparecer en otra

---

## 8) Qué evitar

Para mantener la app ordenada, evita estas prácticas:

- meter lógica de varios temas en un mismo archivo
- poner widgets de una materia dentro de otra materia
- guardar JSON en rutas distintas según cada archivo
- crear un launcher con miles de funciones encadenadas
- mezclar UI, cálculo y persistencia en un solo bloque gigante
- duplicar el mismo historial en varios widgets sin un origen único

---

## 9) Cómo añadir una nueva materia paso a paso

1. crea una carpeta nueva dentro de app-content si hace falta
2. crea un archivo de tema, por ejemplo estadistica_app.py
3. define la función build_estadistica_ui(tab, root)
4. crea el contenido visual dentro de ese frame
5. añade la importación al launcher
6. crea la pestaña y llama a la función
7. si hace falta, guarda sus datos en Other o en un JSON propio
8. prueba que la interfaz carga bien y que tus datos persisten correctamente

---

## 10) Ejemplo completo de patrón

```python
# archivo: app-content/estadistica/estadistica_app.py
import tkinter as tk


def build_estadistica_ui(estadistica_tab, root):
    title = tk.Label(estadistica_tab, text="Estadística", font=("Arial", 14, "bold"))
    title.pack(anchor="w", padx=12, pady=(12, 8))

    panel = tk.Frame(estadistica_tab)
    panel.pack(fill="both", expand=True, padx=12, pady=8)

    entry = tk.Entry(panel)
    entry.pack(fill="x", padx=10, pady=10)

    button = tk.Button(panel, text="Guardar", command=lambda: print(entry.get()))
    button.pack(padx=10, pady=(0, 10))

    return estadistica_tab
```

Y luego en el launcher:

```python
from estadistica.estadistica_app import build_estadistica_ui

estadistica_tab = ttk.Frame(notebook)
notebook.add(estadistica_tab, text="Estadistica")
build_estadistica_ui(estadistica_tab, root)
```

---

## 11) Resumen rápido

La app ya no se expande “todo junto”. Ahora la regla es:

- un tema = un archivo
- un archivo = una función de construcción
- un launcher = composición de módulos

Esto hace que el proyecto sea más claro, más fácil de mantener y mucho más fácil de ampliar en el futuro.

Si quieres añadir un nuevo tema, lo más natural es crear un nuevo archivo dentro de app-content y conectarlo al launcher con una sola importación y una sola llamada a la función de montaje.
