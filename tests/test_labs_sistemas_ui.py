import sys
import unittest
from pathlib import Path

import tkinter as tk

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_CONTENT = PROJECT_ROOT / "app-content"
if str(APP_CONTENT) not in sys.path:
    sys.path.insert(0, str(APP_CONTENT))

from materias_taller.informatica.labs_sistemas.herramientas import (
    calcular_permisos_posix,
    diagnosticar_recursos_sistema,
)
from materias_taller.informatica.labs_sistemas.labs_sistemas_ui import ModuloLabsSistemasUI


class LabsSistemasUITests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_chmod_accepts_valid_octal(self):
        res = calcular_permisos_posix("755")
        self.assertNotIn("error", res)
        self.assertIn("rwx", res["notacion_simbolica"])

    def test_system_diagnostic_accepts_values(self):
        res = diagnosticar_recursos_sistema(58, 67, 74, "normal")
        self.assertNotIn("error", res)
        self.assertIn("estado_general", res)

    def test_module_uses_central_glossary(self):
        ui = ModuloLabsSistemasUI(self.root)
        self.assertTrue(hasattr(ui, "glosario_ui"))


if __name__ == "__main__":
    unittest.main()
