import json
import pathlib
import sys
import tempfile
import unittest

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
APP_ROOT = PROJECT_ROOT / "app-content"
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from configuracion.glosario_central import (
    GlosarioCentralUI,
    agregar_entrada_glosario,
    cargar_glosario,
    filtrar_glosario,
)


class GlosarioCentralTests(unittest.TestCase):
    def test_carga_y_filtro_de_glosario(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "glosario.json"
            base = [
                {
                    "nombre": "Inflación",
                    "categorias": ["Economía"],
                    "subcategorias": ["Texto explicativo"],
                    "contenido": "Aumento generalizado de precios.",
                },
                {
                    "nombre": "Adjetivo",
                    "categorias": ["Lengua"],
                    "subcategorias": ["Texto explicativo"],
                    "contenido": "Palabra que acompaña a un sustantivo.",
                },
            ]
            path.write_text(json.dumps(base), encoding="utf-8")

            data = cargar_glosario(path)
            self.assertEqual(len(data), 2)
            self.assertEqual(len(filtrar_glosario(data, "infl", "Economía")), 1)

    def test_agregar_entrada_glosario_guarda_campos_esperados(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = pathlib.Path(tmp) / "glosario.json"
            nueva = {
                "nombre": "Costo fijo",
                "categorias": ["Economía"],
                "subcategorias": ["Texto explicativo"],
                "contenido": "Gasto que no depende del volumen de producción.",
            }
            agregado = agregar_entrada_glosario(path, nueva)
            self.assertTrue(agregado)
            data = cargar_glosario(path)
            self.assertEqual(data[0]["nombre"], "Costo fijo")
            self.assertEqual(data[0]["categorias"], ["Economía"])

    def test_ui_requiere_estructura_basica(self):
        class FakeRoot:
            def __init__(self):
                self.children = []

        root = FakeRoot()
        ui = GlosarioCentralUI(root)
        self.assertTrue(hasattr(ui, "entry_busqueda"))
        self.assertTrue(hasattr(ui, "combo_categoria"))
        self.assertTrue(hasattr(ui, "form_nombre"))
        self.assertTrue(hasattr(ui, "btn_guardar"))
        self.assertTrue(hasattr(ui, "scrollbar"))


if __name__ == "__main__":
    unittest.main()
