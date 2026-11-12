from .historia_ui import ModuloHistoriaUI 
def build_ui(parent_frame, contexto=None, on_back_callback=None): 
    return ModuloHistoriaUI(parent_frame, contexto=contexto, on_back_callback=on_back_callback)