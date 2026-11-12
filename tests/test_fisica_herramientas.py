import importlib.util
from pathlib import Path


def load_fisica_module():
    module_path = Path(__file__).resolve().parents[1] / "app-content" / "materias_generales" / "fisica" / "herramientas.py"
    spec = importlib.util.spec_from_file_location("fisica_herramientas", module_path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_calcular_mru_rechaza_tiempo_no_positivo():
    module = load_fisica_module()
    result = module.calcular_mru(velocidad=None, distancia=20, tiempo=-2)
    assert "error" in result
    assert "mayor a cero" in result["error"]


def test_resolver_ley_ohm_calcula_voltaje_cuando_falta():
    module = load_fisica_module()
    result = module.resolver_ley_ohm(voltaje=None, corriente=2, resistencia=10)
    assert result["voltaje_V"] == 20
    assert result["corriente_A"] == 2
    assert result["resistencia_Ohm"] == 10


def test_analizar_circuito_resistencias_paralelo_incluye_todas_las_resistencias():
    module = load_fisica_module()
    result = module.analizar_circuito_resistencias(12, [2, 3], tipo_circuito="paralelo")
    assert result["tipo"] == "Paralelo"
    assert len(result["detalles_componentes"]) == 2
