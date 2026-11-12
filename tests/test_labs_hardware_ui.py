import sys
import unittest
from pathlib import Path

import tkinter as tk

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_CONTENT = PROJECT_ROOT / "app-content"
if str(APP_CONTENT) not in sys.path:
    sys.path.insert(0, str(APP_CONTENT))

from materias_taller.informatica.labs_hardware.herramientas import (
    calcular_consumo_psu,
    verificar_compatibilidad_ensamble,
)
from materias_taller.informatica.labs_hardware.labs_hardware_ui import ModuloLabsHardwareUI


class LabsHardwareUITests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_psu_calculation_accepts_valid_values(self):
        result = calcular_consumo_psu(125, 220)
        self.assertNotIn("error", result)
        self.assertGreater(result["psu_recomendada_watts"], 0)

    def test_assembly_compatibility_recognizes_valid_config(self):
        result = verificar_compatibilidad_ensamble("AM4", "DDR4")
        self.assertNotIn("error", result)
        self.assertTrue(result["es_compatible"])

    def test_module_uses_central_glossary(self):
        ui = ModuloLabsHardwareUI(self.root)
        self.assertTrue(hasattr(ui, "glosario_ui"))


if __name__ == "__main__":
    unittest.main()
