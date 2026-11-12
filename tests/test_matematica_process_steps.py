import importlib.util
import sys
import types
import unittest
from pathlib import Path


def load_matematica_module():
    fake_tk = types.ModuleType('tkinter')
    fake_ttk = types.ModuleType('tkinter.ttk')
    fake_filedialog = types.ModuleType('tkinter.filedialog')

    class FakeWidget:
        def __init__(self, *args, **kwargs):
            pass

        def pack(self, *args, **kwargs):
            pass

        def grid(self, *args, **kwargs):
            pass

        def configure(self, *args, **kwargs):
            pass

        def bind(self, *args, **kwargs):
            pass

        def insert(self, *args, **kwargs):
            pass

        def delete(self, *args, **kwargs):
            pass

        def see(self, *args, **kwargs):
            pass

    fake_tk.Frame = FakeWidget
    fake_tk.Label = FakeWidget
    fake_tk.Button = FakeWidget
    fake_tk.Text = FakeWidget
    fake_tk.Entry = FakeWidget
    fake_tk.Canvas = FakeWidget
    fake_tk.Listbox = FakeWidget
    fake_tk.Tk = object
    fake_tk.messagebox = types.SimpleNamespace(showerror=lambda *a, **k: None, askyesno=lambda *a, **k: True)
    fake_tk.ttk = fake_ttk
    fake_tk.filedialog = fake_filedialog
    fake_tk.StringVar = lambda *a, **k: None
    fake_tk.END = 'end'
    fake_ttk.Frame = FakeWidget
    fake_ttk.Notebook = FakeWidget
    fake_ttk.Style = FakeWidget
    fake_filedialog.asksaveasfilename = lambda *a, **k: ''
    fake_filedialog.askopenfilename = lambda *a, **k: ''

    sys.modules['tkinter'] = fake_tk
    sys.modules['tkinter.ttk'] = fake_ttk
    sys.modules['tkinter.filedialog'] = fake_filedialog

    module_path = Path(__file__).resolve().parents[1] / 'app-content' / 'matematica' / 'matematica_app.py'
    spec = importlib.util.spec_from_file_location('matematica_app_under_test', module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class ProcessStepTests(unittest.TestCase):
    def test_numeric_process_steps_include_real_equations(self):
        module = load_matematica_module()
        steps = module.build_numeric_process_steps(['3x-4y=-30', '7x+3y=4'], 'Igualación')

        self.assertTrue(any('3x-4y=-30' in step for step in steps), steps)
        self.assertTrue(any('7x+3y=4' in step for step in steps), steps)
        self.assertTrue(any('x =' in step.lower() or 'y =' in step.lower() for step in steps), steps)


if __name__ == '__main__':
    unittest.main()
