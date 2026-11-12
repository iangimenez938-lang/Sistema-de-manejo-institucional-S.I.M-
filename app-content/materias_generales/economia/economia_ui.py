import tkinter as tk 
from tkinter import ttk, messagebox 
import sys 
from pathlib import Path 
from typing import Any

BASE_DIR = Path(__file__).resolve().parent.parent.parent 
if str(BASE_DIR) not in sys.path: 
    sys.path.insert(0, str(BASE_DIR)) 

try:
    from configuracion.config_manager import cargar_configuracion as _cargar_configuracion
    from configuracion.config_manager import aplicar_estilos_globales as _aplicar_estilos_globales
except ImportError:
    def cargar_configuracion() -> dict[str, Any]:
        return {}

    def aplicar_estilos_globales(root, config) -> None:
        return None
else:
    def cargar_configuracion() -> dict[str, Any]:
        return _cargar_configuracion()

    def aplicar_estilos_globales(root, config) -> None:
        _aplicar_estilos_globales(root, config)


class PanelBase(tk.LabelFrame): 
    """Contenedor reutilizable para los paneles del módulo."""
    def __init__(self, parent=None, titulo="Panel", bg_color="#ffffff", fg_color="#007acc"):
        super().__init__(parent, text=titulo, bg=bg_color, fg=fg_color, font=("Arial", 9, "bold"), bd=1, relief="solid", padx=6, pady=6)
            
from .herramientas import ( calcular_punto_equilibrio, simular_mercado_oferta_demanda, calcular_elasticidad_precio, evaluar_viabilidad_van, analizar_texto_economico, CATALOGO_ESCUELAS_ECONOMICAS, DICCIONARIO_ECONOMICO ) 
from configuracion.glosario_central import GlosarioCentralUI

class ModuloEconomiaUI(tk.Frame): 
    """ Vista interactiva para el Módulo de Economía de 4.º Año Informática. Contiene 5 pestañas: Costos/Equilibrio, Mercado, Análisis de Textos, Escuelas Económicas y Viabilidad/Glosario. """ 
    def __init__(self, parent=None, contexto: dict[str, Any] | None = None, on_back_callback=None): 
        self.contexto: dict[str, Any] = contexto or {} 
        self.on_back = on_back_callback 
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
        # 1. Encabezado del Módulo 
        header_frame = tk.Frame(self, bg=accent, padx=12, pady=8, bd=1, relief="solid") 
        header_frame.pack(fill="x", side="top") 
        
        left_header = tk.Frame(header_frame, bg=accent) 
        left_header.pack(side="left", fill="both", expand=True) 
        
        tk.Label( left_header, text="📊 Módulo de Economía - 4.º Año Informática", font=("Arial", 12, "bold"), fg="#ffffff", bg=accent ).pack(anchor="w") 
        tk.Label( left_header, text="Análisis de Textos, Escuelas del Pensamiento Económico, Micro/Macroeconomía y Viabilidad de Proyectos", font=("Arial", 8), fg="#edf7ff", bg=accent ).pack(anchor="w") 
        
        if self.on_back: 
            btn_volver = tk.Button( header_frame, text="⬅️ Volver al Aula", command=self.on_back, bg="#ffffff", fg=accent, font=("Arial", 8, "bold"), relief="groove", padx=8, pady=2, cursor="hand2" ) 
            btn_volver.pack(side="right") 
            
        # 2. Contenedor de Pestañas (Notebook) 
        style = ttk.Style() 
        style.theme_use("clam") 
        style.configure("Eco.TNotebook", background=bg_main) 
        style.configure("Eco.TNotebook.Tab", font=("Arial", 9, "bold"), padding=[10, 4]) 
        notebook = ttk.Notebook(self, style="Eco.TNotebook") 
        notebook.pack(fill="both", expand=True, padx=8, pady=8) 
        
        # Tab 1: Punto de Equilibrio & Costos 
        tab1 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab1, text="🧮 Punto de Equilibrio & Costos") 
        self._build_tab_equilibrio(tab1, panel_bg, fg_main, accent) 
        # Tab 2: Oferta, Demanda & Mercado 
        tab2 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab2, text="📈 Mercado & Elasticidad") 
        self._build_tab_mercado(tab2, panel_bg, fg_main, accent) 
        # Tab 3: Analizador de Textos & Guía de Respuestas 
        tab3 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab3, text="📄 Análisis de Textos & Guías") 
        self._build_tab_analisis_textos(tab3, panel_bg, fg_main, accent) 
        # Tab 4: Escuelas del Pensamiento Económico 
        tab4 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab4, text="🏛️ Escuelas & Pensadores") 
        self._build_tab_escuelas(tab4, panel_bg, fg_main, accent) 
        # Tab 5: Viabilidad Financiera & Glosario 
        tab5 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab5, text="💡 Viabilidad & Glosario") 
        self._build_tab_viabilidad_glosario(tab5, panel_bg, fg_main, accent) 
        
    # --- TAB 1: PUNTO DE EQUILIBRIO --- 
    def _build_tab_equilibrio(self, parent, panel_bg, fg_main, accent): 
        pnl = PanelBase(parent, titulo="🧮 Calculadora de Punto de Equilibrio (Break-Even)", bg_color=panel_bg) 
        pnl.pack(fill="x", pady=(0, 6)) 
        
        f_inputs = tk.Frame(pnl, bg=panel_bg) 
        f_inputs.pack(fill="x", pady=4) 
        
        tk.Label(f_inputs, text="Costos Fijos Totales ($): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=0, sticky="w", pady=2) 
        self.e_cf = tk.Entry(f_inputs, width=12, justify="center"); self.e_cf.grid(row=0, column=1, padx=4, pady=2); self.e_cf.insert(0, "100000") 
        
        tk.Label(f_inputs, text="Precio Venta Unitario ($): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=2, sticky="w", pady=2) 
        self.e_pv = tk.Entry(f_inputs, width=12, justify="center"); self.e_pv.grid(row=0, column=3, padx=4, pady=2); self.e_pv.insert(0, "150") 
        
        tk.Label(f_inputs, text="Costo Variable Unitario ($): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=1, column=0, sticky="w", pady=2) 
        self.e_cvu = tk.Entry(f_inputs, width=12, justify="center"); self.e_cvu.grid(row=1, column=1, padx=4, pady=2); self.e_cvu.insert(0, "50") 
        
        tk.Label(f_inputs, text="Unidades Estimadas a Vender: ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=1, column=2, sticky="w", pady=2) 
        self.e_u_est = tk.Entry(f_inputs, width=12, justify="center"); self.e_u_est.grid(row=1, column=3, padx=4, pady=2); self.e_u_est.insert(0, "1500") 
        
        btn_calc = tk.Button( pnl, text="🧮 Calcular Punto de Equilibrio y Resultados", command=self._calc_equilibrio, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove", cursor="hand2" ) 
        btn_calc.pack(fill="x", pady=6) 
        
        self.txt_res_bep = tk.Text(parent, height=10, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid") 
        self.txt_res_bep.pack(fill="both", expand=True) 
    
    def _calc_equilibrio(self): 
        self.txt_res_bep.delete("1.0", tk.END) 
        
        try: 
            cf = float(self.e_cf.get()) 
            pv = float(self.e_pv.get()) 
            cvu = float(self.e_cvu.get()) 
            u_est = int(float(self.e_u_est.get() or 0))

            res = calcular_punto_equilibrio(cf, pv, cvu, u_est) 
            if "error" in res: 
                self.txt_res_bep.insert(tk.END, f"⚠️ {res['error']}n") 
                return 
                
            self.txt_res_bep.insert(tk.END, "📊 RESULTADOS DEL ANÁLISIS DE PUNTO DE EQUILIBRIO:nn") 
            self.txt_res_bep.insert(tk.END, f"• Punto de Equilibrio (Unidades Mínimas): {res['punto_equilibrio_unidades']} unidadesn") 
            self.txt_res_bep.insert(tk.END, f"• Ingreso de Equilibrio Mínimo: ${res['ingreso_equilibrio']}n") 
            self.txt_res_bep.insert(tk.END, f"• Margen de Contribución Unitario: ${res['margen_contribucion_unitario']}/unidad ({res['ratio_margen_contribucion']}%)n") 
            
            if "unidades_estimadas" in res: 
                self.txt_res_bep.insert(tk.END, f"n📈 EVALUACIÓN CON VOLUMEN ESTIMADO DE {res['unidades_estimadas']} UNIDADES:n") 
                self.txt_res_bep.insert(tk.END, f" > Ingresos Totales: ${res['ingreso_estimado']}n") 
                self.txt_res_bep.insert(tk.END, f" > Costos Totales: ${res['costo_total_estimado']}n") 
                self.txt_res_bep.insert(tk.END, f" > Resultado Económico (Utilidad): ${res['utilidad_estimada']} ({res['estado_proyecto']})n") 
        
        except Exception: 
            messagebox.showerror("Error", "Ingresa datos numéricos válidos.") 
    
    # --- TAB 2: MERCADO & ELASTICIDAD --- 
    def _build_tab_mercado(self, parent, panel_bg, fg_main, accent): 
        pnl_mkt = PanelBase(parent, titulo="📈 Simulador de Oferta, Demanda y Elasticidad", bg_color=panel_bg) 
        pnl_mkt.pack(fill="x", pady=(0, 6)) 
        
        f_eq = tk.Frame(pnl_mkt, bg=panel_bg) 
        f_eq.pack(fill="x", pady=2) 
        
        tk.Label(f_eq, text="Demanda Qd = ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=0) 
        self.e_adem = tk.Entry(f_eq, width=6, justify="center"); self.e_adem.grid(row=0, column=1); self.e_adem.insert(0, "1000") 
        
        tk.Label(f_eq, text=" - ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=2) 
        self.e_bdem = tk.Entry(f_eq, width=6, justify="center"); self.e_bdem.grid(row=0, column=3); self.e_bdem.insert(0, "5") 
        
        tk.Label(f_eq, text=" * P | Oferta Qo = ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=4) 
        self.e_aofe = tk.Entry(f_eq, width=6, justify="center"); self.e_aofe.grid(row=0, column=5); self.e_aofe.insert(0, "200") 
        
        tk.Label(f_eq, text=" + ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=6) 
        self.e_bofe = tk.Entry(f_eq, width=6, justify="center"); self.e_bofe.grid(row=0, column=7); self.e_bofe.insert(0, "3") 
        
        tk.Label(f_eq, text=" * P", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=8) 
        
        f_eval = tk.Frame(pnl_mkt, bg=panel_bg) 
        f_eval.pack(fill="x", pady=4) 
        
        tk.Label(f_eval, text="Precio de Mercado a Evaluar ($): ", font=("Arial", 8, "bold"), bg=panel_bg).pack(side="left") 
        self.e_peval = tk.Entry(f_eval, width=10, justify="center"); self.e_peval.pack(side="left", padx=4); self.e_peval.insert(0, "110") 
        
        btn_mkt = tk.Button(pnl_mkt, text="📈 Calcular Equilibrio de Mercado", command=self._calc_mercado, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove", cursor="hand2") 
        btn_mkt.pack(fill="x", pady=4) 
        
        self.txt_res_mkt = tk.Text(parent, height=8, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid") 
        self.txt_res_mkt.pack(fill="both", expand=True) 

        pnl_van = PanelBase(parent, titulo="💡 Evaluación Financiera de Proyectos (VAN)", bg_color=panel_bg) 
        pnl_van.pack(fill="x", pady=(8, 6)) 

        f_v = tk.Frame(pnl_van, bg=panel_bg) 
        f_v.pack(fill="x", pady=2) 

        tk.Label(f_v, text="Inversión Inicial ($): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=0, sticky="w") 
        self.e_inv = tk.Entry(f_v, width=10, justify="center"); self.e_inv.grid(row=0, column=1, padx=4); self.e_inv.insert(0, "500000") 

        tk.Label(f_v, text="Tasa de Descuento (%): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=2, sticky="w") 
        self.e_tasa = tk.Entry(f_v, width=6, justify="center"); self.e_tasa.grid(row=0, column=3, padx=4); self.e_tasa.insert(0, "12") 

        tk.Label(f_v, text="Flujos Anuales (separados por coma): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=1, column=0, columnspan=2, sticky="w", pady=4) 
        self.e_flujos = tk.Entry(f_v, width=28); self.e_flujos.grid(row=1, column=2, columnspan=2, sticky="ew", pady=4); self.e_flujos.insert(0, "150000, 200000, 250000, 280000") 

        btn_van = tk.Button(pnl_van, text="💡 Evaluar Viabilidad VAN & Payback", command=self._calc_van, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove", cursor="hand2") 
        btn_van.pack(fill="x", pady=4) 

        self.txt_van_resultado = tk.Text(pnl_van, height=8, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid") 
        self.txt_van_resultado.pack(fill="both", expand=True) 
    
    def _calc_mercado(self): 
        self.txt_res_mkt.delete("1.0", tk.END) 
        
        try: 
            adem, bdem = float(self.e_adem.get()), float(self.e_bdem.get()) 
            aofe, bofe = float(self.e_aofe.get()), float(self.e_bofe.get()) 
            peval = float(self.e_peval.get() or 0) 
            
            res = simular_mercado_oferta_demanda(adem, bdem, aofe, bofe, peval) 
            if "error" in res: 
                self.txt_res_mkt.insert(tk.END, f"⚠️ {res['error']}n") 
                return 
            
            self.txt_res_mkt.insert(tk.END, "📈 SIMULACIÓN DE EQUILIBRIO DE MERCADO:nn") 
            self.txt_res_mkt.insert(tk.END, f"• Precio de Equilibrio (P*): ${res['precio_equilibrio']}n") 
            self.txt_res_mkt.insert(tk.END, f"• Cantidad de Equilibrio (Q*): {res['cantidad_equilibrio']} unidadesnn") 
            
            if "precio_evaluado" in res: 
                self.txt_res_mkt.insert(tk.END, f"🔍 SITUACIÓN CON PRECIO EVALUADO EN ${res['precio_evaluado']}:n") 
                self.txt_res_mkt.insert(tk.END, f" > Demanda Demandada (Qd): {res['demanda_actual']} unidadesn") 
                self.txt_res_mkt.insert(tk.END, f" > Oferta Ofrecida (Qo): {res['oferta_actual']} unidadesn") 
                self.txt_res_mkt.insert(tk.END, f" > Diagnóstico: {res['situacion_mercado']}n") 
        
        except Exception: 
            messagebox.showerror("Error", "Ingresa números válidos.") 
    
    # --- TAB 3: ANÁLISIS DE TEXTOS & GUÍA DE RESPUESTAS --- 
    def _build_tab_analisis_textos(self, parent, panel_bg, fg_main, accent): 
        pnl_txt = PanelBase(parent, titulo="📄 Analizador de Textos Económicos & Extractor de Ideas", bg_color=panel_bg) 
        pnl_txt.pack(fill="x", pady=(0, 6)) 
        
        tk.Label( pnl_txt, text="Pega o escribe el texto / noticia económica a analizar en tus clases:", font=("Arial", 8, "italic"), bg=panel_bg, fg=fg_main ).pack(anchor="w") 
        self.txt_input_analisis = tk.Text(pnl_txt, height=5, font=("Arial", 9), bg="#ffffff", bd=1, relief="solid") 
        self.txt_input_analisis.pack(fill="x", pady=4) 
        self.txt_input_analisis.insert( "1.0", "La inflación en Argentina afecta la estabilidad de los costos fijos de las empresas tecnológicas. " "Es necesario equilibrar los ingresos y ajustar el presupuesto. " "La transformación digital y el comercio electrónico impulsan la productividad en las pymes." ) 
        
        btn_analizar_t = tk.Button( pnl_txt, text="🔍 Analizar Texto & Extraer Guía de Preguntas / Respuestas", command=self._procesar_texto_analisis, bg="#28a745", fg="#ffffff", font=("Arial", 8, "bold"), relief="groove", cursor="hand2" ) 
        btn_analizar_t.pack(fill="x", pady=4) 
        
        self.txt_res_analisis = tk.Text(parent, height=10, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid") 
        self.txt_res_analisis.pack(fill="both", expand=True) 
    
    def _procesar_texto_analisis(self): 
        texto_raw = self.txt_input_analisis.get("1.0", tk.END).strip() 
        
        self.txt_res_analisis.delete("1.0", tk.END) 
        res = analizar_texto_economico(texto_raw) 
        if "error" in res: 
            self.txt_res_analisis.insert(tk.END, f"⚠️ {res['error']}n") 
            return 
        
        self.txt_res_analisis.insert(tk.END, "📋 ANÁLISIS DE TEXTO Y CONCEPTOS CLAVES:nn") 
        palabras_clave = res.get("palabras_clave", [])
        self.txt_res_analisis.insert(tk.END, f"• Palabras Clave Económicas Detectadas: {', '.join(palabras_clave)}nn")
        resumen = res.get("resumen_ejecutivo", "")
        self.txt_res_analisis.insert(tk.END, f'📝 Resumen Ejecutivo:\n"{resumen}"\n\n')
        self.txt_res_analisis.insert(tk.END, "❓ GUÍA DE PREGUNTAS Y RESPUESTAS RECOMENDADAS:n") 

        for idx, qa in enumerate(res.get("guia_preguntas_respuestas", []), start=1):
            if not isinstance(qa, dict):
                continue
            pregunta = qa.get("pregunta", "")
            respuesta = qa.get("respuesta", "")
            self.txt_res_analisis.insert(tk.END, f"n P{idx}. {pregunta}n")
            self.txt_res_analisis.insert(tk.END, f" R{idx}. {respuesta}n")
    
    # --- TAB 4: ESCUELAS ECONÓMICAS & PENSADORES --- 
    def _build_tab_escuelas(self, parent, panel_bg, fg_main, accent): 
        top_f = tk.Frame(parent, bg=panel_bg, padx=8, pady=4, bd=1, relief="solid") 
        top_f.pack(fill="x", pady=(0, 6)) 
        
        tk.Label(top_f, text="Selecciona Escuela Económica: ", font=("Arial", 9, "bold"), bg=panel_bg).pack(side="left") 
        escuelas_lista = list(CATALOGO_ESCUELAS_ECONOMICAS.keys()) 
        
        self.cmb_escuelas = ttk.Combobox(top_f, values=escuelas_lista, state="readonly", width=40) 
        self.cmb_escuelas.set(escuelas_lista[2]) 
        self.cmb_escuelas.pack(side="left", padx=6) 
        self.cmb_escuelas.bind("<<ComboboxSelected>>", self._on_seleccionar_escuela) 
        
        self.pnl_esc = PanelBase(parent, titulo="🏛️ Ficha Histórica y Teórica", bg_color=panel_bg) 
        self.pnl_esc.pack(fill="both", expand=True) 
        
        self.txt_info_escuela = tk.Text(self.pnl_esc, font=("Arial", 9), bg="#ffffff", bd=1, relief="solid") 
        self.txt_info_escuela.pack(fill="both", expand=True, padx=4, pady=4) 
        
        self._mostrar_detalle_escuela(escuelas_lista[2]) 
    
    def _on_seleccionar_escuela(self, event=None): 
        esc_sel = self.cmb_escuelas.get() 
        self._mostrar_detalle_escuela(esc_sel) 
    
    def _mostrar_detalle_escuela(self, nombre_escuela): 
        data = CATALOGO_ESCUELAS_ECONOMICAS.get(nombre_escuela, {}) 
        self.txt_info_escuela.delete("1.0", tk.END) 
        
        if not data: 
            return 
            
        self.txt_info_escuela.insert(tk.END, f"🏛️ {nombre_escuela.upper()}\n\n") 
        self.txt_info_escuela.insert(tk.END, f"• Época / Período: {data['epoca']}\n") 
        self.txt_info_escuela.insert(tk.END, f"• Contexto Histórico: {data['contexto']}\n\n") 
        self.txt_info_escuela.insert(tk.END, "👨‍🏫 PRINCIPALES PENSADORES Y EXPONENTES:\n") 
        for p in data["pensadores"]: 
            self.txt_info_escuela.insert(tk.END, f" > {p}\n") 
            self.txt_info_escuela.insert(tk.END, "\n💡 IDEAS Y POSTULADOS CENTRALES:\n") 
        for idea in data["ideas_clave"]: 
            self.txt_info_escuela.insert(tk.END, f" • {idea}\n") 
    
# --- TAB 5: GLOSARIO CENTRAL DE CONCEPTOS ECONÓMICOS --- 
    def _build_tab_viabilidad_glosario(self, parent, panel_bg, fg_main, accent):
        self.glosario_ui = GlosarioCentralUI(
            parent,
            titulo="📚 Glosario central de Economía",
            data_path=Path(__file__).resolve().parents[2] / "persistance" / "glosario_central.json",
        )

        if hasattr(self.glosario_ui, "entries"):
            self.glosario_ui.entries = [
                {
                    "nombre": nombre,
                    "categorias": ["Economía"],
                    "subcategorias": ["Texto explicativo"],
                    "contenido": contenido,
                }
                for nombre, contenido in DICCIONARIO_ECONOMICO.items()
            ] + self.glosario_ui.entries

        if hasattr(self.glosario_ui, "_aplicar_filtro"):
            self.glosario_ui._aplicar_filtro()

    def _mostrar_termino_glosario(self):
        return None

    def _calc_van(self):
        try:
            if not hasattr(self, "txt_van_resultado"):
                return

            inv = float(self.e_inv.get())
            tasa = float(self.e_tasa.get())
            flujos_str = self.e_flujos.get().split(",")
            flujos = [float(f.strip()) for f in flujos_str if f.strip()]

            res = evaluar_viabilidad_van(inv, flujos, tasa)

            self.txt_van_resultado.delete("1.0", tk.END)
            self.txt_van_resultado.insert(tk.END, "💡 EVALUACIÓN DE VIABILIDAD DE PROYECTO:\n\n")
            self.txt_van_resultado.insert(tk.END, f"• Dictamen: {res['dictamen']}\n")
            self.txt_van_resultado.insert(tk.END, f"• Valor Actual Neto (VAN): ${res['van']}\n")
            self.txt_van_resultado.insert(tk.END, f"• Período de Recuperación (Payback): {res['periodo_recuperacion_periodos']} años/períodos\n")
            self.txt_van_resultado.insert(tk.END, f"• Flujos Descontados Anuales: {res['flujos_descontados']}\n")
        except Exception:
            messagebox.showerror("Error", "Ingresa valores válidos.")
