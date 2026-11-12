import tkinter as tk 
from tkinter import ttk, messagebox 
import sys 
from pathlib import Path 
from typing import Any

from configuracion.glosario_central import GlosarioCentralUI

BASE_DIR = Path(__file__).resolve().parent.parent.parent 
if str(BASE_DIR) not in sys.path: 
    sys.path.insert(0, str(BASE_DIR)) 


def cargar_configuracion() -> dict[str, Any]:
    try:
        from configuracion.config_manager import cargar_configuracion as _cargar_configuracion
        config = _cargar_configuracion()
        return config if isinstance(config, dict) else {}
    except Exception:
        return {}


def aplicar_estilos_globales(root, config) -> None:
    try:
        from configuracion.config_manager import aplicar_estilos_globales as _aplicar_estilos_globales
        _aplicar_estilos_globales(root, config)
    except Exception:
        return None


class PanelBase(tk.LabelFrame):
    """Contenedor reutilizable para los paneles del módulo."""
    def __init__(self, parent=None, titulo="Panel", bg_color="#ffffff", fg_color="#007acc"):
        super().__init__(parent, text=titulo, bg=bg_color, fg=fg_color, font=("Arial", 9, "bold"), bd=1, relief="solid", padx=6, pady=6)

HAS_TKINTER = True

from .herramientas import ( calcular_imc_y_composicion, calcular_frecuencia_cardiaca_zonas, evaluar_test_ruffier, calcular_metabolismo_y_calorias, REGLAMENTO_DEPORTES, DICCIONARIO_ED_FISICA ) 

class ModuloEdFisicaUI(tk.Frame): 
    """ Vista interactiva para el Módulo de Educación Física y Salud de 4.º Año Informática. Contiene 4 pestañas: Evaluación Físico-Cardíaca, Nutrición & Calorías, Reglamentos Deportivos y Glosario. """ 
    def __init__(self, parent=None, contexto: dict[str, Any] | None = None, on_back_callback=None): 
        self.contexto: dict[str, Any] = contexto or {}
        self.on_back = on_back_callback 
        self.glosario_ui = None
        config = cargar_configuracion()
        self.config_val: dict[str, Any] = config if isinstance(config, dict) else {}
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
        
        tk.Label( left_header, text="🏀 Módulo de Educación Física & Salud - 4.º Año Informática", font=("Arial", 12, "bold"), fg="#ffffff", bg=accent ).pack(anchor="w") 
        tk.Label( left_header, text="Evaluación Físico-Cardíaca, IMC, Zonas de Entrenamiento, Nutrición y Reglamentos Deportivos", font=("Arial", 8), fg="#edf7ff", bg=accent ).pack(anchor="w") 
        
        if self.on_back: 
            btn_volver = tk.Button( header_frame, text="⬅️ Volver al Aula", command=self.on_back, bg="#ffffff", fg=accent, font=("Arial", 8, "bold"), relief="groove", padx=8, pady=2, cursor="hand2" ) 
            btn_volver.pack(side="right") 
            
        style = ttk.Style() 
        style.theme_use("clam") 
        style.configure("EdF.TNotebook", background=bg_main) 
        style.configure("EdF.TNotebook.Tab", font=("Arial", 9, "bold"), padding=[10, 4]) 
        
        notebook = ttk.Notebook(self, style="EdF.TNotebook") 
        notebook.pack(fill="both", expand=True, padx=8, pady=8) 
        
        # Tab 1: Evaluación Físico-Cardíaca 
        tab1 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab1, text="🏃 Evaluación Físico-Cardíaca") 
        self._build_tab_evaluacion(tab1, panel_bg, fg_main, accent) 
        # Tab 2: Nutrición & Calorías 
        tab2 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab2, text="🥗 Nutrición & Calorías") 
        self._build_tab_nutricion(tab2, panel_bg, fg_main, accent) 
        # Tab 3: Reglamentos Deportivos 
        tab3 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab3, text="🏀 Reglamentos Deportivos") 
        self._build_tab_reglamentos(tab3, panel_bg, fg_main, accent) 
        # Tab 4: Glosario 
        tab4 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab4, text="📚 Glosario de Salud") 
        self._build_tab_glosario(tab4, panel_bg, fg_main, accent) 
        
    # --- TAB 1: EVALUACIÓN FÍSICO-CARDÍACA --- 
    def _build_tab_evaluacion(self, parent, panel_bg, fg_main, accent): 
        pnl_imc = PanelBase(parent, titulo="🏃 Calculadora de IMC y Zonas Cardíacas (Karvonen)", bg_color=panel_bg) 
        pnl_imc.pack(fill="x", pady=(0, 6)) 
        
        f_in = tk.Frame(pnl_imc, bg=panel_bg) 
        f_in.pack(fill="x", pady=2) 
        
        tk.Label(f_in, text="Peso (kg): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=0) 
        self.e_peso = tk.Entry(f_in, width=8, justify="center"); self.e_peso.grid(row=0, column=1); self.e_peso.insert(0, "68") 
        
        tk.Label(f_in, text="Altura (m): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=2) 
        self.e_alt = tk.Entry(f_in, width=8, justify="center"); self.e_alt.grid(row=0, column=3); self.e_alt.insert(0, "1.72") 
        
        tk.Label(f_in, text="Edad (años): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=4) 
        self.e_edad = tk.Entry(f_in, width=6, justify="center"); self.e_edad.grid(row=0, column=5); self.e_edad.insert(0, "16") 
        
        btn_imc = tk.Button( pnl_imc, text="🏃 Evaluar IMC y Zonas Cardíacas de Entrenamiento", command=self._calc_evaluacion, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove", cursor="hand2" ) 
        btn_imc.pack(fill="x", pady=4) 
        
        pnl_ruf = PanelBase(parent, titulo="🫀 Evaluación de Test de Ruffier-Dickson (Resistencia Cardíaca)", bg_color=panel_bg) 
        pnl_ruf.pack(fill="x", pady=(0, 6)) 
        
        f_r = tk.Frame(pnl_ruf, bg=panel_bg) 
        f_r.pack(fill="x", pady=2) 
        
        tk.Label(f_r, text="P0 Reposo (PPM): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=0) 
        self.e_p0 = tk.Entry(f_r, width=6, justify="center"); self.e_p0.grid(row=0, column=1); self.e_p0.insert(0, "70") 
        
        tk.Label(f_r, text="P1 Post-40 Sentadillas: ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=2) 
        self.e_p1 = tk.Entry(f_r, width=6, justify="center"); self.e_p1.grid(row=0, column=3); self.e_p1.insert(0, "115") 
        
        tk.Label(f_r, text="P2 Recuperación (1 min): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=4) 
        self.e_p2 = tk.Entry(f_r, width=6, justify="center"); self.e_p2.grid(row=0, column=5); self.e_p2.insert(0, "80") 
        
        btn_ruf = tk.Button( pnl_ruf, text="🫀 Evaluar Test de Ruffier", command=self._calc_ruffier, bg="#28a745", fg="#ffffff", font=("Arial", 8, "bold"), relief="groove" ) 
        btn_ruf.pack(fill="x", pady=4) 
        
        self.txt_res_eval = tk.Text(parent, height=8, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid", wrap="word") 
        self.txt_res_eval.pack(fill="both", expand=True) 
    
    def _calc_evaluacion(self): 
        self.txt_res_eval.delete("1.0", tk.END) 
        try: 
            p = float(self.e_peso.get()) 
            a = float(self.e_alt.get()) 
            e = int(self.e_edad.get()) 
            res_imc = calcular_imc_y_composicion(p, a)
            res_fc = calcular_frecuencia_cardiaca_zonas(e)

            if not isinstance(res_imc, dict) or "error" in res_imc:
                mensaje = res_imc.get("error", "Error en el cálculo de IMC.") if isinstance(res_imc, dict) else "Error en el cálculo de IMC."
                self.txt_res_eval.insert(tk.END, f"⚠️ {mensaje}\n")
                return
            if not isinstance(res_fc, dict) or "error" in res_fc:
                mensaje = res_fc.get("error", "Error en la frecuencia cardíaca.") if isinstance(res_fc, dict) else "Error en la frecuencia cardíaca."
                self.txt_res_eval.insert(tk.END, f"⚠️ {mensaje}\n")
                return

            self.txt_res_eval.insert(tk.END, "🏃 RESULTADOS DE EVALUACIÓN FÍSICA Y CARDÍACA:\n\n")
            self.txt_res_eval.insert(tk.END, f"• Índice de Masa Corporal (IMC): {res_imc['imc']} kg/m² ({res_imc['categoria']})\n")
            self.txt_res_eval.insert(tk.END, f" └─ Recomendación: {res_imc['recomendacion']}\n\n")
            self.txt_res_eval.insert(tk.END, f"• Frecuencia Cardíaca Máxima Teórica (FCM): {res_fc['fc_maxima_fcm']} PPM\n")
            self.txt_res_eval.insert(tk.END, "📊 Zonas de Entrenamiento Karvonen:\n")
            zonas = res_fc.get("zonas_entrenamiento", {})
            if isinstance(zonas, dict):
                for zona, rango in list(zonas.items()):
                    self.txt_res_eval.insert(tk.END, f" • {zona}: {rango}\n")
        except Exception: 
            messagebox.showerror("Error", "Ingresa números válidos.")
    
    def _calc_ruffier(self): 
        self.txt_res_eval.delete("1.0", tk.END) 
        
        try: 
            p0 = int(self.e_p0.get()) 
            p1 = int(self.e_p1.get()) 
            p2 = int(self.e_p2.get()) 
            res = evaluar_test_ruffier(p0, p1, p2) 
            
            self.txt_res_eval.insert(tk.END, "🫀 EVALUACIÓN DEL TEST DE RUFFIER-DICKSON:\n\n") 
            self.txt_res_eval.insert(tk.END, f"• ÍNDICE RUFFIER: {res['indice_ruffier']}\n") 
            self.txt_res_eval.insert(tk.END, f"• Condición Cardíaca Evaluada: {res['evaluacion']}\n") 
            self.txt_res_eval.insert(tk.END, f"• Registro Pulso: Reposo={p0} PPM | Post-Esfuerzo={p1} PPM | Recuperación={p2} PPM\n") 
        except Exception: 
            messagebox.showerror("Error", "Ingresa valores numéricos de pulso válidos.") 

    # --- TAB 2: NUTRICIÓN & CALORÍAS --- 
    def _build_tab_nutricion(self, parent, panel_bg, fg_main, accent): 
        pnl_n = PanelBase(parent, titulo="🥗 Calculadora de Metabolismo Basal y Necesidades Calóricas", bg_color=panel_bg) 
        pnl_n.pack(fill="x", pady=(0, 6)) 
        
        f_n = tk.Frame(pnl_n, bg=panel_bg) 
        f_n.pack(fill="x", pady=2) 
        tk.Label(f_n, text="Nivel Actividad: ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=0) 
        
        self.cmb_act = ttk.Combobox(f_n, values=["sedentario", "ligero", "moderado", "intenso", "atleta"], state="readonly", width=12) 
        self.cmb_act.set("moderado") 
        self.cmb_act.grid(row=0, column=1, padx=4) 
        
        btn_nut = tk.Button( pnl_n, text="🥗 Calcular Gasto Calórico e Hidratación Recomendada", command=self._calc_nutricion, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove", cursor="hand2" ) 
        btn_nut.pack(fill="x", pady=4) 
        
        self.txt_res_nut = tk.Text(parent, height=10, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid", wrap="word") 
        self.txt_res_nut.pack(fill="both", expand=True) 
    
    def _calc_nutricion(self): 
        self.txt_res_nut.delete("1.0", tk.END) 
        try: 
            p = float(self.e_peso.get() if hasattr(self, 'e_peso') else 68) 
            a_cm = float(self.e_alt.get() if hasattr(self, 'e_alt') else 1.72) * 100 
            e = int(self.e_edad.get() if hasattr(self, 'e_edad') else 16) 
            act = self.cmb_act.get() 
            res = calcular_metabolismo_y_calorias(p, a_cm, e, nivel_actividad=act) 
            
            self.txt_res_nut.insert(tk.END, "🥗 REQUERIMIENTO CALÓRICO Y NUTRICIONAL DIARIO:\n\n") 
            self.txt_res_nut.insert(tk.END, f"• Tasa Metabólica Basal (TMB): {res['tmb_watts_calorias']} kcal/día\n") 
            self.txt_res_nut.insert(tk.END, f"• Gasto Energético Total ({res['nivel_actividad']}): {res['calorias_mantenimiento_diarias']} kcal/día\n") 
            self.txt_res_nut.insert(tk.END, f"• Consumo de Agua Recomendado: {res['hidratacion_diaria_recomendada_litros']} litros/día\n") 

        except Exception: 
            messagebox.showerror("Error", "Revisa los datos ingresados.") 

    # --- TAB 3: REGLAMENTOS DEPORTIVOS --- 
    def _build_tab_reglamentos(self, parent, panel_bg, fg_main, accent): 
        top_f = tk.Frame(parent, bg=panel_bg, padx=8, pady=4, bd=1, relief="solid") 
        top_f.pack(fill="x", pady=(0, 6)) 
        
        tk.Label(top_f, text="Seleccionar Deporte: ", font=("Arial", 9, "bold"), bg=panel_bg).pack(side="left") 
        deportes_lista = list(REGLAMENTO_DEPORTES.keys()) 
        
        self.cmb_dep = ttk.Combobox(top_f, values=deportes_lista, state="readonly", width=30) 
        self.cmb_dep.set(deportes_lista[0]) 
        self.cmb_dep.pack(side="left", padx=6) 
        self.cmb_dep.bind("<<ComboboxSelected>>", self._on_select_deporte) 
        
        self.pnl_dep = PanelBase(parent, titulo="🏀 Ficha Reglamentaria del Deporte", bg_color=panel_bg) 
        self.pnl_dep.pack(fill="both", expand=True) 
        
        self.txt_res_dep = tk.Text(self.pnl_dep, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid", wrap="word") 
        self.txt_res_dep.pack(fill="both", expand=True, padx=4, pady=4) 
        
        self._show_deporte_detail(deportes_lista[0]) 
    
    def _on_select_deporte(self, event=None): 
        self._show_deporte_detail(self.cmb_dep.get()) 
    
    def _show_deporte_detail(self, deporte_key): 
        data = REGLAMENTO_DEPORTES.get(deporte_key, {}) 
        self.txt_res_dep.delete("1.0", tk.END) 
        if not data: 
            return 
        
        self.txt_res_dep.insert(tk.END, f"🏀 REGLAMENTO TÉCNICO: {deporte_key.upper()}\n\n") 
        self.txt_res_dep.insert(tk.END, f"• Jugadores en Cancha: {data['jugadores_en_cancha']}\n") 
        self.txt_res_dep.insert(tk.END, f"• Terreno de Juego: {data['dimensiones_cancha']}\n\n") 
        self.txt_res_dep.insert(tk.END, "📋 Reglas Principales de Juego:\n") 
        for regla in data["reglas_principales"]: 
            self.txt_res_dep.insert(tk.END, f" > {regla}\n") 

    # --- TAB 4: GLOSARIO --- 
    def _build_tab_glosario(self, parent, panel_bg, fg_main, accent):
        self.glosario_ui = GlosarioCentralUI(
            parent,
            titulo="📚 Glosario central de Educación Física",
            data_path=Path(__file__).resolve().parents[2] / "persistance" / "glosario_ed_fisica.json",
        )

        self.glosario_ui.entries = [
            {
                "nombre": term,
                "categorias": ["Educación Física", "Salud"],
                "subcategorias": ["Concepto clave"],
                "contenido": defn,
            }
            for term, defn in DICCIONARIO_ED_FISICA.items()
        ] + getattr(self.glosario_ui, "entries", [])

        if hasattr(self.glosario_ui, "_aplicar_filtro"):
            self.glosario_ui._aplicar_filtro()