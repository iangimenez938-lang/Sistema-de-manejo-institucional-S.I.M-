from .tecnologia_ui import ModuloTecnologiaUI 

def build_ui(parent_frame, contexto=None, on_back_callback=None): 
    return ModuloTecnologiaUI(parent_frame, contexto=contexto, on_back_callback=on_back_callback)