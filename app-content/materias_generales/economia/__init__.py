from .economia_ui import ModuloEconomiaUI 

def build_ui(parent_frame, contexto=None, on_back_callback=None): 
    return ModuloEconomiaUI(parent_frame, contexto=contexto, on_back_callback=on_back_callback)