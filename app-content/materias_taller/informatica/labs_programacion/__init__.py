from .labs_programacion_ui import ModuloLabsProgramacionUI 

def build_ui(parent_frame, contexto=None, on_back_callback=None): 
    return ModuloLabsProgramacionUI(parent_frame, contexto=contexto, on_back_callback=on_back_callback)