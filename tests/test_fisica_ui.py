import importlib
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


class FakeRoot(FakeWidget):
    pass


def load_fisica_ui_module():
    fake_tk = types.ModuleType("tkinter")
    fake_tk.__path__ = []
    fake_ttk = types.ModuleType("tkinter.ttk")
    fake_messagebox = types.ModuleType("tkinter.messagebox")
    fake_colorchooser = types.ModuleType("tkinter.colorchooser")
    fake_font = types.ModuleType("tkinter.font")

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
    fake_tk.colorchooser = fake_colorchooser
    fake_tk.font = fake_font
    fake_messagebox.showerror = lambda *args, **kwargs: None
    fake_colorchooser.askcolor = lambda *args, **kwargs: (None, "#000000")
    fake_font.families = lambda: ["Arial", "Verdana"]

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
    sys.modules["tkinter.colorchooser"] = fake_colorchooser
    sys.modules["tkinter.font"] = fake_font

    project_root = Path(__file__).resolve().parents[1]
    app_content_root = project_root / "app-content"
    if str(app_content_root) not in sys.path:
        sys.path.insert(0, str(app_content_root))

    module_name = "materias_generales.fisica.fisica_ui"
    if module_name in sys.modules:
        del sys.modules[module_name]

    return importlib.import_module(module_name)


class FisicaUITests(unittest.TestCase):
    def test_fisica_ui_uses_central_glossary(self):
        module = load_fisica_ui_module()
        module.aplicar_estilos_globales = lambda *args, **kwargs: None
        root = FakeRoot()
        ui = module.ModuloFisicaUI(root)

        self.assertTrue(hasattr(ui, "glosario_ui"))
        self.assertFalse(hasattr(ui, "txt_glosario"))

    def test_ondas_ui_starts_blank_and_accepts_numeric_frequency(self):
        module = load_fisica_ui_module()
        module.aplicar_estilos_globales = lambda *args, **kwargs: None
        root = FakeRoot()
        ui = module.ModuloFisicaUI(root)

        self.assertEqual(ui.e_freq.get(), "")
        self.assertEqual(ui.e_lambda.get(), "")

        ui.e_freq = type("FakeEntry", (), {"get": lambda self: "10000000"})()
        ui.e_lambda = type("FakeEntry", (), {"get": lambda self: ""})()
        ui.txt_res_ond = FakeWidget()
        module.messagebox.showerror = lambda *args, **kwargs: (_ for _ in ()).throw(AssertionError("No debería mostrar error"))

        ui._calc_ondas()


if __name__ == "__main__":
    unittest.main()
