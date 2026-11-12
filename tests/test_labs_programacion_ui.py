import importlib.util
import sys
import types
import unittest
from pathlib import Path


class FakeWidget:
    def __init__(self, *args, **kwargs):
        self.kwargs = kwargs
        self.children = []
        self.text = kwargs.get("text", "")
        self._config = dict(kwargs)
        self.master = args[0] if args else None
        self.tk = object()

    def pack(self, *args, **kwargs):
        return None

    def grid(self, *args, **kwargs):
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

    def __call__(self, *args, **kwargs):
        return None


class FakeRoot(FakeWidget):
    pass


def load_labs_programacion_ui_module():
    fake_tk = types.ModuleType("tkinter")
    fake_ttk = types.ModuleType("tkinter.ttk")
    fake_messagebox = types.ModuleType("tkinter.messagebox")

    fake_tk.Frame = FakeWidget
    fake_tk.Label = FakeWidget
    fake_tk.Button = FakeWidget
    fake_tk.Entry = FakeWidget
    fake_tk.Text = FakeWidget
    fake_tk.LabelFrame = FakeWidget
    fake_tk.Tk = FakeRoot
    fake_tk.END = "end"
    fake_tk.messagebox = types.SimpleNamespace(showerror=lambda *a, **k: None)

    class FakeNotebook(FakeWidget):
        def add(self, *args, **kwargs):
            return None

    fake_ttk.Style = type("FakeStyle", (), {"__init__": lambda self, *a, **k: None, "theme_use": lambda self, *a, **k: None, "configure": lambda self, *a, **k: None, "map": lambda self, *a, **k: None})
    fake_ttk.Notebook = FakeNotebook

    sys.modules["tkinter"] = fake_tk
    sys.modules["tkinter.ttk"] = fake_ttk
    sys.modules["tkinter.messagebox"] = fake_messagebox

    module_path = Path(__file__).resolve().parents[1] / "app-content" / "materias_taller" / "informatica" / "labs_programacion" / "labs_programacion_ui.py"
    spec = importlib.util.spec_from_file_location("labs_programacion_ui_under_test", module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LabsProgramacionUITests(unittest.TestCase):
    def test_text_widgets_wrap_long_lines(self):
        module = load_labs_programacion_ui_module()
        module.aplicar_estilos_globales = lambda *args, **kwargs: None
        root = FakeRoot()
        ui = module.ModuloLabsProgramacionUI(root)

        self.assertEqual(ui.txt_codigo.cget("wrap"), "word")
        self.assertEqual(ui.txt_consola.cget("wrap"), "word")
        self.assertEqual(ui.txt_res_diag.cget("wrap"), "word")
        self.assertEqual(ui.txt_res_tv.cget("wrap"), "word")

    def test_module_uses_central_glossary(self):
        module = load_labs_programacion_ui_module()
        module.aplicar_estilos_globales = lambda *args, **kwargs: None
        root = FakeRoot()
        ui = module.ModuloLabsProgramacionUI(root)

        self.assertTrue(hasattr(ui, "glosario_ui"))

    def test_diagram_tab_has_own_editor(self):
        module = load_labs_programacion_ui_module()
        module.aplicar_estilos_globales = lambda *args, **kwargs: None
        root = FakeRoot()
        ui = module.ModuloLabsProgramacionUI(root)

        self.assertTrue(hasattr(ui, "txt_codigo_diagrama"))
        self.assertIsNotNone(ui.txt_codigo_diagrama)


if __name__ == "__main__":
    unittest.main()
