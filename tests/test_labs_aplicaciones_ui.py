import sys
import unittest
from pathlib import Path

import tkinter as tk

PROJECT_ROOT = Path(__file__).resolve().parents[1]
APP_CONTENT = PROJECT_ROOT / "app-content"
if str(APP_CONTENT) not in sys.path:
    sys.path.insert(0, str(APP_CONTENT))

from materias_taller.informatica.labs_aplicaciones.herramientas import (
    ejecutar_consulta_sql_simulada,
    obtener_plantilla_componente_web,
)
from materias_taller.informatica.labs_aplicaciones.labs_aplicaciones_ui import ModuloLabsAplicacionesUI


class LabsAplicacionesUITests(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.root.withdraw()

    def tearDown(self):
        self.root.destroy()

    def test_sql_query_returns_rows(self):
        result = ejecutar_consulta_sql_simulada("SELECT nombre, promedio FROM estudiantes WHERE promedio >= 8.5 ORDER BY promedio DESC")
        self.assertNotIn("error", result)
        self.assertGreater(result["total_registros"], 0)

    def test_component_template_is_available(self):
        result = obtener_plantilla_componente_web("Formulario de Login")
        self.assertNotIn("error", result)
        self.assertIn("html", result)
        self.assertIn("css", result)

    def test_module_uses_central_glossary(self):
        ui = ModuloLabsAplicacionesUI(self.root)
        self.assertTrue(hasattr(ui, "glosario_ui"))


if __name__ == "__main__":
    unittest.main()
