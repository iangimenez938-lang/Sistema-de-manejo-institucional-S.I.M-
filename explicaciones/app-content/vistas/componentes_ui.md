import tkinter as tk 
from tkinter import ttk 

try: 
    HAS_TKINTER = True 
except ImportError: 
    HAS_TKINTER = False 
    
class HeaderBar(tk.Frame): 
    """Encabezado superior reutilizable para la aplicación y módulos.""" 
    def __init__(self, parent, titulo="Sistema Educativo Técnico", subtitulo="Plan de Estudio e Integración Modular", bg_color="#007acc", on_home_click=None, on_config_click=None, on_creditos_click=None, fg_title="#ffffff", fg_subtitle="#e0f2fe", button_bg="#ffffff", button_fg="#007acc"):
        super().__init__(parent, bg=bg_color, padx=12, pady=8) 
        self.pack(fill="x", side="top") 
        
        # Panel izquierdo para títulos 
        frame_textos = tk.Frame(self, bg=bg_color) 
        frame_textos.pack(side="left", fill="both", expand=True) 
        
        lbl_t = tk.Label(frame_textos, text=titulo, font=("Arial", 12, "bold"), fg=fg_title, bg=bg_color, justify="left", wraplength=700) 
        lbl_t.pack(anchor="w", fill="x") 
        
        if subtitulo: 
            lbl_s = tk.Label(frame_textos, text=subtitulo, font=("Arial", 9), fg=fg_subtitle, bg=bg_color, justify="left", wraplength=700) 
            lbl_s.pack(anchor="w", fill="x") 
        
        buttons_frame = tk.Frame(self, bg=bg_color) 
        buttons_frame.pack(side="right")

        # 🏠 Botón de Regreso a Inicio (Derecha) 
        if on_home_click: 
            btn_home = tk.Button( buttons_frame, text="🏠 Inicio", command=on_home_click, bg=button_bg, fg=button_fg, font=("Arial", 9, "bold"), relief="groove", bd=1, padx=10, pady=4, cursor="hand2" ) 
            btn_home.pack(side="left", padx=(8, 0))

        if on_config_click:
            btn_config = tk.Button( buttons_frame, text="⚙️ Ajustes", command=on_config_click, bg=button_bg, fg=button_fg, font=("Arial", 9, "bold"), relief="groove", bd=1, padx=10, pady=4, cursor="hand2" ) 
            btn_config.pack(side="left", padx=(8, 0))

        if on_creditos_click:
            btn_creditos = tk.Button( buttons_frame, text="ℹ️ Créditos", command=on_creditos_click, bg=button_bg, fg=button_fg, font=("Arial", 9, "bold"), relief="groove", bd=1, padx=10, pady=4, cursor="hand2" ) 
            btn_creditos.pack(side="left", padx=(8, 0))
            
class StatusBar(tk.Label): 
    """Barra de estado inferior estandarizada.""" 
    
    def __init__(self, parent, text_inicial="Listo", bg_color="#333333", fg_color="#ffffff"): 
        super().__init__( 
            parent, 
            text=text_inicial, 
            font=("Arial", 8, "bold"), 
            bg=bg_color, 
            fg=fg_color, 
            anchor="w", 
            padx=8, 
            pady=3 
        ) 
        self.pack(fill="x", side="bottom") 
        
    def set_mensaje(self, mensaje: str): 
        self.config(text=mensaje) 
        
class PanelBase(tk.LabelFrame): 
    """Contenedor estilo tarjeta con bordes para agrupar herramientas.""" 
    
    def __init__(self, parent, titulo="Panel", bg_color="#ffffff", fg_color="#007acc"): 
        super().__init__( 
            parent, 
            text=titulo, 
            font=("Arial", 9, "bold"), 
            fg=fg_color, 
            bg=bg_color, 
            bd=1, 
            relief="solid", 
            padx=8, 
            pady=8 
        ) 
        
class CardButton(tk.Button): 
    """Botón con formato de tarjeta responsiva para materias y accesos.""" 
    
    def __init__(self, parent, text, command=None, icon="📖", bg="#f8f9fa", fg="#007acc", **kwargs): 
        full_text = f"{icon}\n{text}" if icon else text 

        button_kwargs = {
            "text": full_text,
            "bg": bg,
            "fg": fg,
            "font": ("Arial", 9, "bold"),
            "bd": 1,
            "relief": "solid",
            "padx": 6,
            "pady": 8,
            "wraplength": 160,
            "justify": "center",
            "cursor": "hand2",
            "activebackground": fg,
            "activeforeground": "#ffffff",
        }
        extra_kwargs = dict(kwargs)
        extra_kwargs.pop("parent", None)
        extra_kwargs.pop("activebackground", None)
        extra_kwargs.pop("activeforeground", None)
        button_kwargs.update(extra_kwargs)
        if command is not None:
            button_kwargs["command"] = command

        super().__init__(parent, **button_kwargs)