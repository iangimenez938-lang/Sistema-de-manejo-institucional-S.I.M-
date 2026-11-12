import importlib
import pathlib
import sys
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT / "app-content") not in sys.path:
    sys.path.insert(0, str(ROOT / "app-content"))


class InformaticaIntegrationTests(unittest.TestCase):
    def test_informatica_package_exposes_build_ui(self):
        module = importlib.import_module("materias_taller.informatica")

        self.assertTrue(hasattr(module, "build_ui"))
        self.assertTrue(callable(module.build_ui))


if __name__ == "__main__":
    unittest.main()
