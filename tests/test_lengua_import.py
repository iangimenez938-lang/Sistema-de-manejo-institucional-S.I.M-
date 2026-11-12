import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP_CONTENT = ROOT / 'app-content'
if str(APP_CONTENT) not in sys.path:
    sys.path.insert(0, str(APP_CONTENT))


def test_lengua_builder_is_importable_from_module():
    import importlib

    module = importlib.import_module('ciclo_avanzado.cuarto.cuarto_informatica.lengua.lengua_app')
    assert hasattr(module, 'build_lengua_ui')
    assert callable(module.build_lengua_ui)
