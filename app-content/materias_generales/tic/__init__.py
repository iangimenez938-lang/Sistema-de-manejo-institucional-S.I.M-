from .tic_ui import ModuloTicUI 

def build_ui(parent_frame, contexto=None, on_back_callback=None): 
    return ModuloTicUI(parent_frame, contexto=contexto, on_back_callback=on_back_callback)