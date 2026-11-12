import sys
import unittest
from pathlib import Path

import tkinter as tk

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_CONTENT = PROJECT_ROOT / "app-content"
if str(APP_CONTENT) not in sys.path:
    sys.path.insert(0, str(APP_CONTENT))

from materias_generales.ingles.ingles_ui import ModuloInglesUI
from materias_generales.lengua.lengua_ui import ModuloLenguaUI


class InglesLenguaUITests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_ingles_uses_central_glossary(self):
        ui = ModuloInglesUI(self.root)
        self.assertTrue(hasattr(ui, "glosario_ui"))

    def test_lengua_uses_central_glossary(self):
        ui = ModuloLenguaUI(self.root)
        self.assertTrue(hasattr(ui, "glosario_ui"))


if __name__ == "__main__":
    unittest.main()
