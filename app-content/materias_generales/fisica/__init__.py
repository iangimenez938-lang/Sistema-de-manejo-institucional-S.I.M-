from .fisica_ui import ModuloFisicaUI


def build_ui(parent_frame, contexto=None, on_back_callback=None):
    return ModuloFisicaUI(parent_frame, contexto=contexto, on_back_callback=on_back_callback)
