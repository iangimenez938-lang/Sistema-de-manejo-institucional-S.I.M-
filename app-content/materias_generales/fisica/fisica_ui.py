import tkinter as tk 
from tkinter import ttk, messagebox 
import sys 
from pathlib import Path 
from typing import Any

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
    def __init__(self, parent=None, titulo="Panel", bg_color="#ffffff", fg_color="#007acc"):
        super().__init__(parent, text=titulo, bg=bg_color, fg=fg_color, font=("Arial", 9, "bold"), bd=1, relief="solid", padx=6, pady=6)

from .herramientas import ( calcular_mru, calcular_mrua, calcular_fuerza_newton, calcular_fuerza_friccion, resolver_ley_ohm, analizar_circuito_resistencias, calcular_consumo_energia_equipos, calcular_energia_mecanica, calcular_ondas_frecuencia_longitud, calcular_refraccion_snell ) 
from configuracion.glosario_central import GlosarioCentralUI

DICCIONARIO_FISICA = {
    "MRU": "Movimiento Rectilíneo Uniforme: el cuerpo recorre distancias iguales en tiempos iguales, manteniendo velocidad constante.",
    "MRUA": "Movimiento Rectilíneo Uniformemente Acelerado: la velocidad cambia de forma constante con el tiempo.",
    "Fuerza": "La fuerza es la interacción que modifica el estado de movimiento o la forma de un cuerpo.",
    "Voltaje": "El voltaje es la diferencia de potencial eléctrico que impulsa la corriente en un circuito.",
    "Corriente": "La corriente eléctrica es el flujo de carga por unidad de tiempo en un conductor.",
    "Resistencia": "La resistencia limita el paso de la corriente y transforma energía eléctrica en calor o trabajo.",
    "Ley de Ohm": "V = I × R: el voltaje es igual al producto entre la corriente y la resistencia.",
    "Frecuencia": "La frecuencia indica cuántos ciclos de una onda ocurren por segundo, medida en hercios (Hz).",
    "Longitud de onda": "La longitud de onda es la distancia entre dos crestas o dos puntos equivalentes de una onda.",
    "Refracción": "La refracción es el cambio de dirección que experimenta la luz al pasar de un medio a otro.",
    "Fibra óptica": "La fibra óptica transmite luz a través de un núcleo y un revestimiento con distintos índices de refracción.",
}

class ModuloFisicaUI(tk.Frame): 
    """ Vista interactiva para el Módulo de Física Aplicada de 4.º Año Informática. Contiene 5 pestañas: Cinemática, Dinámica, Electricidad, Energía/Consumo y Óptica/Ondas. """ 
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
        header_frame = tk.Frame(self, bg=accent, padx=12, pady=8, bd=1, relief="solid") 
        header_frame.pack(fill="x", side="top") 
        
        left_header = tk.Frame(header_frame, bg=accent) 
        left_header.pack(side="left", fill="both", expand=True) 
        tk.Label( left_header, text="⚡ Módulo de Física Aplicada - 4.º Año Informática", font=("Arial", 12, "bold"), fg="#ffffff", bg=accent ).pack(anchor="w") 
        
        tk.Label( left_header, text="Cinemática, Dinámica, Electricidad en Hardware, Consumo Energético y Fibra Óptica / Ondas", font=("Arial", 8), fg="#edf7ff", bg=accent ).pack(anchor="w") 
        
        if self.on_back: 
            btn_volver = tk.Button( header_frame, text="⬅️ Volver al Aula", command=self.on_back, bg="#ffffff", fg=accent, font=("Arial", 8, "bold"), relief="groove", padx=8, pady=2, cursor="hand2" ) 
            btn_volver.pack(side="right") 
            
        style = ttk.Style() 
        style.theme_use("clam") 
        style.configure("Fis.TNotebook", background=bg_main) 
        style.configure("Fis.TNotebook.Tab", font=("Arial", 9, "bold"), padding=[10, 4]) 
        notebook = ttk.Notebook(self, style="Fis.TNotebook") 
        notebook.pack(fill="both", expand=True, padx=8, pady=8) 
        
        # Tab 1: Cinemática & Robótica 
        tab1 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab1, text="🏎️ Cinemática & Movimiento") 
        self._build_tab_cinematica(tab1, panel_bg, fg_main, accent) 
        # Tab 2: Dinámica & Leyes de Newton 
        tab2 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab2, text="⚖️ Dinámica & Newton") 
        self._build_tab_dinamica(tab2, panel_bg, fg_main, accent) 
        # Tab 3: Electricidad & Ley de Ohm en Hardware 
        tab3 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab3, text="⚡ Electricidad & Ley de Ohm") 
        self._build_tab_electricidad(tab3, panel_bg, fg_main, accent) 
        # Tab 4: Energía & Consumo en Equipos 
        tab4 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab4, text="💡 Consumo & Eficiencia") 
        self._build_tab_energia(tab4, panel_bg, fg_main, accent) 
        # Tab 5: Óptica, Fibra Óptica & Ondas 
        tab5 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab5, text="💎 Óptica & Fibra") 
        self._build_tab_ondas_optica(tab5, panel_bg, fg_main, accent) 
        # Tab 6: Glosario central 
        tab6 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab6, text="📚 Glosario") 
        self._build_tab_glosario(tab6, panel_bg, fg_main, accent) 
        
    # --- TAB 1: CINEMÁTICA --- 
    def _build_tab_cinematica(self, parent, panel_bg, fg_main, accent): 
        
        pnl = PanelBase(parent, titulo="🏎️ Calculadora MRU y MRUA (Sensores y Robótica)", bg_color=panel_bg) 
        pnl.pack(fill="x", pady=(0, 6)) 
        
        f_inputs = tk.Frame(pnl, bg=panel_bg) 
        f_inputs.pack(fill="x", pady=4) 
        
        tk.Label(f_inputs, text="Velocidad Inicial v0 (m/s): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=0, sticky="w", pady=2) 
        self.e_v0 = tk.Entry(f_inputs, width=10, justify="center"); self.e_v0.grid(row=0, column=1, padx=4, pady=2); self.e_v0.insert(0, "0") 
        
        tk.Label(f_inputs, text="Aceleración a (m/s²): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=2, sticky="w", pady=2) 
        self.e_a = tk.Entry(f_inputs, width=10, justify="center"); self.e_a.grid(row=0, column=3, padx=4, pady=2); self.e_a.insert(0, "2.5") 
        
        tk.Label(f_inputs, text="Tiempo t (segundos): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=1, column=0, sticky="w", pady=2) 
        self.e_t = tk.Entry(f_inputs, width=10, justify="center"); self.e_t.grid(row=1, column=1, padx=4, pady=2); self.e_t.insert(0, "5") 
        
        btn_mrua = tk.Button( pnl, text="🏎️ Calcular Movimiento (MRUA)", command=self._calc_mrua, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove", cursor="hand2" ) 
        btn_mrua.pack(fill="x", pady=6) 
        
        self.txt_res_cin = tk.Text(parent, height=10, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid") 
        self.txt_res_cin.pack(fill="both", expand=True) 
        
    def _calc_mrua(self): 
        self.txt_res_cin.delete("1.0", tk.END) 
        
        try: 
            v0 = float(self.e_v0.get()) 
            a = float(self.e_a.get()) 
            t = float(self.e_t.get()) 
            res = calcular_mrua(v_inicial=v0, aceleracion=a, tiempo=t)
            if not isinstance(res, dict):
                raise TypeError("La respuesta del cálculo no es válida.")
            if "error" in res:
                self.txt_res_cin.insert(tk.END, f"⚠️ {res.get('error', 'Error desconocido')}n")
                return 

            velocidad_final = float(res.get("velocidad_final", 0.0))
            distancia_recorrida = float(res.get("distancia_recorrida", 0.0))
            pasos = res.get("pasos", [])
            self.txt_res_cin.insert(tk.END, "🏎️ RESULTADOS DE CINEMÁTICA (MRUA):nn")
            self.txt_res_cin.insert(tk.END, f"• Velocidad Final (vf): {velocidad_final} m/s ({round(velocidad_final * 3.6, 2)} km/h)n")
            self.txt_res_cin.insert(tk.END, f"• Distancia Recorrida (d): {distancia_recorrida} metrosnn")
            self.txt_res_cin.insert(tk.END, "📋 Pasos de Resolución:n")

            for paso in pasos:
                self.txt_res_cin.insert(tk.END, f" • {paso}n")
        
        except Exception: 
            messagebox.showerror("Error", "Ingresa datos numéricos válidos.") 
    
    # --- TAB 2: DINÁMICA --- 
    def _build_tab_dinamica(self, parent, panel_bg, fg_main, accent): 
        pnl = PanelBase(parent, titulo="⚖️ Segunda Ley de Newton & Fuerza de Fricción", bg_color=panel_bg) 
        pnl.pack(fill="x", pady=(0, 6)) 
        
        f_in = tk.Frame(pnl, bg=panel_bg) 
        f_in.pack(fill="x", pady=4) 
        
        tk.Label(f_in, text="Masa m (kg): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=0, sticky="w") 
        self.e_m = tk.Entry(f_in, width=10, justify="center"); self.e_m.grid(row=0, column=1, padx=4); self.e_m.insert(0, "15") 
        
        tk.Label(f_in, text="Aceleración a (m/s²): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=2, sticky="w") 
        self.e_acel = tk.Entry(f_in, width=10, justify="center"); self.e_acel.grid(row=0, column=3, padx=4); self.e_acel.insert(0, "3.0") 
        
        tk.Label(f_in, text="Coef. Fricción (μ): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=1, column=0, sticky="w", pady=4) 
        self.e_mu = tk.Entry(f_in, width=10, justify="center"); self.e_mu.grid(row=1, column=1, padx=4, pady=4); self.e_mu.insert(0, "0.25") 
        
        btn_din = tk.Button( pnl, text="⚖️ Calcular Fuerzas y Pesos", command=self._calc_dinamica, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove", cursor="hand2" ) 
        btn_din.pack(fill="x", pady=6) 
        
        self.txt_res_din = tk.Text(parent, height=10, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid") 
        self.txt_res_din.pack(fill="both", expand=True) 
    
    def _calc_dinamica(self): 
        self.txt_res_din.delete("1.0", tk.END) 
        
        try: 
            m = float(self.e_m.get()) 
            a = float(self.e_acel.get()) 
            mu = float(self.e_mu.get()) 
            res_n = calcular_fuerza_newton(m, aceleracion=a) 
            res_f = calcular_fuerza_friccion(m, mu) 
            
            self.txt_res_din.insert(tk.END, "⚖️ RESULTADOS DE DINÁMICA & FUERZAS:nn") 
            self.txt_res_din.insert(tk.END, f"• Fuerza Neta Aplicada (F = m*a): {res_n['fuerza_net_N']} N (Newtons)n") 
            self.txt_res_din.insert(tk.END, f"• Peso del Cuerpo (P = m*g): {res_n['peso_N']} Nn") 
            self.txt_res_din.insert(tk.END, f"• Fuerza Normal (N): {res_f['fuerza_normal_N']} Nn") 
            self.txt_res_din.insert(tk.END, f"• Fuerza de Fricción / Rozamiento (fk): {res_f['fuerza_friccion_N']} Nn") 
        except Exception: 
            messagebox.showerror("Error", "Ingresa datos numéricos válidos.") 
    
    # --- TAB 3: ELECTRICIDAD & LEY DE OHM --- 
    def _build_tab_electricidad(self, parent, panel_bg, fg_main, accent): 
        pnl_ohm = PanelBase(parent, titulo="⚡ Ley de Ohm (V = I × R) & Potencia (P = V × I)", bg_color=panel_bg) 
        pnl_ohm.pack(fill="x", pady=(0, 6)) 
        
        f_o = tk.Frame(pnl_ohm, bg=panel_bg) 
        f_o.pack(fill="x", pady=2) 
        
        tk.Label(f_o, text="Voltaje V (Volts): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=0) 
        self.e_volt = tk.Entry(f_o, width=8, justify="center"); self.e_volt.grid(row=0, column=1); self.e_volt.insert(0, "12") 
        
        tk.Label(f_o, text="Resistencia R (Ω): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=2) 
        self.e_res = tk.Entry(f_o, width=8, justify="center"); self.e_res.grid(row=0, column=3); self.e_res.insert(0, "24") 
        
        btn_ohm = tk.Button( pnl_ohm, text="⚡ Calcular Ley de Ohm", command=self._calc_ohm, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove" ) 
        btn_ohm.pack(fill="x", pady=4) 
        
        pnl_cir = PanelBase(parent, titulo="🔌 Analizador de Circuitos en Hardware (Serie / Paralelo)", bg_color=panel_bg) 
        pnl_cir.pack(fill="x", pady=(0, 6)) 
        
        f_c = tk.Frame(pnl_cir, bg=panel_bg) 
        f_c.pack(fill="x", pady=2) 
        
        tk.Label(f_c, text="Tipo Circuito: ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=0) 
        self.cmb_tipo_c = ttk.Combobox(f_c, values=["Serie", "Paralelo"], state="readonly", width=10) 
        
        self.cmb_tipo_c.set("Serie") 
        self.cmb_tipo_c.grid(row=0, column=1, padx=4) 
        
        tk.Label(f_c, text="Resistencias (Ω, separadas por coma): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=2) 
        self.e_r_lista = tk.Entry(f_c, width=24); self.e_r_lista.grid(row=0, column=3, padx=4); self.e_r_lista.insert(0, "10, 20, 30") 
        
        btn_cir = tk.Button( pnl_cir, text="🔌 Analizar Caídas de Tensión & Corrientes", command=self._calc_circuito, bg="#28a745", fg="#ffffff", font=("Arial", 8, "bold"), relief="groove" ) 
        btn_cir.pack(fill="x", pady=4) 
        
        self.txt_res_elec = tk.Text(parent, height=8, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid") 
        self.txt_res_elec.pack(fill="both", expand=True) 
    
    def _calc_ohm(self): 
        self.txt_res_elec.delete("1.0", tk.END) 
        
        try: 
            v = float(self.e_volt.get()) if self.e_volt.get() else None 
            r = float(self.e_res.get()) if self.e_res.get() else None 
            
            res = resolver_ley_ohm(voltaje=v, resistencia=r) 
            if "error" in res: 
                self.txt_res_elec.insert(tk.END, f"⚠️ {res['error']}n") 
                return 
            
            self.txt_res_elec.insert(tk.END, "⚡ RESULTADOS LEY DE OHM:nn") 
            self.txt_res_elec.insert(tk.END, f"• Voltaje (V): {res['voltaje_V']} Vn") 
            self.txt_res_elec.insert(tk.END, f"• Corriente (I): {res['corriente_A']} A ({res['corriente_mA']} mA)n") 
            self.txt_res_elec.insert(tk.END, f"• Resistencia (R): {res['resistencia_Ohm']} Ωn") 
            self.txt_res_elec.insert(tk.END, f"• Potencia Disipada (P): {res['potencia_W']} Watts (W)n") 
        except Exception: 
            messagebox.showerror("Error", "Ingresa números válidos.") 
    
    def _calc_circuito(self): 
        self.txt_res_elec.delete("1.0", tk.END) 
        
        try: 
            v_f = float(self.e_volt.get() or 12) 
            t_c = self.cmb_tipo_c.get() 
            r_str = self.e_r_lista.get().split(",") 
            r_list = [float(x.strip()) for x in r_str if x.strip()] 
            
            res = analizar_circuito_resistencias(v_f, r_list, tipo_circuito=t_c) 
            if "error" in res: 
                self.txt_res_elec.insert(tk.END, f"⚠️ {res['error']}n") 
                return 
                
            self.txt_res_elec.insert(tk.END, f"🔌 ANÁLISIS DE CIRCUITO EN {res['tipo'].upper()}:nn") 
            self.txt_res_elec.insert(tk.END, f"• Resistencia Equivalente (Req): {res['resistencia_equivalente_Ohm']} Ωn") 
            self.txt_res_elec.insert(tk.END, f"• Corriente Total de Fuente: {res['corriente_total_A']} An") 
            self.txt_res_elec.insert(tk.END, f"• Potencia Total Consumida: {res['potencia_total_W']} Wnn") 
            self.txt_res_elec.insert(tk.END, "📋 Comportamiento por Componente:n") 
            
            componentes = res.get("detalles_componentes", [])
            for comp in componentes:
                if not isinstance(comp, dict):
                    continue
                resistencia = comp.get("resistencia", "R")
                voltaje_v = comp.get("voltaje_V", 0)
                corriente_a = comp.get("corriente_A", 0)
                potencia_w = comp.get("potencia_W", 0)
                self.txt_res_elec.insert(tk.END, f" • {resistencia} -> Voltaje: {voltaje_v}V | Corriente: {corriente_a}A | Potencia: {potencia_w}Wn")
        except Exception: 
            messagebox.showerror("Error", "Ingresa datos válidos.") 
    
    # --- TAB 4: ENERGÍA & CONSUMO --- 
    def _build_tab_energia(self, parent, panel_bg, fg_main, accent): 
        pnl = PanelBase(parent, titulo="💡 Consumo Eléctrico & Eficiencia Energética en Servidores/PCs", bg_color=panel_bg) 
        pnl.pack(fill="x", pady=(0, 6)) 
        
        f_p = tk.Frame(pnl, bg=panel_bg) 
        f_p.pack(fill="x", pady=2) 
        
        tk.Label(f_p, text="Potencia Consumo (Watts): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=0, sticky="w") 
        self.e_p_w = tk.Entry(f_p, width=10, justify="center"); self.e_p_w.grid(row=0, column=1, padx=4); self.e_p_w.insert(0, "450") 
        
        tk.Label(f_p, text="Horas Uso Diarias: ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=2, sticky="w") 
        self.e_hrs = tk.Entry(f_p, width=10, justify="center"); self.e_hrs.grid(row=0, column=3, padx=4); self.e_hrs.insert(0, "12") 
        
        tk.Label(f_p, text="Precio kWh ($): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=1, column=0, sticky="w", pady=4) 
        self.e_pkwh = tk.Entry(f_p, width=10, justify="center"); self.e_pkwh.grid(row=1, column=1, padx=4, pady=4); self.e_pkwh.insert(0, "65.0") 
        
        btn_p = tk.Button( pnl, text="💡 Calcular Consumo y Costo Energético", command=self._calc_consumo, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove", cursor="hand2" ) 
        btn_p.pack(fill="x", pady=4) 
        
        self.txt_res_ene = tk.Text(parent, height=10, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid") 
        self.txt_res_ene.pack(fill="both", expand=True) 
    
    def _calc_consumo(self): 
        self.txt_res_ene.delete("1.0", tk.END) 
        
        try: 
            w = float(self.e_p_w.get()) 
            hrs = float(self.e_hrs.get()) 
            pkwh = float(self.e_pkwh.get()) 
            res = calcular_consumo_energia_equipos(w, hrs, precio_kwh=pkwh) 
            
            self.txt_res_ene.insert(tk.END, "💡 AUDITORÍA Y ESTIMACIÓN DE CONSUMO ENERGÉTICO:nn") 
            self.txt_res_ene.insert(tk.END, f"• Potencia Nominal: {res['potencia_watts']} W ({res['potencia_kw']} kW)n") 
            self.txt_res_ene.insert(tk.END, f"• Consumo Diario Estimado: {res['kwh_diarios']} kWh/dían") 
            self.txt_res_ene.insert(tk.END, f"• Consumo Mensual Proyectado (30 días): {res['kwh_mensuales']} kWh/mesn") 
            self.txt_res_ene.insert(tk.END, f"• Costo Estimado en Factura: ${res['costo_estimado_mensual']} ARS/mesn") 
        except Exception: 
            messagebox.showerror("Error", "Ingresa números válidos.") 
    
    # --- TAB 5: ONDAS & OPTICA --- 
    def _build_tab_ondas_optica(self, parent, panel_bg, fg_main, accent): 
        pnl_s = PanelBase(parent, titulo="💎 Óptica & Refracción Ley de Snell (Fibra Óptica)", bg_color=panel_bg) 
        pnl_s.pack(fill="x", pady=(0, 6)) 
        
        f_s = tk.Frame(pnl_s, bg=panel_bg) 
        f_s.pack(fill="x", pady=2) 
        
        tk.Label(f_s, text="Índice Núcleo n1: ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=0) 
        self.e_n1 = tk.Entry(f_s, width=6, justify="center"); self.e_n1.grid(row=0, column=1); self.e_n1.insert(0, "1.48") 
        
        tk.Label(f_s, text="Índice Revestimiento n2: ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=2) 
        self.e_n2 = tk.Entry(f_s, width=6, justify="center"); self.e_n2.grid(row=0, column=3); self.e_n2.insert(0, "1.44") 
        
        tk.Label(f_s, text="Ángulo Incidencia (°): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=4) 
        self.e_ang = tk.Entry(f_s, width=6, justify="center"); self.e_ang.grid(row=0, column=5); self.e_ang.insert(0, "80") 
        
        btn_snell = tk.Button( pnl_s, text="💎 Evaluar Refracción y Reflexión Total Interna", command=self._calc_snell, bg="#28a745", fg="#ffffff", font=("Arial", 8, "bold"), relief="groove" ) 
        btn_snell.pack(fill="x", pady=4) 
        
        self.txt_res_ond = tk.Text(parent, height=8, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid") 
        self.txt_res_ond.pack(fill="both", expand=True) 
        
    def _build_tab_glosario(self, parent, panel_bg, fg_main, accent):
        self.glosario_ui = GlosarioCentralUI(
            parent,
            titulo="📚 Glosario central de Física",
            data_path=Path(__file__).resolve().parents[2] / "persistance" / "glosario_central.json",
        )

        if hasattr(self.glosario_ui, "entries"):
            self.glosario_ui.entries = [
                {
                    "nombre": nombre,
                    "categorias": ["Física"],
                    "subcategorias": ["Concepto básico"],
                    "contenido": contenido,
                }
                for nombre, contenido in DICCIONARIO_FISICA.items()
            ] + self.glosario_ui.entries

        if hasattr(self.glosario_ui, "_aplicar_filtro"):
            self.glosario_ui._aplicar_filtro()
        
    def _calc_ondas(self): 
        self.txt_res_ond.delete("1.0", tk.END) 

        try:
            texto_freq = str(getattr(self.e_freq, "get", lambda: "")()).replace(",", ".").strip()
            texto_lambda = str(getattr(self.e_lambda, "get", lambda: "")()).replace(",", ".").strip()

            if not texto_freq and not texto_lambda:
                self.txt_res_ond.insert(tk.END, "🌐 Ingresá una frecuencia o una longitud de onda para calcular.\n")
                return

            if texto_freq and texto_lambda:
                texto_principal = texto_freq
            elif texto_freq:
                texto_principal = texto_freq
            else:
                texto_principal = texto_lambda

            valor = float(texto_principal)
            if valor <= 0:
                self.txt_res_ond.insert(tk.END, "🌐 El valor ingresado debe ser mayor a cero.\n")
                return

            if texto_freq and not texto_lambda:
                res = calcular_ondas_frecuencia_longitud(frecuencia_hz=valor)
            elif texto_lambda and not texto_freq:
                res = calcular_ondas_frecuencia_longitud(longitud_onda_m=valor)
            else:
                res = calcular_ondas_frecuencia_longitud(frecuencia_hz=valor)

            if "error" in res:
                self.txt_res_ond.insert(tk.END, f"🌐 {res['error']}\n")
                return

            self.txt_res_ond.insert(tk.END, "🌐 ANÁLISIS DE TELECOMUNICACIONES & ONDAS:\n\n")
            self.txt_res_ond.insert(tk.END, f"• Frecuencia Señal: {res['frecuencia_Hz']} Hz ({res['frecuencia_MHz']} MHz)\n")
            self.txt_res_ond.insert(tk.END, f"• Longitud de Onda (λ): {res['longitud_onda_m']} metros ({res['longitud_onda_nm']} nm)\n")
        except Exception:
            self.txt_res_ond.insert(tk.END, "🌐 No se pudo calcular con ese valor. Probá con un número positivo.\n")
            return
    
    def _calc_snell(self): 
        self.txt_res_ond.delete("1.0", tk.END) 
        
        try: 
            n1 = float(self.e_n1.get()) 
            n2 = float(self.e_n2.get()) 
            ang = float(self.e_ang.get()) 
            res = calcular_refraccion_snell(n1, n2, ang) 
            
            self.txt_res_ond.insert(tk.END, "💎 COMPORTAMIENTO ÓPTICO EN FIBRA ÓPTICA:nn") 
            self.txt_res_ond.insert(tk.END, f"• Evento Óptico: {res['evento']}n") 
            if "angulo_refraccion_grados" in res: 
                self.txt_res_ond.insert(tk.END, f"• Ángulo de Refracción Salida: {res['angulo_refraccion_grados']}°n") 
            if "angulo_critico_grados" in res: 
                self.txt_res_ond.insert(tk.END, f"• Ángulo Límite Crítico: {res['angulo_critico_grados']}°n") 
        except Exception: 
            messagebox.showerror("Error", "Ingresa números válidos.")