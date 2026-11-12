import json 
from pathlib import Path 
from tkinter import ttk 

# Ruta de almacenamiento de la configuración 
CONFIG_FILE = Path("Other/config.json") 

# Configuración visual por defecto 
CONFIG_DEFECTO = { 
    "font_family": "Arial", 
    "font_size": 10, 
    "tema": "Custom", 
    "bg_color": "#ffffff", 
    "fg_color": "#212529", 
    "panel_bg": "#f8f9fa", 
    "accent_color": "#007acc" 
} 

# Temas predefinidos 
TEMAS_PREDEFINIDOS = { 
    "Claro (Estándar)": { "bg_color": "#ffffff", "fg_color": "#212529", "panel_bg": "#f8f9fa", "accent_color": "#007acc" }, 
    "Oscuro (Modo Noche)": { "bg_color": "#1e1e1e", "fg_color": "#d4d4d4", "panel_bg": "#252526", "accent_color": "#0e639c" }, 
    "Sepia (Lectura Relajante)": { "bg_color": "#fbf0d9", "fg_color": "#5f4b32", "panel_bg": "#f4e7ce", "accent_color": "#8d5b4c" }, 
    "Azul Nocturno": { "bg_color": "#0f172a", "fg_color": "#e2e8f0", "panel_bg": "#1e293b", "accent_color": "#38bdf8" } 
} 

def cargar_configuracion(): 
    """Carga la configuración desde Other/config.json o retorna los valores por defecto.""" 
    if CONFIG_FILE.exists(): 
        try: 
            with open(CONFIG_FILE, "r", encoding="utf-8") as f: 
                data = json.load(f) 
                config = CONFIG_DEFECTO.copy() 
                config.update(data) 
                return config 
        except Exception: 
            pass 
        
    return CONFIG_DEFECTO.copy() 

def guardar_configuracion(config): 
    """Guarda la configuración activa en Other/config.json.""" 
    try: 
        CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True) 
        with open(CONFIG_FILE, "w", encoding="utf-8") as f: 
            json.dump(config, f, ensure_ascii=False, indent=2) 
            return True 
    except Exception as e: 
        print(f"Error guardando config.json: {e}") 
        return False 
    
def aplicar_estilos_ttk(root, config): 
    """Aplica la paleta visual configurada a los estilos ttk del árbol de widgets.""" 
    if root is None:
        return

    bg_main = config.get("bg_color", "#ffffff")
    fg_main = config.get("fg_color", "#212529")
    panel_bg = config.get("panel_bg", "#f8f9fa")
    accent = config.get("accent_color", "#007acc")
    font_family = config.get("font_family", "Arial")
    font_size = config.get("font_size", 10)

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    style.configure(".", background=panel_bg, foreground=fg_main, font=(font_family, font_size))
    style.configure("TFrame", background=panel_bg)
    style.configure("TLabel", background=panel_bg, foreground=fg_main, font=(font_family, font_size))
    style.configure("TEntry", fieldbackground=bg_main, foreground=fg_main, insertcolor=fg_main)
    style.configure("TCombobox", fieldbackground=bg_main, foreground=fg_main, background=panel_bg, arrowcolor=accent)
    style.map("TCombobox", fieldbackground=[("readonly", bg_main)], background=[("readonly", panel_bg)], foreground=[("readonly", fg_main)])
    style.configure("TSpinbox", fieldbackground=bg_main, foreground=fg_main, background=panel_bg, arrowcolor=accent)
    style.map("TSpinbox", fieldbackground=[("readonly", bg_main)], background=[("readonly", panel_bg)], foreground=[("readonly", fg_main)])
    style.configure("TButton", background=accent, foreground="#ffffff", padding=(8, 6), font=(font_family, font_size, "bold"))
    style.map("TButton", background=[("active", accent), ("pressed", accent)], foreground=[("active", "#ffffff"), ("pressed", "#ffffff")])
    style.configure("Treeview", background=bg_main, foreground=fg_main, fieldbackground=bg_main, rowheight=max(24, font_size + 10), font=(font_family, font_size))
    style.configure("Treeview.Heading", background=panel_bg, foreground=fg_main, font=(font_family, font_size, "bold"))
    style.map("Treeview", background=[("selected", accent)], foreground=[("selected", "#ffffff")])
    style.configure("TNotebook", background=panel_bg)
    style.configure("TNotebook.Tab", background=panel_bg, foreground=fg_main, padding=(10, 4))
    style.map("TNotebook.Tab", background=[("selected", panel_bg), ("active", panel_bg)], foreground=[("selected", fg_main), ("active", fg_main)])

    try:
        root.configure(bg=bg_main)
    except Exception:
        pass


def aplicar_estilos_globales(root, config): 
    """Aplica la configuración tanto a ttk.Style como a los widgets tk tradicionales.""" 
    aplicar_estilos_ttk(root, config)
    aplicar_estilos_a_widget_tree(root, config)
    
def aplicar_estilos_a_widget_tree(widget, config): 
    """Aplica colores al UI de contenedores sin transformar editores de texto en cajas de texto."""
    if widget is None:
        return

    if getattr(widget, "_skip_theme", False):
        return

    try:
        if not widget.winfo_exists():
            return
    except Exception:
        return

    bg_main = config.get("bg_color", "#ffffff")
    fg_main = config.get("fg_color", "#212529")
    panel_bg = config.get("panel_bg", "#f8f9fa")
    accent = config.get("accent_color", "#007acc")
    font_family = config.get("font_family", "Arial")
    font_size = config.get("font_size", 10)
    try:
        widget_type = widget.winfo_class()
    except Exception:
        return

    try:
        if widget_type == "Entry":
            widget.config(bg=bg_main, fg=fg_main, insertbackground=fg_main, font=(font_family, font_size))

        elif widget_type == "Text":
            widget.config(bg=bg_main, fg=fg_main, font=(font_family, font_size), wrap="word")
            if not hasattr(widget, "_app_scrollbar"):
                try:
                    scroll = ttk.Scrollbar(widget.master if getattr(widget, "master", None) is not None else widget, orient="vertical", command=widget.yview)
                    widget.configure(yscrollcommand=scroll.set)
                    scroll.pack(side="right", fill="y")
                    widget._app_scrollbar = scroll
                except Exception:
                    pass

        # Frames / contenedores nativos
        elif widget_type == "Frame":
            if widget.cget("bg") not in [accent, "#007acc"]:
                widget.config(bg=panel_bg)

        # Canvas nativos
        elif widget_type == "Canvas":
            widget.config(bg=panel_bg)

        elif widget_type == "Label":
            widget.config(bg=panel_bg, fg=fg_main, font=(font_family, font_size))

        elif widget_type == "Button":
            widget.config(bg=panel_bg, fg=fg_main, font=(font_family, font_size))
    except Exception:
        pass

    # Aplicar recursivamente a todos los elementos hijos
    for child in widget.winfo_children():
        aplicar_estilos_a_widget_tree(child, config)