import tkinter as tk 
from tkinter import ttk, messagebox 
import sys 
from pathlib import Path 

from configuracion.glosario_central import GlosarioCentralUI

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent 
if str(BASE_DIR) not in sys.path: 
    sys.path.insert(0, str(BASE_DIR)) 
    
from configuracion.config_manager import cargar_configuracion, aplicar_estilos_globales 
from vistas.componentes_ui import PanelBase 
from .herramientas import ejecutar_consulta_sql_simulada, PLANTILLAS_COMPONENTES_WEB, DICCIONARIO_APLICACIONES, generar_plantilla_aplicacion 

class ModuloLabsAplicacionesUI(tk.Frame): 
    def __init__(self, parent=None, contexto: dict = None, on_back_callback=None): 
        self.contexto = contexto or {}; self.on_back = on_back_callback 
        self.glosario_ui = None
        self.config_val = cargar_configuracion() 
        bg_main = self.config_val.get("bg_color", "#ffffff"); panel_bg = self.config_val.get("panel_bg", "#f8f9fa"); accent = self.config_val.get("accent_color", "#007acc") 
        super().__init__(parent, bg=bg_main); self.pack(fill="both", expand=True) 
        self._build_ui(bg_main, panel_bg, accent) 
        aplicar_estilos_globales(self, self.config_val) 
        
    def _build_ui(self, bg_main, panel_bg, accent): 
        header = tk.Frame(self, bg=accent, padx=12, pady=8, bd=1, relief="solid"); header.pack(fill="x", side="top") 
        tk.Label(header, text="📱 Labs. Aplicaciones - 4.º Año Informática", font=("Arial", 12, "bold"), fg="#ffffff", bg=accent).pack(anchor="w") 
        
        if self.on_back: 
            tk.Button(header, text="⬅️ Volver", command=self.on_back, bg="#ffffff", fg=accent, font=("Arial", 8, "bold")).pack(side="right") 
            
        notebook = ttk.Notebook(self); notebook.pack(fill="both", expand=True, padx=8, pady=8) 
        tab1 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8); notebook.add(tab1, text="🗄️ Consola SQL &amp; SQLite") 
        
        self._build_tab_sql(tab1, panel_bg, accent) 
        tab2 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8); notebook.add(tab2, text="🌐 Maquetado HTML/CSS") 
        
        self._build_tab_web(tab2, panel_bg) 
        tab3 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8); notebook.add(tab3, text="📚 Glosario Apps") 
        
        self._build_tab_glosario(tab3, panel_bg) 
        
    def _build_tab_sql(self, parent, panel_bg, accent): 
        pnl = PanelBase(parent, titulo="🗄️ Consola de Consultas SQL (SQLite)", bg_color=panel_bg); pnl.pack(fill="x", pady=(0, 6)) 
        self.e_sql = tk.Entry(pnl, width=60); self.e_sql.pack(fill="x", pady=4); self.e_sql.insert(0, "SELECT * FROM estudiantes WHERE promedio >= 8.5") 
        btn = tk.Button(pnl, text="⚡ Ejecutar Consulta SQL", command=self._run_sql, bg=accent, fg="#ffffff", font=("Arial", 8, "bold")) 
        btn.pack(fill="x", pady=2) 
        
        self.txt_sql = tk.Text(parent, height=8, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid", wrap="word"); self.txt_sql.pack(fill="both", expand=True) 
        
    def _run_sql(self): 
        self.txt_sql.delete("1.0", tk.END) 
        res = ejecutar_consulta_sql_simulada(self.e_sql.get().strip()) 
        
        if "error" in res: 
            self.txt_sql.insert(tk.END, f"⚠️ {res['error']}\n"); return self.txt_sql.insert(tk.END, f"🗄️ RESULTADO SQL ({res['total_registros']} filas):\nColumnas: {', '.join(res['columnas'])}\n\n") 
        
        for fila in res["filas"]: 
            self.txt_sql.insert(tk.END, f" ► {fila}\n") 
            
    def _build_tab_web(self, parent, panel_bg): 
        pnl = PanelBase(parent, titulo="🌐 Generador de componentes HTML5 & CSS3", bg_color=panel_bg); pnl.pack(fill="both", expand=True)

        top = tk.Frame(pnl, bg=panel_bg)
        top.pack(fill="x", pady=(0, 6))
        tk.Label(top, text="Componente:", font=("Arial", 8, "bold"), bg=panel_bg).pack(side="left")
        self.cmb_componentes = ttk.Combobox(top, values=list(PLANTILLAS_COMPONENTES_WEB.keys()), state="readonly", width=24)
        self.cmb_componentes.set("Formulario de Login")
        self.cmb_componentes.pack(side="left", padx=6)

        tk.Button(top, text="🧩 Generar vista", command=self._generar_componente_web).pack(side="left", padx=6)

        self.txt_web = tk.Text(pnl, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_web.pack(fill="both", expand=True, padx=2, pady=2)
        self._generar_componente_web()

    def _generar_componente_web(self):
        nombre = self.cmb_componentes.get()
        data = generar_plantilla_aplicacion(nombre)
        self.txt_web.delete("1.0", tk.END)
        if "error" in data:
            self.txt_web.insert(tk.END, f"⚠️ {data['error']}\n")
            return
        self.txt_web.insert(tk.END, f"🌐 COMPONENTE: {data['nombre']}\n\n[HTML]:\n{data['html']}\n\n[CSS]:\n{data['css']}\n")
            
    def _build_tab_glosario(self, parent, panel_bg): 
        self.glosario_ui = GlosarioCentralUI(
            parent,
            titulo="📚 Glosario Web & BDD",
            data_path=Path(__file__).resolve().parents[4] / "persistance" / "glosario_aplicaciones.json",
        )
        self.glosario_ui.entries = [
            {
                "nombre": term,
                "categorias": ["Aplicaciones", "Web"],
                "subcategorias": ["Concepto"],
                "contenido": defn,
            }
            for term, defn in DICCIONARIO_APLICACIONES.items()
        ] + list(getattr(self.glosario_ui, "entries", []))
        if hasattr(self.glosario_ui, "_aplicar_filtro"):
            self.glosario_ui._aplicar_filtro()