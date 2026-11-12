import tkinter as tk 
from tkinter import ttk, messagebox 
import sys 
from pathlib import Path 

from configuracion.glosario_central import GlosarioCentralUI

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent 
if str(BASE_DIR) not in sys.path: 
    sys.path.insert(0, str(BASE_DIR)) 

try:
    import importlib
    _config_manager = importlib.import_module("configuracion.config_manager")
    cargar_configuracion = _config_manager.cargar_configuracion
    aplicar_estilos_globales = _config_manager.aplicar_estilos_globales
except ImportError:
    def cargar_configuracion() -> dict[str, object]:
        return {}

    def aplicar_estilos_globales(root, config) -> None:
        return None

try:
    import importlib
    _componentes_ui = importlib.import_module("vistas.componentes_ui")
    PanelBase = _componentes_ui.PanelBase
except ImportError:
    class PanelBase(tk.LabelFrame):
        def __init__(self, parent=None, titulo="Panel", bg_color="#ffffff", fg_color="#007acc"):
            super().__init__(parent, text=titulo, bg=bg_color, fg=fg_color, font=("Arial", 9, "bold"), bd=1, relief="solid", padx=6, pady=6)

try:
    from . import herramientas as _hardware_tools
except ImportError:
    import importlib
    _hardware_tools = importlib.import_module("herramientas")

MATRIZ_FALLAS_HARDWARE = _hardware_tools.MATRIZ_FALLAS_HARDWARE
calcular_consumo_psu = _hardware_tools.calcular_consumo_psu
COMPATIBILIDAD_SOCKETS = _hardware_tools.COMPATIBILIDAD_SOCKETS
verificar_compatibilidad_ensamble = _hardware_tools.verificar_compatibilidad_ensamble
DICCIONARIO_HARDWARE = _hardware_tools.DICCIONARIO_HARDWARE

class ModuloLabsHardwareUI(tk.Frame): 
    def __init__(self, parent=None, contexto: dict | None = None, on_back_callback=None): 
        self.contexto: dict[str, object] = contexto or {}
        self.on_back = on_back_callback 
        self.glosario_ui = None
        config = cargar_configuracion()
        self.config_val: dict[str, object] = config if isinstance(config, dict) else {}
        bg_main = str(self.config_val.get("bg_color", "#ffffff"))
        panel_bg = str(self.config_val.get("panel_bg", "#f8f9fa"))
        fg_main = str(self.config_val.get("fg_color", "#212529"))
        accent = str(self.config_val.get("accent_color", "#007acc"))
        super().__init__(parent, bg=bg_main) 
        self.pack(fill="both", expand=True) 
        self._build_ui(bg_main=bg_main, panel_bg=panel_bg, fg_main=fg_main, accent=accent) 
        aplicar_estilos_globales(self, self.config_val) 
        
    def _build_ui(self, bg_main="#ffffff", panel_bg="#f8f9fa", fg_main="#212529", accent="#007acc"): 
        header_frame = tk.Frame(self, bg=accent, padx=12, pady=8, bd=1, relief="solid") 
        header_frame.pack(fill="x", side="top") 
        
        left_header = tk.Frame(header_frame, bg=accent) 
        left_header.pack(side="left", fill="both", expand=True) 
        
        tk.Label(left_header, text="🖥️ Labs. Hardware - 4.º Año Informática", font=("Arial", 12, "bold"), fg="#ffffff", bg=accent).pack(anchor="w") 
        tk.Label(left_header, text="Arquitectura de Computadoras, Diagnóstico de Fallas, Fuentes de Alimentación y Compatibilidad", font=("Arial", 8), fg="#edf7ff", bg=accent).pack(anchor="w") 
        
        if self.on_back: 
            btn_volver = tk.Button(header_frame, text="⬅️ Volver al Aula", command=self.on_back, bg="#ffffff", fg=accent, font=("Arial", 8, "bold"), relief="groove", padx=8, pady=2, cursor="hand2") 
            btn_volver.pack(side="right") 
            
        style = ttk.Style() 
        style.theme_use("clam") 
        style.configure("Hwd.TNotebook", background=bg_main) 
        style.configure("Hwd.TNotebook.Tab", font=("Arial", 9, "bold"), padding=[10, 4]) 
        
        notebook = ttk.Notebook(self, style="Hwd.TNotebook") 
        notebook.pack(fill="both", expand=True, padx=8, pady=8) 
        
        tab1 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab1, text="🛠️ Diagnóstico & Troubleshooting") 
        self._build_tab_diagnostico(tab1, panel_bg, fg_main, accent) 
        
        tab2 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab2, text="⚡ Calculadora de Fuente PSU") 
        self._build_tab_psu(tab2, panel_bg, fg_main, accent) 
        
        tab3 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab3, text="🧩 Compatibilidad de Ensamble") 
        self._build_tab_compatibilidad(tab3, panel_bg, fg_main, accent) 
        
        tab4 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab4, text="📚 Glosario de Hardware") 
        self._build_tab_glosario(tab4, panel_bg, fg_main, accent) 
        
    def _build_tab_diagnostico(self, parent, panel_bg, fg_main, accent): 
        top_f = tk.Frame(parent, bg=panel_bg, padx=8, pady=4, bd=1, relief="solid") 
        top_f.pack(fill="x", pady=(0, 6)) 
        
        tk.Label(top_f, text="Seleccionar Síntoma o Falla: ", font=("Arial", 9, "bold"), bg=panel_bg).pack(side="left") 
        fallas_lista = list(MATRIZ_FALLAS_HARDWARE.keys()) 
        
        self.cmb_fallas = ttk.Combobox(top_f, values=fallas_lista, state="readonly", width=42) 
        self.cmb_fallas.set(fallas_lista[0]) 
        self.cmb_fallas.pack(side="left", padx=6) 
        self.cmb_fallas.bind("<<ComboboxSelected>>", self._on_select_falla) 
        
        self.pnl_falla = PanelBase(parent, titulo="🛠️ Protocolo Técnico de Resolución paso a paso", bg_color=panel_bg) 
        self.pnl_falla.pack(fill="both", expand=True) 
        
        self.txt_res_falla = tk.Text(self.pnl_falla, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid", wrap="word") 
        self.txt_res_falla.pack(fill="both", expand=True, padx=4, pady=4) 
        self._show_falla_detail(fallas_lista[0]) 
        
    def _on_select_falla(self, event=None): self._show_falla_detail(self.cmb_fallas.get()) 
    
    def _show_falla_detail(self, falla_key): 
        data = MATRIZ_FALLAS_HARDWARE.get(falla_key, {}) 
        self.txt_res_falla.delete("1.0", tk.END) 
        
        if not data: 
            return 
            
        self.txt_res_falla.insert(tk.END, f"🛠️ GUÍA TÉCNICA: {falla_key.upper()}\n\n") 
        self.txt_res_falla.insert(tk.END, f"⚠️ Síntoma Reportado: {data['sintoma']}\n\n🔍 Causas Probables:\n") 
        
        for causa in data["causas_probables"]: self.txt_res_falla.insert(tk.END, f" • {causa}\n") 
        self.txt_res_falla.insert(tk.END, "\n📋 Protocolo de Solución Recomendado:\n") 
        for paso in data["solucion_paso_a_paso"]: self.txt_res_falla.insert(tk.END, f" {paso}\n") 
        
    def _build_tab_psu(self, parent, panel_bg, fg_main, accent): 
        pnl = PanelBase(parent, titulo="⚡ Estimador de Wattage Requerido para la Fuente de Alimentación", bg_color=panel_bg) 
        pnl.pack(fill="x", pady=(0, 6)) 
        f_in = tk.Frame(pnl, bg=panel_bg); f_in.pack(fill="x", pady=2) 
        tk.Label(f_in, text="CPU TDP (Watts): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=0) 
        
        self.e_cpu_w = tk.Entry(f_in, width=8, justify="center"); self.e_cpu_w.grid(row=0, column=1); self.e_cpu_w.insert(0, "125") 
        tk.Label(f_in, text="GPU TDP (Watts): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=2) 
        self.e_gpu_w = tk.Entry(f_in, width=8, justify="center"); self.e_gpu_w.grid(row=0, column=3); self.e_gpu_w.insert(0, "220") 
        
        btn_psu = tk.Button(pnl, text="⚡ Calcular Consumo y Fuente Recomendada", command=self._calc_psu, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove") 
        btn_psu.pack(fill="x", pady=4) 
        
        self.txt_res_psu = tk.Text(parent, height=10, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid", wrap="word") 
        self.txt_res_psu.pack(fill="both", expand=True) 
        
    def _calc_psu(self): 
        self.txt_res_psu.delete("1.0", tk.END) 
        try: 
            res = calcular_consumo_psu(float(self.e_cpu_w.get()), float(self.e_gpu_w.get())) 
            self.txt_res_psu.insert(tk.END, f"⚡ CONSUMO ESTIMADO: {res['consumo_estimado_watts']} W\n💡 FUENTE RECOMENDADA: {res['psu_recomendada_watts']} W ({res['certificacion_sugerida']})\n") 
        except Exception: 
            messagebox.showerror("Error", "Datos inválidos.") 
            
    def _build_tab_compatibilidad(self, parent, panel_bg, fg_main, accent): 
        pnl = PanelBase(parent, titulo="🧩 Chequeador de Compatibilidad Motherboard / Socket / RAM", bg_color=panel_bg) 
        pnl.pack(fill="x", pady=(0, 6)) 
        f_c = tk.Frame(pnl, bg=panel_bg); f_c.pack(fill="x", pady=2) 
        
        tk.Label(f_c, text="Socket: ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=0) 
        self.cmb_socket = ttk.Combobox(f_c, values=list(COMPATIBILIDAD_SOCKETS.keys()), state="readonly", width=12); self.cmb_socket.set("AM4"); self.cmb_socket.grid(row=0, column=1) 
        
        tk.Label(f_c, text="RAM: ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=2) 
        self.cmb_ram = ttk.Combobox(f_c, values=["DDR4", "DDR5"], state="readonly", width=10); self.cmb_ram.set("DDR4"); self.cmb_ram.grid(row=0, column=3) 
        btn_c = tk.Button(pnl, text="🧩 Verificar Compatibilidad", command=self._calc_comp, bg="#28a745", fg="#ffffff", font=("Arial", 8, "bold")) 
        btn_c.pack(fill="x", pady=4) 
        self.txt_res_comp = tk.Text(parent, height=8, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid", wrap="word") 
        self.txt_res_comp.pack(fill="both", expand=True) 
        
    def _calc_comp(self): 
        self.txt_res_comp.delete("1.0", tk.END) 
        res = verificar_compatibilidad_ensamble(self.cmb_socket.get(), self.cmb_ram.get()) 
        self.txt_res_comp.insert(tk.END, f"🧩 DICTAMEN: {res['dictamen']}\nCPUs Soportadas: {', '.join(res['cpus_soportadas'])}\n") 
        
    def _build_tab_glosario(self, parent, panel_bg, fg_main, accent):
        self.glosario_ui = GlosarioCentralUI(
            parent,
            titulo="📚 Glosario de Arquitectura",
            data_path=Path(__file__).resolve().parents[4] / "persistance" / "glosario_hardware.json",
        )
        self.glosario_ui.entries = [
            {
                "nombre": term,
                "categorias": ["Hardware", "Informática"],
                "subcategorias": ["Concepto"],
                "contenido": defn,
            }
            for term, defn in DICCIONARIO_HARDWARE.items()
        ] + list(getattr(self.glosario_ui, "entries", []))
        if hasattr(self.glosario_ui, "_aplicar_filtro"):
            self.glosario_ui._aplicar_filtro()