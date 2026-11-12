from .labs_hardware_ui import ModuloLabsHardwareUI 

def build_ui(parent_frame, contexto=None, on_back_callback=None): 
    return ModuloLabsHardwareUI(parent_frame, contexto=contexto, on_back_callback=on_back_callback)