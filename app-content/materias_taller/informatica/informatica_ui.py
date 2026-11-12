import importlib
import tkinter as tk

try:
    from configuracion.config_manager import cargar_configuracion, aplicar_estilos_globales
    from vistas.componentes_ui import CardButton, PanelBase
except ImportError:  # pragma: no cover
    def cargar_configuracion():
        return {}

    def aplicar_estilos_globales(widget, config):
        return None

    class PanelBase(tk.LabelFrame):
        def __init__(self, parent=None, titulo="Panel", bg_color="#ffffff", fg_color="#007acc"):
            super().__init__(parent, text=titulo, bg=bg_color, fg=fg_color, font=("Arial", 9, "bold"), bd=1, relief="solid", padx=8, pady=8)

    class CardButton(tk.Button):
        def __init__(self, parent, text, command=None, icon="📖", bg="#f8f9fa", fg="#007acc", **kwargs):
            full_text = f"{icon}\n{text}" if icon else text
            super().__init__(parent, text=full_text, command=command, bg=bg, fg=fg, font=("Arial", 9, "bold"), bd=1, relief="solid", padx=6, pady=8, wraplength=160, justify="center", cursor="hand2", activebackground=fg, activeforeground="#ffffff", **kwargs)

LABORATORIOS = [
    {"key": "labs_programacion", "nombre": "Labs. Programación", "icon": "💻"},
    {"key": "labs_hardware", "nombre": "Labs. Hardware", "icon": "🖥️"},
    {"key": "labs_aplicaciones", "nombre": "Labs. Aplicaciones", "icon": "📱"},
    {"key": "labs_sistemas", "nombre": "Labs. Sistemas", "icon": "🛠️"},
]


class ModuloInformaticaUI(tk.Frame):
    """Pantalla central para acceder a los laboratorios de Informática."""

    def __init__(self, parent=None, contexto: dict | None = None, on_back_callback=None):
        super().__init__(parent, bg="#ffffff")
        self.contexto = contexto or {}
        self.on_back = on_back_callback
        self.config_val = cargar_configuracion()
        bg_main = self.config_val.get("bg_color", "#ffffff")
        panel_bg = self.config_val.get("panel_bg", "#f8f9fa")
        fg_main = self.config_val.get("fg_color", "#212529")
        accent = self.config_val.get("accent_color", "#007acc")
        self.configure(bg=bg_main)
        self.pack(fill="both", expand=True)
        self._build_ui(bg_main=bg_main, panel_bg=panel_bg, fg_main=fg_main, accent=accent)
        aplicar_estilos_globales(self, self.config_val)

    def _volver_a_clase(self):
        if self.on_back:
            self.on_back()
            return
        self._volver_a_informatica()

    def _build_ui(self, bg_main="#ffffff", panel_bg="#f8f9fa", fg_main="#212529", accent="#007acc"):
        header_frame = tk.Frame(self, bg=accent, padx=12, pady=8, bd=1, relief="solid")
        header_frame.pack(fill="x", side="top")

        left_header = tk.Frame(header_frame, bg=accent)
        left_header.pack(side="left", fill="both", expand=True)

        tk.Label(left_header, text="💻 Módulo de Informática - 4.º Año", font=("Arial", 12, "bold"), fg="#ffffff", bg=accent).pack(anchor="w")
        tk.Label(left_header, text="Laboratorios de programación, hardware, aplicaciones y sistemas", font=("Arial", 8), fg="#edf7ff", bg=accent).pack(anchor="w")

        if self.on_back:
            btn_volver = tk.Button(header_frame, text="🏫 Volver a la clase", command=self._volver_a_clase, bg="#ffffff", fg=accent, font=("Arial", 8, "bold"), relief="groove", padx=8, pady=2, cursor="hand2")
            btn_volver.pack(side="right")

        panel = PanelBase(self, titulo="🧪 Seleccioná un laboratorio", bg_color=panel_bg)
        panel.pack(fill="both", expand=True, padx=8, pady=8)

        frame_cards = tk.Frame(panel, bg=panel_bg)
        frame_cards.pack(fill="both", expand=True)

        for idx, item in enumerate(LABORATORIOS):
            btn = CardButton(
                frame_cards,
                text=item["nombre"],
                command=lambda key=item["key"]: self._abrir_lab(key),
                icon=item["icon"],
                bg=panel_bg,
                fg=accent,
            )
            btn.grid(row=idx // 2, column=idx % 2, padx=8, pady=8, sticky="nsew")

        for column in range(2):
            frame_cards.columnconfigure(column, weight=1)

    def _abrir_lab(self, lab_key: str):
        for widget in self.winfo_children():
            widget.destroy()

        try:
            modulo = importlib.import_module(f"materias_taller.informatica.{lab_key}")
        except ModuleNotFoundError:
            tk.messagebox.showerror("Error", f"No se pudo abrir el laboratorio '{lab_key}'.")
            self._volver_a_informatica()
            return

        if hasattr(modulo, "build_ui"):
            modulo.build_ui(
                self,
                contexto={**self.contexto, "materia": lab_key, "modulo_central": lab_key},
                on_back_callback=self._volver_a_clase,
            )
            return

        tk.messagebox.showerror("Error", f"El laboratorio '{lab_key}' no tiene una vista compatible.")
        self._volver_a_informatica()

    def _volver_a_informatica(self):
        for widget in self.winfo_children():
            widget.destroy()
        self._build_ui(
            bg_main=self.config_val.get("bg_color", "#ffffff"),
            panel_bg=self.config_val.get("panel_bg", "#f8f9fa"),
            fg_main=self.config_val.get("fg_color", "#212529"),
            accent=self.config_val.get("accent_color", "#007acc"),
        )
