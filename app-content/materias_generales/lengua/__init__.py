from .lengua_ui import ModuloLenguaUI 

def build_ui(parent_frame, contexto=None, on_back_callback=None): 
    return ModuloLenguaUI(parent_frame, contexto=contexto, on_back_callback=on_back_callback)