import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PERSISTENCE_DIR = PROJECT_ROOT / "persistance"
DEFAULT_GLOSARIO_PATH = PERSISTENCE_DIR / "glosario_central.json"


def _normalizar_entrada(entrada: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(entrada, dict):
        raise ValueError("Cada entrada del glosario debe ser un diccionario.")

    nombre = str(entrada.get("nombre", "")).strip()
    categorias = entrada.get("categorias", [])
    subcategorias = entrada.get("subcategorias", [])
    contenido = str(entrada.get("contenido", "")).strip()

    if not nombre:
        raise ValueError("El nombre del concepto es obligatorio.")

    def _lista(value: Any) -> list[str]:
        if isinstance(value, str):
            return [part.strip() for part in value.split(",") if part.strip()]
        if isinstance(value, (list, tuple, set)):
            return [str(item).strip() for item in value if str(item).strip()]
        return []

    return {
        "nombre": nombre,
        "categorias": _lista(categorias),
        "subcategorias": _lista(subcategorias),
        "contenido": contenido,
    }


def cargar_glosario(path: str | Path | None = None) -> list[dict[str, Any]]:
    target = Path(path) if path is not None else DEFAULT_GLOSARIO_PATH
    if not target.exists():
        return []

    try:
        with open(target, "r", encoding="utf-8") as handle:
            data = json.load(handle)
            if not isinstance(data, list):
                return []
            return [_normalizar_entrada(item) for item in data]
    except Exception:
        return []


def guardar_glosario(datos: list[dict[str, Any]], path: str | Path | None = None) -> bool:
    target = Path(path) if path is not None else DEFAULT_GLOSARIO_PATH
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            json.dump([_normalizar_entrada(item) for item in datos], handle, ensure_ascii=False, indent=2)
        return True
    except Exception:
        return False


def filtrar_glosario(datos: list[dict[str, Any]], texto: str = "", categoria: str = "") -> list[dict[str, Any]]:
    query = str(texto or "").strip().lower()
    categoria_filtro = str(categoria or "").strip().lower()
    resultado: list[dict[str, Any]] = []

    for item in datos:
        nombre = str(item.get("nombre", "")).lower()
        contenido = str(item.get("contenido", "")).lower()
        categorias = [str(cat).lower() for cat in item.get("categorias", [])]

        coincide_texto = not query or query in nombre or query in contenido
        coincide_categoria = not categoria_filtro or categoria_filtro in categorias

        if coincide_texto and coincide_categoria:
            resultado.append(item)

    return resultado


def agregar_entrada_glosario(path: str | Path | None, entrada: dict[str, Any]) -> bool:
    target = Path(path) if path is not None else DEFAULT_GLOSARIO_PATH
    datos_actuales = cargar_glosario(target)
    normalizada = _normalizar_entrada(entrada)
    datos_actuales.append(normalizada)
    return guardar_glosario(datos_actuales, target)


class GlosarioCentralUI:
    """Pantalla reutilizable de glosario con buscador, filtro y almacenamiento local."""

    def __init__(self, parent=None, titulo: str = "Glosario central", data_path: str | Path | None = None):
        self.parent = parent
        self.data_path = Path(data_path) if data_path is not None else DEFAULT_GLOSARIO_PATH
        self.entries = cargar_glosario(self.data_path)
        self.title = titulo

        self.entry_busqueda = None
        self.combo_categoria = None
        self.form_nombre = None
        self.form_categorias = None
        self.form_subcategorias = None
        self.form_contenido = None
        self.lista_resultados = None
        self.detalle_contenido = None
        self.btn_guardar = None
        self.canvas = None
        self.scrollbar = None
        self.lista_scrollbar = None
        self.form_scrollbar = None
        self.detalle_scrollbar = None

        self._build_ui_if_possible()

    def _build_ui_if_possible(self):
        try:
            import tkinter as tk
            from tkinter import ttk
            ui_ready = (
                hasattr(tk, "Frame")
                and hasattr(tk, "Label")
                and hasattr(tk, "Entry")
                and hasattr(tk, "Text")
                and hasattr(tk, "Listbox")
                and hasattr(tk, "LabelFrame")
            )
            if not ui_ready:
                raise RuntimeError("Tk interfas incompleta")
        except Exception:
            self.entry_busqueda = _FakeEntry()
            self.combo_categoria = _FakeComboBox()
            self.form_nombre = _FakeEntry()
            self.form_categorias = _FakeEntry()
            self.form_subcategorias = _FakeEntry()
            self.form_contenido = _FakeText()
            self.lista_resultados = _FakeList()
            self.detalle_contenido = _FakeText()
            self.btn_guardar = _FakeButton(self._guardar_entrada)
            return

        if self.parent is None or not hasattr(self.parent, "tk"):
            self.entry_busqueda = _FakeEntry()
            self.combo_categoria = _FakeComboBox()
            self.form_nombre = _FakeEntry()
            self.form_categorias = _FakeEntry()
            self.form_subcategorias = _FakeEntry()
            self.form_contenido = _FakeText()
            self.lista_resultados = _FakeList()
            self.detalle_contenido = _FakeText()
            self.btn_guardar = _FakeButton(self._guardar_entrada)
            self.scrollbar = _FakeScrollBar()
            self.lista_scrollbar = _FakeScrollBar()
            self.form_scrollbar = _FakeScrollBar()
            self.detalle_scrollbar = _FakeScrollBar()
            return

        self.frame = tk.Frame(self.parent, bg="#ffffff", padx=12, pady=12)
        self.frame.pack(fill="both", expand=True)

        header = tk.Label(self.frame, text=self.title, font=("Arial", 12, "bold"), anchor="w")
        header.pack(fill="x", pady=(0, 8))

        controls = tk.Frame(self.frame, bg="#ffffff")
        controls.pack(fill="x", pady=(0, 8))

        tk.Label(controls, text="Buscar:", font=("Arial", 9, "bold")).pack(side="left")
        self.entry_busqueda = tk.Entry(controls, width=30)
        self.entry_busqueda.pack(side="left", padx=(6, 12))

        categorias = self._categorias_disponibles()
        tk.Label(controls, text="Categoría:", font=("Arial", 9, "bold")).pack(side="left")
        self.combo_categoria = ttk.Combobox(controls, values=categorias, state="readonly", width=20)
        self.combo_categoria.set(categorias[0] if categorias else "")
        self.combo_categoria.pack(side="left")

        btn_filtrar = tk.Button(controls, text="Filtrar", command=self._aplicar_filtro)
        btn_filtrar.pack(side="left", padx=(12, 0))

        body = tk.Frame(self.frame, bg="#ffffff")
        body.pack(fill="both", expand=True)

        left = tk.Frame(body, bg="#f8f9fa", padx=8, pady=8)
        left.pack(side="left", fill="y", expand=False, padx=(0, 8))

        tk.Label(left, text="Resultados", font=("Arial", 9, "bold")).pack(anchor="w")
        self.lista_resultados = tk.Listbox(left, width=28, height=16)
        self.lista_scrollbar = ttk.Scrollbar(left, orient="vertical", command=self.lista_resultados.yview)
        self.lista_resultados.configure(yscrollcommand=self.lista_scrollbar.set)
        self.lista_scrollbar.pack(side="right", fill="y")
        self.lista_resultados.pack(side="left", fill="both", expand=True)
        self.lista_resultados.bind("<<ListboxSelect>>", self._mostrar_detalle_actual)
        self.scrollbar = self.lista_scrollbar

        right = tk.Frame(body, bg="#ffffff")
        right.pack(side="left", fill="both", expand=True)

        form = tk.LabelFrame(right, text="Ficha del concepto", padx=8, pady=8)
        form.pack(fill="both", expand=True, pady=(0, 8))

        tk.Label(form, text="Nombre:", font=("Arial", 8, "bold")).grid(row=0, column=0, sticky="w", padx=4, pady=4)
        self.form_nombre = tk.Entry(form, width=40)
        self.form_nombre.grid(row=0, column=1, sticky="ew", padx=4, pady=4)

        tk.Label(form, text="Categorías:", font=("Arial", 8, "bold")).grid(row=1, column=0, sticky="w", padx=4, pady=4)
        self.form_categorias = tk.Entry(form, width=40)
        self.form_categorias.grid(row=1, column=1, sticky="ew", padx=4, pady=4)

        tk.Label(form, text="Subcategorías:", font=("Arial", 8, "bold")).grid(row=2, column=0, sticky="w", padx=4, pady=4)
        self.form_subcategorias = tk.Entry(form, width=40)
        self.form_subcategorias.grid(row=2, column=1, sticky="ew", padx=4, pady=4)

        tk.Label(form, text="Contenido:", font=("Arial", 8, "bold")).grid(row=3, column=0, sticky="nw", padx=4, pady=4)
        self.form_contenido = tk.Text(form, height=12, wrap="word")
        self.form_contenido.grid(row=3, column=1, sticky="nsew", padx=4, pady=4)
        self.detalle_contenido = self.form_contenido

        if hasattr(form, "grid_columnconfigure"):
            form.grid_columnconfigure(1, weight=1)
        if hasattr(form, "grid_rowconfigure"):
            form.grid_rowconfigure(3, weight=1)

        self.btn_guardar = tk.Button(form, text="Guardar en glosario", command=self._guardar_entrada)
        self.btn_guardar.grid(row=4, column=1, sticky="e", padx=4, pady=(6, 0))

        self._aplicar_filtro()

    def _categorias_disponibles(self) -> list[str]:
        categorias = set()
        for item in self.entries:
            for categoria in item.get("categorias", []):
                categorias.add(str(categoria))
        return sorted(categorias)

    def _aplicar_filtro(self):
        if self.lista_resultados is None:
            return

        categoria = ""
        if self.combo_categoria is not None and hasattr(self.combo_categoria, "get"):
            categoria = str(self.combo_categoria.get() or "")

        texto = ""
        if self.entry_busqueda is not None and hasattr(self.entry_busqueda, "get"):
            texto = str(self.entry_busqueda.get() or "")

        resultados = filtrar_glosario(self.entries, texto, categoria)
        self.lista_resultados.delete(0, "end")
        for item in resultados:
            self.lista_resultados.insert("end", item.get("nombre", "Sin nombre"))

        if resultados:
            self._mostrar_detalle(resultados[0])

    def _mostrar_detalle_actual(self, event=None):
        if self.lista_resultados is None:
            return
        try:
            index = self.lista_resultados.curselection()[0]
            title = self.lista_resultados.get(index)
        except Exception:
            return

        for item in self.entries:
            if item.get("nombre") == title:
                self._mostrar_detalle(item)
                return

    def _mostrar_detalle(self, item: dict[str, Any]):
        if self.form_nombre is None:
            return

        try:
            self.form_nombre.delete(0, "end")
            self.form_categorias.delete(0, "end")
            self.form_subcategorias.delete(0, "end")
            self.form_contenido.delete("1.0", "end")

            self.form_nombre.insert(0, item.get("nombre", ""))
            self.form_categorias.insert(0, ", ".join(item.get("categorias", [])))
            self.form_subcategorias.insert(0, ", ".join(item.get("subcategorias", [])))
            self.form_contenido.insert("1.0", item.get("contenido", ""))

            if hasattr(self.detalle_contenido, "config"):
                self.detalle_contenido.config(state="normal")
        except Exception:
            pass

    def _guardar_entrada(self):
        if self.form_nombre is None:
            return

        try:
            nombre = str(self.form_nombre.get() or "").strip()
            categorias = str(self.form_categorias.get() or "").strip()
            subcategorias = str(self.form_subcategorias.get() or "").strip()
            contenido = str(self.form_contenido.get("1.0", "end") or "").strip() if hasattr(self.form_contenido, "get") else ""

            if not nombre or not contenido:
                return

            entrada = {
                "nombre": nombre,
                "categorias": categorias,
                "subcategorias": subcategorias,
                "contenido": contenido,
            }
            if agregar_entrada_glosario(self.data_path, entrada):
                self.entries = cargar_glosario(self.data_path)
                self._aplicar_filtro()
                if hasattr(self.form_nombre, "delete"):
                    self.form_nombre.delete(0, "end")
                if hasattr(self.form_categorias, "delete"):
                    self.form_categorias.delete(0, "end")
                if hasattr(self.form_subcategorias, "delete"):
                    self.form_subcategorias.delete(0, "end")
                if hasattr(self.form_contenido, "delete"):
                    self.form_contenido.delete("1.0", "end")
        except Exception:
            pass


class _FakeEntry:
    def __init__(self):
        self._value = ""

    def get(self):
        return self._value

    def set(self, value):
        self._value = value

    def delete(self, *args, **kwargs):
        self._value = ""

    def insert(self, *args, **kwargs):
        value = args[1] if len(args) > 1 else ""
        self._value = str(value)


class _FakeComboBox:
    def __init__(self, values=None):
        self._values = list(values or [])
        self._value = self._values[0] if self._values else ""

    def get(self):
        return self._value

    def set(self, value):
        self._value = value


class _FakeText:
    def __init__(self):
        self._value = ""

    def get(self, *args, **kwargs):
        return self._value

    def insert(self, *args, **kwargs):
        value = args[1] if len(args) > 1 else ""
        self._value += str(value)

    def delete(self, *args, **kwargs):
        self._value = ""

    def config(self, **kwargs):
        return None


class _FakeList:
    def __init__(self):
        self.items = []
        self.selection = ()

    def delete(self, *args, **kwargs):
        self.items = []

    def insert(self, *args, **kwargs):
        value = args[1] if len(args) > 1 else ""
        self.items.append(str(value))

    def curselection(self):
        return self.selection

    def get(self, index):
        return self.items[index]


class _FakeScrollBar:
    def __init__(self):
        self.value = 0

    def pack(self, *args, **kwargs):
        return None

    def grid(self, *args, **kwargs):
        return None

    def set(self, *args, **kwargs):
        return None


class _FakeButton:
    def __init__(self, callback=None):
        self.callback = callback

    def pack(self, *args, **kwargs):
        return None
