from .labs_sistemas_ui import ModuloLabsSistemasUI 

def build_ui(parent_frame, contexto=None, on_back_callback=None): 
    return ModuloLabsSistemasUI(parent_frame, contexto=contexto, on_back_callback=on_back_callback)