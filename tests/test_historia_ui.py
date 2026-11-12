import importlib.util
import sys
import types
import unittest
from pathlib import Path


class FakeWidget:
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        self._config = dict(kwargs)
        self.children = []
        self.master = args[0] if args else None
        self.tk = object()

    def pack(self, *args, **kwargs):
        return None

    def grid(self, *args, **kwargs):
        return None

    def bind(self, *args, **kwargs):
        return None

    def config(self, **kwargs):
        self._config.update(kwargs)

    def cget(self, key):
        return self._config.get(key)

    def insert(self, *args, **kwargs):
        return None

    def delete(self, *args, **kwargs):
        return None

    def heading(self, *args, **kwargs):
        return None

    def column(self, *args, **kwargs):
        return None

    def get(self, *args, **kwargs):
        return ""

    def get_children(self):
        return []


class FakeRoot(FakeWidget):
    pass


def load_historia_ui_module():
    fake_tk = types.ModuleType("tkinter")
    fake_ttk = types.ModuleType("tkinter.ttk")
    fake_messagebox = types.ModuleType("tkinter.messagebox")

    fake_tk.Frame = FakeWidget
    fake_tk.Label = FakeWidget
    fake_tk.Button = FakeWidget
    fake_tk.Entry = FakeWidget
    fake_tk.Text = FakeWidget
    fake_tk.LabelFrame = FakeWidget

    def make_string_var(*args, **kwargs):
        state = {"value": kwargs.get("value", "")}
        return types.SimpleNamespace(
            get=lambda: state["value"],
            set=lambda value: state.__setitem__("value", value),
            trace_add=lambda *a, **k: None,
        )

    fake_tk.StringVar = make_string_var
    fake_tk.Tk = FakeRoot
    fake_tk.END = "end"
    fake_tk.messagebox = fake_messagebox
    fake_messagebox.showerror = lambda *args, **kwargs: None

    class FakeNotebook(FakeWidget):
        def add(self, *args, **kwargs):
            return None

    fake_ttk.Style = type(
        "FakeStyle",
        (),
        {"__init__": lambda self, *a, **k: None, "theme_use": lambda self, *a, **k: None, "configure": lambda self, *a, **k: None, "map": lambda self, *a, **k: None},
    )
    fake_ttk.Notebook = FakeNotebook
    fake_ttk.Combobox = FakeWidget
    fake_ttk.Treeview = FakeWidget

    sys.modules["tkinter"] = fake_tk
    sys.modules["tkinter.ttk"] = fake_ttk
    sys.modules["tkinter.messagebox"] = fake_messagebox

    module_path = Path(__file__).resolve().parents[1] / "app-content" / "materias_generales" / "historia" / "historia_ui.py"
    spec = importlib.util.spec_from_file_location("historia_ui_under_test", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HistoriaUITests(unittest.TestCase):
    def test_history_ui_uses_real_tool_panels(self):
        module = load_historia_ui_module()
        module.aplicar_estilos_globales = lambda *args, **kwargs: None
        root = FakeRoot()
        ui = module.ModuloHistoriaUI(root)

        self.assertTrue(hasattr(ui, "txt_timeline"))
        self.assertTrue(hasattr(ui, "txt_comparacion"))
        self.assertTrue(hasattr(ui, "txt_analisis"))
        self.assertTrue(hasattr(ui, "txt_glosario_h"))

    def test_history_ui_allows_user_events(self):
        module = load_historia_ui_module()
        module.aplicar_estilos_globales = lambda *args, **kwargs: None
        root = FakeRoot()
        ui = module.ModuloHistoriaUI(root)

        self.assertTrue(hasattr(ui, "_agregar_evento_manual"))
        ui.eventos_historia = [{"anio": 1900, "titulo": "Evento base", "descripcion": "base"}]
        ui.entry_anio = types.SimpleNamespace(get=lambda: "1950")
        ui.entry_titulo = types.SimpleNamespace(get=lambda: "Nuevo evento")
        ui.entry_descripcion = types.SimpleNamespace(get=lambda: "Texto del evento")

        ui._agregar_evento_manual()

        self.assertTrue(any(event["titulo"] == "Nuevo evento" for event in ui.eventos_historia))
        self.assertEqual(ui.eventos_historia[0]["anio"], 1900)


if __name__ == "__main__":
    unittest.main()
