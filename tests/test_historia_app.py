import importlib.util
import json
import sys
import tempfile
import types
import unittest
from pathlib import Path


def load_historia_module():
    fake_tk = types.ModuleType('tkinter')
    fake_ttk = types.ModuleType('tkinter.ttk')
    fake_messagebox = types.ModuleType('tkinter.messagebox')

    class FakeWidget:
        def __init__(self, *args, **kwargs):
            pass

        def pack(self, *args, **kwargs):
            pass

        def grid(self, *args, **kwargs):
            pass

        def bind(self, *args, **kwargs):
            pass

        def insert(self, *args, **kwargs):
            pass

        def delete(self, *args, **kwargs):
            pass

        def get(self, *args, **kwargs):
            return ''

        def curselection(self):
            return ()

    fake_tk.Frame = FakeWidget
    fake_tk.Label = FakeWidget
    fake_tk.Button = FakeWidget
    fake_tk.Entry = FakeWidget
    fake_tk.Listbox = FakeWidget
    fake_tk.StringVar = lambda *args, **kwargs: types.SimpleNamespace(set=lambda *a, **k: None, get=lambda *a, **k: '')
    fake_tk.messagebox = fake_messagebox
    fake_messagebox.showerror = lambda *args, **kwargs: None
    fake_ttk.Frame = FakeWidget
    fake_ttk.Notebook = FakeWidget
    fake_tk.ttk = fake_ttk

    sys.modules['tkinter'] = fake_tk
    sys.modules['tkinter.ttk'] = fake_ttk
    sys.modules['tkinter.messagebox'] = fake_messagebox

    module_path = Path(__file__).resolve().parents[1] / 'app-content' / 'historia' / 'historia_app.py'
    spec = importlib.util.spec_from_file_location('historia_app_under_test', module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class HistoriaAppTests(unittest.TestCase):
    def test_save_history_persists_json_file(self):
        module = load_historia_module()

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            module.OTHER_DIR = temp_path
            module.HISTORY_FILE = temp_path / 'historia_history.json'

            module.save_history(['Entre 1492 y 1789: 297 años'])

            self.assertTrue(module.HISTORY_FILE.exists())
            data = json.loads(module.HISTORY_FILE.read_text(encoding='utf-8'))
            self.assertEqual(data, ['Entre 1492 y 1789: 297 años'])

    def test_default_persistence_dir_uses_persistance(self):
        module = load_historia_module()
        self.assertEqual(module.OTHER_DIR.name, 'persistance')

    def test_event_year_is_normalized_case_insensitively(self):
        module = load_historia_module()
        self.assertEqual(module.normalizar_anio_evento('año 1492'), '1492')
        self.assertEqual(module.normalizar_anio_evento('Año 1789'), '1789')


if __name__ == '__main__':
    unittest.main()
