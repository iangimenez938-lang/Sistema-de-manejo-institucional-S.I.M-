import importlib
import traceback

modules = [
    'real_informacion_app',
    'creditos_app',
    'matematica.matematica_app',
    'quimica.quimica_app',
    'historia.historia_app',
    'lengua.lengua_app',
    'updater',
]

for m in modules:
    try:
        importlib.import_module(m)
        print(f'OK: {m}')
    except Exception as e:
        print(f'ERR: {m} -> {type(e).__name__}: {e}')
        traceback.print_exc()
