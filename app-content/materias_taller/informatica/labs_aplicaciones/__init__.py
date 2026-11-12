from .labs_aplicaciones_ui import ModuloLabsAplicacionesUI 

def build_ui(parent_frame, contexto=None, on_back_callback=None): 
    return ModuloLabsAplicacionesUI(parent_frame, contexto=contexto, on_back_callback=on_back_callback)