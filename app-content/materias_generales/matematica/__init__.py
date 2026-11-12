# pyright: reportMissingImports=false


def __getattr__(name):
    if name in {"ModuloMatematicaUI", "VistaMatematicaUI"}:
        from .matematica_ui import ModuloMatematicaUI, VistaMatematicaUI
        return {"ModuloMatematicaUI": ModuloMatematicaUI, "VistaMatematicaUI": VistaMatematicaUI}[name]
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def crear_vista_matematica(parent, contexto: dict, on_back_callback=None):
    """Instancia y retorna el módulo de Matemática integrado al contenedor principal."""
    from .matematica_ui import VistaMatematicaUI
    return VistaMatematicaUI(
        parent=parent,
        contexto=contexto,
        on_back_callback=on_back_callback,
    )