import importlib.util
import sys
import types
import unittest
from pathlib import Path


class FakeWidget:
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        self._config = dict(kwargs)
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

    def get(self, *args, **kwargs):
        return ""

    def set(self, *args, **kwargs):
        return None

    def heading(self, *args, **kwargs):
        return None

    def column(self, *args, **kwargs):
        return None


class FakeRoot(FakeWidget):
    pass


def load_economia_ui_module():
    fake_tk = types.ModuleType("tkinter")
    fake_ttk = types.ModuleType("tkinter.ttk")
    fake_messagebox = types.ModuleType("tkinter.messagebox")

    fake_tk.Frame = FakeWidget
    fake_tk.Label = FakeWidget
    fake_tk.Button = FakeWidget
    fake_tk.Entry = FakeWidget
    fake_tk.Text = FakeWidget
    fake_tk.LabelFrame = FakeWidget
    fake_tk.END = "end"
    fake_tk.StringVar = lambda *args, **kwargs: types.SimpleNamespace(get=lambda: "", set=lambda value: None)
    fake_tk.Tk = FakeRoot
    fake_tk.messagebox = fake_messagebox
    fake_messagebox.showerror = lambda *args, **kwargs: None

    class FakeNotebook(FakeWidget):
        def add(self, *args, **kwargs):
            return None

    class FakeCombobox(FakeWidget):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.values = kwargs.get("values", [])
            self.state = kwargs.get("state", "readonly")
            self._selected = ""

        def set(self, value):
            self._selected = value

        def get(self):
            return self._selected

    fake_ttk.Style = type(
        "FakeStyle",
        (),
        {"__init__": lambda self, *a, **k: None, "theme_use": lambda self, *a, **k: None, "configure": lambda self, *a, **k: None, "map": lambda self, *a, **k: None},
    )
    fake_ttk.Notebook = FakeNotebook
    fake_ttk.Combobox = FakeCombobox

    sys.modules["tkinter"] = fake_tk
    sys.modules["tkinter.ttk"] = fake_ttk
    sys.modules["tkinter.messagebox"] = fake_messagebox

    project_root = Path(__file__).resolve().parents[1]
    app_content_root = project_root / "app-content"
    if str(app_content_root) not in sys.path:
        sys.path.insert(0, str(app_content_root))

    module_name = "materias_generales.economia.economia_ui"
    if module_name in sys.modules:
        del sys.modules[module_name]

    import importlib
    return importlib.import_module(module_name)


class EconomiaUITests(unittest.TestCase):
    def test_economia_ui_keeps_van_out_of_glossary(self):
        module = load_economia_ui_module()
        module.aplicar_estilos_globales = lambda *args, **kwargs: None
        root = FakeRoot()
        ui = module.ModuloEconomiaUI(root)

        self.assertTrue(hasattr(ui, "txt_van_resultado"))
        self.assertFalse(hasattr(ui, "cmb_glosario"))
        self.assertTrue(hasattr(ui, "glosario_ui"))

    def test_economia_glossary_can_show_selected_term(self):
        module = load_economia_ui_module()
        module.aplicar_estilos_globales = lambda *args, **kwargs: None
        root = FakeRoot()
        ui = module.ModuloEconomiaUI(root)

        self.assertTrue(hasattr(ui, "glosario_ui"))
        self.assertFalse(hasattr(ui, "txt_glosario"))


if __name__ == "__main__":
    unittest.main()
