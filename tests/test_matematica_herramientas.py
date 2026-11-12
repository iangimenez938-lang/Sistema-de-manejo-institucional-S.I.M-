import sys
import unittest
from pathlib import Path

APP_ROOT = Path(__file__).resolve().parents[1] / "app-content"
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from materias_generales.matematica.matematica_herramientas import (
    analizar_funcion_cuadratica,
    optimizacion_programacion_lineal_2d,
)


class MatematicaHerramientasTests(unittest.TestCase):
    def test_analizar_funcion_cuadratica_incluye_vertice_y_raices(self):
        res = analizar_funcion_cuadratica(1, -3, 2)

        self.assertIn("vertice", res)
        self.assertIn("raices", res)
        self.assertEqual(res["vertice"], (1.5, -0.25))
        self.assertEqual(res["raices"], [1.0, 2.0])

    def test_optimizacion_programacion_lineal_2d_devuelve_optimo(self):
        puntos = [(0, 0), (4, 0), (0, 3), (2, 2)]
        res = optimizacion_programacion_lineal_2d(3, 2, puntos, tipo="max")

        self.assertIn("optimo", res)
        self.assertEqual(res["optimo"]["z"], 12.0)


if __name__ == "__main__":
    unittest.main()
