from .informatica_ui import ModuloInformaticaUI


def build_ui(parent_frame, contexto=None, on_back_callback=None):
    return ModuloInformaticaUI(
        parent=parent_frame,
        contexto=contexto,
        on_back_callback=on_back_callback,
    )


def crear_vista_informatica(parent_frame, contexto=None, on_back_callback=None):
    """Instancia y retorna el módulo principal de Informática integrando sus labs."""
    return build_ui(parent_frame, contexto=contexto, on_back_callback=on_back_callback)
