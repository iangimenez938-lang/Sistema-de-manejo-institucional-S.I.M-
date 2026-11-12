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
from .herramientas import (
    calcular_permisos_posix,
    COMANDOS_SISTEMA_DICCIONARIO,
    simular_planificacion_cpu,
    diagnosticar_recursos_sistema,
    DICCIONARIO_SISTEMAS,
)

class ModuloLabsSistemasUI(tk.Frame):
    def __init__(self, parent=None, contexto: dict[str, object] | None = None, on_back_callback=None):
        self.contexto: dict[str, object] = contexto or {}
        self.on_back = on_back_callback
        self.glosario_ui = None
        self.config_val = cargar_configuracion()
        bg_main = self.config_val.get("bg_color", "#ffffff")
        panel_bg = self.config_val.get("panel_bg", "#f8f9fa")
        accent = self.config_val.get("accent_color", "#007acc")
        super().__init__(parent, bg=bg_main)
        self.pack(fill="both", expand=True)
        self._build_ui(bg_main, panel_bg, accent)
        aplicar_estilos_globales(self, self.config_val)
        
    def _build_ui(self, bg_main, panel_bg, accent): 
        header = tk.Frame(self, bg=accent, padx=12, pady=8, bd=1, relief="solid"); header.pack(fill="x", side="top") 
        
        tk.Label(header, text="🛠️ Labs. Sistemas - 4.º Año Informática", font=("Arial", 12, "bold"), fg="#ffffff", bg=accent).pack(anchor="w") 
        
        if self.on_back: tk.Button(header, text="⬅️ Volver", command=self.on_back, bg="#ffffff", fg=accent, font=("Arial", 8, "bold")).pack(side="right") 
            
        notebook = ttk.Notebook(self); notebook.pack(fill="both", expand=True, padx=8, pady=8) 
        
        tab1 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8); notebook.add(tab1, text="🔑 Permisos POSIX (chmod)") 
        self._build_tab_posix(tab1, panel_bg, accent) 
        
        tab2 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8); notebook.add(tab2, text="💻 Comandos CLI") 
        self._build_tab_cli(tab2, panel_bg) 
        
        tab3 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8); notebook.add(tab3, text="⚙️ Planificador CPU") 
        self._build_tab_cpu(tab3, panel_bg, accent) 

        tab4 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8); notebook.add(tab4, text="📊 Diagnóstico del Sistema") 
        self._build_tab_diagnostico(tab4, panel_bg, accent) 

        tab5 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8); notebook.add(tab5, text="📚 Glosario") 
        self._build_tab_glosario(tab5, panel_bg, accent) 
        
    def _build_tab_posix(self, parent, panel_bg, accent): 
        pnl = PanelBase(parent, titulo="🔑 Calculadora de Permisos POSIX", bg_color=panel_bg); pnl.pack(fill="x", pady=(0, 6)) 
        f = tk.Frame(pnl, bg=panel_bg); f.pack(fill="x", pady=2) 
        tk.Label(f, text="Permiso Octal (ej 755): ", font=("Arial", 8, "bold"), bg=panel_bg).pack(side="left") 
        
        self.e_oct = tk.Entry(f, width=8, justify="center"); self.e_oct.pack(side="left", padx=4); self.e_oct.insert(0, "755") 
        btn = tk.Button(pnl, text="🔑 Analizar Permisos", command=self._calc_posix, bg=accent, fg="#ffffff", font=("Arial", 8, "bold")) 
        btn.pack(fill="x", pady=4) 
        self.txt_pos = tk.Text(parent, height=8, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid", wrap="word"); self.txt_pos.pack(fill="both", expand=True) 
        
    def _calc_posix(self): 
        self.txt_pos.delete("1.0", tk.END) 
        res = calcular_permisos_posix(self.e_oct.get().strip()) 
        self.txt_pos.insert(tk.END, f"🔑 NOTACIÓN SIMBÓLICA: {res['notacion_simbolica']}\n• {res['owner']}\n• {res['group']}\n• {res['others']}\n") 
        
    def _build_tab_cli(self, parent, panel_bg): 
        pnl = PanelBase(parent, titulo="💻 Diccionario de Comandos Linux / Bash", bg_color=panel_bg); pnl.pack(fill="both", expand=True) 
        txt = tk.Text(pnl, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid", wrap="word"); txt.pack(fill="both", expand=True, padx=2, pady=2) 
        
        for cmd, info in COMANDOS_SISTEMA_DICCIONARIO.items(): 
            txt.insert(tk.END, f"📌 {cmd} ({info['categoria']}):\n Efecto: {info['efecto']}\n Ejemplo: {info['ejemplo']}\n\n") 
            
    def _build_tab_cpu(self, parent, panel_bg, accent): 
        pnl = PanelBase(parent, titulo="⚙️ Simulador de Planificación FIFO de CPU", bg_color=panel_bg); pnl.pack(fill="x", pady=(0, 6)) 
        btn = tk.Button(pnl, text="⚙️ Ejecutar Simulación FIFO", command=self._sim_cpu, bg="#28a745", fg="#ffffff", font=("Arial", 8, "bold")) 
        btn.pack(fill="x", pady=4) 
        self.txt_cpu = tk.Text(parent, height=8, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid", wrap="word"); self.txt_cpu.pack(fill="both", expand=True) 
        
    def _sim_cpu(self):
        self.txt_cpu.delete("1.0", tk.END)
        procs = [{"pid": "P1", "rafaga": 6}, {"pid": "P2", "rafaga": 3}, {"pid": "P3", "rafaga": 8}]
        res = simular_planificacion_cpu(procs)
        self.txt_cpu.insert(tk.END, f"⚙️ SECUENCIA DE EJECUCIÓN (Tiempo Total: {res['tiempo_total_ms']} ms):\n\n")
        for paso in res["secuencia_ejecucion"]:
            if not isinstance(paso, dict):
                continue
            pid = paso.get("pid", "N/A")
            inicio = paso.get("inicio", 0)
            fin = paso.get("fin", 0)
            espera = paso.get("espera", 0)
            self.txt_cpu.insert(
                tk.END,
                f" ► Proceso {pid}: Inicio {inicio}ms -> Fin {fin}ms (Espera: {espera}ms)\n",
            )

    def _build_tab_diagnostico(self, parent, panel_bg, accent):
        pnl = PanelBase(parent, titulo="📊 Diagnóstico de uso del sistema", bg_color=panel_bg)
        pnl.pack(fill="x", pady=(0, 6))

        f = tk.Frame(pnl, bg=panel_bg)
        f.pack(fill="x", pady=2)

        tk.Label(f, text="CPU (%): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=0, sticky="w")
        self.e_cpu = tk.Entry(f, width=8, justify="center"); self.e_cpu.grid(row=0, column=1, padx=4)
        self.e_cpu.insert(0, "58")

        tk.Label(f, text="Memoria (%): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=2, sticky="w")
        self.e_mem = tk.Entry(f, width=8, justify="center"); self.e_mem.grid(row=0, column=3, padx=4)
        self.e_mem.insert(0, "67")

        tk.Label(f, text="Disco (%): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=1, column=0, sticky="w", pady=4)
        self.e_disc = tk.Entry(f, width=8, justify="center"); self.e_disc.grid(row=1, column=1, padx=4, pady=4)
        self.e_disc.insert(0, "74")

        tk.Label(f, text="Red: ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=1, column=2, sticky="w", pady=4)
        self.cmb_red = ttk.Combobox(f, values=["normal", "lento", "caido"], state="readonly", width=12)
        self.cmb_red.set("normal")
        self.cmb_red.grid(row=1, column=3, padx=4, pady=4)

        btn = tk.Button(pnl, text="📊 Evaluar Estado del Sistema", command=self._eval_diagnostico, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"))
        btn.pack(fill="x", pady=4)

        self.txt_diag = tk.Text(parent, height=9, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_diag.pack(fill="both", expand=True)

    def _eval_diagnostico(self):
        self.txt_diag.delete("1.0", tk.END)
        try:
            cpu = float(self.e_cpu.get())
            mem = float(self.e_mem.get())
            disco = float(self.e_disc.get())
            red = self.cmb_red.get()
            res = diagnosticar_recursos_sistema(cpu, mem, disco, red)
            if "error" in res:
                self.txt_diag.insert(tk.END, f"⚠️ {res['error']}\n")
                return
            self.txt_diag.insert(tk.END, "📊 DIAGNÓSTICO GENERAL DEL SISTEMA\n\n")
            self.txt_diag.insert(tk.END, f"• Estado general: {res['estado_general']}\n")
            self.txt_diag.insert(tk.END, f"• Promedio de uso: {res['score_promedio']}%\n")
            self.txt_diag.insert(tk.END, f"• CPU: {res['cpu_percent']}% | Memoria: {res['memoria_percent']}% | Disco: {res['disco_percent']}%\n")
            self.txt_diag.insert(tk.END, f"• Red: {res['red_estado']}\n\n")
            self.txt_diag.insert(tk.END, f"💡 Recomendación: {res['recomendacion']}\n")
        except Exception:
            messagebox.showerror("Error", "Ingresá valores numéricos válidos.")

    def _build_tab_glosario(self, parent, panel_bg, accent):
        self.glosario_ui = GlosarioCentralUI(
            parent,
            titulo="📚 Glosario de Sistemas Operativos",
            data_path=Path(__file__).resolve().parents[4] / "persistance" / "glosario_sistemas.json",
        )
        self.glosario_ui.entries = [
            {
                "nombre": term,
                "categorias": ["Sistemas", "Informática"],
                "subcategorias": ["Concepto clave"],
                "contenido": defn,
            }
            for term, defn in DICCIONARIO_SISTEMAS.items()
        ] + list(getattr(self.glosario_ui, "entries", []))
        if hasattr(self.glosario_ui, "_aplicar_filtro"):
            self.glosario_ui._aplicar_filtro()