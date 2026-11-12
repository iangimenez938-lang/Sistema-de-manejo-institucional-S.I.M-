import sys
import unittest
from pathlib import Path

import tkinter as tk

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_CONTENT = PROJECT_ROOT / "app-content"
if str(APP_CONTENT) not in sys.path:
    sys.path.insert(0, str(APP_CONTENT))

from materias_generales.ed_fisica.ed_fisica_ui import ModuloEdFisicaUI
from materias_generales.ed_fisica.herramientas import (
    calcular_imc_y_composicion,
    calcular_metabolismo_y_calorias,
)


class EdFisicaUITests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_imc_calculation_accepts_valid_numbers(self):
        result = calcular_imc_y_composicion(68, 1.72)
        self.assertNotIn("error", result)
        self.assertGreater(result["imc"], 18.5)
        self.assertLess(result["imc"], 25.1)

    def test_metabolism_calculation_accepts_valid_numbers(self):
        result = calcular_metabolismo_y_calorias(68, 172, 16, nivel_actividad="moderado")
        self.assertNotIn("error", result)
        self.assertGreater(result["calorias_mantenimiento_diarias"], 0)

    def test_module_uses_central_glossary(self):
        ui = ModuloEdFisicaUI(self.root)
        self.assertTrue(hasattr(ui, "glosario_ui"))


if __name__ == "__main__":
    unittest.main()
