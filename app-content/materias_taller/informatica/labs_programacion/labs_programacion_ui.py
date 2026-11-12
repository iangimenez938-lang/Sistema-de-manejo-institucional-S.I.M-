# pyright: reportAttributeAccessIssue=false
# pyright: reportCallIssue=false
# pyright: reportGeneralTypeIssues=false
# pyright: reportAssignmentType=false
from typing import Any

try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    HAS_TKINTER = True
except (ImportError, Exception):
    HAS_TKINTER = False

    class Dummy:
        Frame = object
        Label = object
        Button = object
        Entry = object
        Text = object
        LabelFrame = object
        Notebook = object
        Combobox = object
        Style = object
        END = ""

        def __init__(self, *args, **kwargs):
            pass

        def pack(self, *args, **kwargs):
            pass

        def grid(self, *args, **kwargs):
            pass

        def config(self, *args, **kwargs):
            pass

    tk: Any = Dummy()
    tk.Frame = Dummy
    tk.Label = Dummy
    tk.Button = Dummy
    tk.Entry = Dummy
    tk.Text = Dummy
    tk.LabelFrame = Dummy

    ttk: Any = Dummy()
    ttk.Notebook = Dummy
    ttk.Combobox = Dummy
    ttk.Style = Dummy

    messagebox = Dummy()

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from configuracion.config_manager import cargar_configuracion, aplicar_estilos_globales
    from configuracion.glosario_central import GlosarioCentralUI
    from vistas.componentes_ui import PanelBase  # type: ignore[assignment]
except ImportError:
    def cargar_configuracion() -> dict[str, object]:
        return {}

    def aplicar_estilos_globales(root: Any, config: dict[str, object]) -> None:
        return None

    class GlosarioCentralUI:
        def __init__(self, *args, **kwargs):
            self.entries = []

    class _FallbackPanelBase:
        def __init__(self, *args, **kwargs):
            pass

        def pack(self, *args, **kwargs):
            pass

        def grid(self, *args, **kwargs):
            pass

        def config(self, *args, **kwargs):
            pass

    PanelBase = _FallbackPanelBase

try:
    from configuracion.config_manager import cargar_configuracion, aplicar_estilos_globales
    from configuracion.glosario_central import GlosarioCentralUI
    from vistas.componentes_ui import PanelBase  # type: ignore[assignment]
except ImportError:
    def cargar_configuracion() -> dict[str, object]:
        return {}

    def aplicar_estilos_globales(root: Any, config: dict[str, object]) -> None:
        return None

    class _FallbackPanelBase:
        def __init__(self, *args, **kwargs):
            pass

        def pack(self, *args, **kwargs):
            pass

        def grid(self, *args, **kwargs):
            pass

        def config(self, *args, **kwargs):
            pass

    PanelBase = _FallbackPanelBase

try:
    from .herramientas import (
        interpretar_pseudocodigo,
        generar_diagrama_flujo,
        generar_tabla_verdad,
        DICCIONARIO_PROGRAMACION,
    )
except ImportError:
    def interpretar_pseudocodigo(codigo_str: str, entradas_usuario: dict[str, object] | None = None) -> dict[str, Any]:
        return {"error": "No se pudo cargar el intérprete de pseudocódigo."}

    def generar_diagrama_flujo(codigo_str: str) -> dict[str, Any]:
        return {"total_nodos": 0, "diagrama_nodos": []}

    def generar_tabla_verdad(expresion_booleana: str) -> dict[str, Any]:
        return {"expresion": expresion_booleana, "variables": ["A", "B"], "filas_tabla": []}

    DICCIONARIO_PROGRAMACION = {}
            
class _FallbackTkFrame:
    def __init__(self, *args, **kwargs):
        pass

    def pack(self, *args, **kwargs):
        pass

    def grid(self, *args, **kwargs):
        pass

    def config(self, *args, **kwargs):
        pass


if HAS_TKINTER:
    _BaseFrame = tk.Frame
else:
    _BaseFrame = _FallbackTkFrame


class ModuloLabsProgramacionUI(_BaseFrame):
    """ Vista interactiva para Laboratorios de Programación (4.º Año Informática). Contiene 4 pestañas: Intérprete Pseudocódigo, Diagramador de Flujo, Tablas de Verdad y Glosario. """ 
    
    def __init__(self, parent=None, contexto: dict[str, object] | None = None, on_back_callback=None):
        self.contexto: dict[str, object] = contexto or {}
        self.on_back = on_back_callback
        self.glosario_ui = None
        self.txt_codigo_diagrama = None

        if not HAS_TKINTER:
            return

        self.config_val = cargar_configuracion()
        bg_main = str(self.config_val.get("bg_color", "#ffffff"))
        panel_bg = str(self.config_val.get("panel_bg", "#f8f9fa"))
        fg_main = str(self.config_val.get("fg_color", "#212529"))
        accent = str(self.config_val.get("accent_color", "#007acc"))
        super().__init__(parent, bg=bg_main)

        self.pack(fill="both", expand=True)
        self._build_ui(bg_main=bg_main, panel_bg=panel_bg, fg_main=fg_main, accent=accent)
        aplicar_estilos_globales(self, self.config_val) 
        
    def _build_ui(self, bg_main="#ffffff", panel_bg="#f8f9fa", fg_main="#212529", accent="#007acc"): 
        if not HAS_TKINTER: 
            return 
        
        header_frame = tk.Frame(self, bg=accent, padx=12, pady=8, bd=1, relief="solid") 
        header_frame.pack(fill="x", side="top") 
        
        left_header = tk.Frame(header_frame, bg=accent) 
        left_header.pack(side="left", fill="both", expand=True) 
        tk.Label( left_header, text="💻 Labs. Programación - 4.º Año Especialidad Informática", font=("Arial", 12, "bold"), fg="#ffffff", bg=accent ).pack(anchor="w") 
        tk.Label( left_header, text="Lógica Algorítmica, Intérprete de Pseudocódigo, Diagramador de Flujo y Tablas de Verdad", font=("Arial", 8), fg="#edf7ff", bg=accent ).pack(anchor="w") 
        
        if self.on_back: 
            btn_volver = tk.Button( header_frame, text="⬅️ Volver al Aula", command=self.on_back, bg="#ffffff", fg=accent, font=("Arial", 8, "bold"), relief="groove", padx=8, pady=2, cursor="hand2" ) 
            btn_volver.pack(side="right") 
            
        style = ttk.Style() 
        style.theme_use("clam") 
        style.configure("Prog.TNotebook", background=bg_main) 
        style.configure("Prog.TNotebook.Tab", font=("Arial", 9, "bold"), padding=[10, 4]) 
        notebook = ttk.Notebook(self, style="Prog.TNotebook") 
        notebook.pack(fill="both", expand=True, padx=8, pady=8) 
        
        # Tab 1: Intérprete y Ejecutor de Pseudocódigo 
        tab1 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab1, text="💻 Intérprete de Pseudocódigo") 
        self._build_tab_interprete(tab1, panel_bg, fg_main, accent) 
        
        # Tab 2: Diagramador de Flujo de Datos 
        tab2 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab2, text="📐 Diagrama de Flujo") 
        self._build_tab_diagrama(tab2, panel_bg, fg_main, accent) 
        
        # Tab 3: Evaluador de Lógica & Tablas de Verdad 
        tab3 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab3, text="🔣 Tablas de Verdad") 
        self._build_tab_logica(tab3, panel_bg, fg_main, accent) 
        
        # Tab 4: Glosario de Programación 
        tab4 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8) 
        notebook.add(tab4, text="📚 Glosario de Lógica") 
        self._build_tab_glosario(tab4, panel_bg, fg_main, accent) 
        
    # --- TAB 1: INTÉRPRETE DE PSEUDOCÓDIGO --- 
    def _build_tab_interprete(self, parent, panel_bg, fg_main, accent): 
        pnl_code = PanelBase(parent, titulo="💻 Editor de Pseudocódigo (PSeInt / Algorítmico)", bg_color=panel_bg) 
        pnl_code.pack(fill="x", pady=(0, 6)) 
        self.txt_codigo = tk.Text(pnl_code, height=6, font=("Consolas", 9), bg="#ffffff", bd=1, relief="solid", wrap="word") 
        self.txt_codigo.pack(fill="x", pady=4) 
        codigo_ejemplo = ( "// Ejemplo: Algoritmo de Cálculo de Promedio y Estado\n" "a = 8\n" "b = 9\n" "promedio = (a + b) / 2\n" "ESCRIBIR \"Calculando promedio...\"\n" "ESCRIBIR promedio\n" "SI promedio &gt;= 7 ENTONCES\n" " ESCRIBIR \"Estado: APROBADO\"\n" "FINSI" ) 
        
        self.txt_codigo.insert("1.0", codigo_ejemplo) 
        btn_run = tk.Button( pnl_code, text="▶️ Ejecutar Pseudocódigo Paso a Paso", command=self._ejecutar_codigo, bg="#28a745", fg="#ffffff", font=("Arial", 8, "bold"), relief="groove", cursor="hand2" ) 
        btn_run.pack(fill="x", pady=2) 
        
        pnl_out = PanelBase(parent, titulo="🖥️ Consola de Salida y Traza de Variables", bg_color=panel_bg) 
        pnl_out.pack(fill="both", expand=True) 
        
        self.txt_consola = tk.Text(pnl_out, font=("Consolas", 8), bg="#0f172a", fg="#38bdf8", bd=1, relief="solid", wrap="word") 
        self.txt_consola.pack(fill="both", expand=True, padx=2, pady=2) 
        
    def _ejecutar_codigo(self): 
        code_str = self.txt_codigo.get("1.0", tk.END).strip() 
        self.txt_consola.delete("1.0", tk.END) 
        
        res = interpretar_pseudocodigo(code_str) 
        if "error" in res: 
            self.txt_consola.insert(tk.END, f"⚠️ {res['error']}\n") 
            return 
    
        self.txt_consola.insert(tk.END, "🖥️ CONSOLA DE SALIDA:\n")
        self.txt_consola.insert(tk.END, "--------------------------------------------------\n")
        salida = res.get("consola_salida", []) if isinstance(res, dict) else []
        for line in salida:
            self.txt_consola.insert(tk.END, f"► {line}\n")

        self.txt_consola.insert(tk.END, "\n📊 TABLA DE VARIABLES FINALES:\n")
        self.txt_consola.insert(tk.END, "--------------------------------------------------\n")
        variables_finales = res.get("variables_finales", {}) if isinstance(res, dict) else {}
        if isinstance(variables_finales, dict):
            for k, v in variables_finales.items():
                self.txt_consola.insert(tk.END, f" • {k} = {v}\n")

        self.txt_consola.insert(tk.END, "\n🔍 TRAZA DE EJECUCIÓN PASO A PASO:\n")
        self.txt_consola.insert(tk.END, "--------------------------------------------------\n")
        traza = res.get("traza_paso_a_paso", []) if isinstance(res, dict) else []
        for paso in traza:
            if not isinstance(paso, dict):
                continue
            linea_num = paso.get("linea_num", "?")
            instruccion = paso.get("instruccion", "")
            accion = paso.get("accion", "")
            self.txt_consola.insert(tk.END, f"Línea {linea_num}: {instruccion} ──► {accion}\n")
        
    # --- TAB 2: DIAGRAMADOR DE FLUJO --- 
    def _build_tab_diagrama(self, parent, panel_bg, fg_main, accent): 
        pnl_diag = PanelBase(parent, titulo="📐 Generador de Diagrama de Flujo de Datos (Flowchart)", bg_color=panel_bg) 
        pnl_diag.pack(fill="both", expand=True) 

        self.txt_codigo_diagrama = tk.Text(pnl_diag, height=6, font=("Consolas", 9), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_codigo_diagrama.pack(fill="x", pady=(0, 6))
        ejemplo_dig = (
            "INICIO\n"
            "LEER numero\n"
            "SI numero >= 10 ENTONCES\n"
            "    ESCRIBIR \"Aprobado\"\n"
            "SINO\n"
            "    ESCRIBIR \"Reprobado\"\n"
            "FIN SI\n"
            "FIN"
        )
        self.txt_codigo_diagrama.insert("1.0", ejemplo_dig)

        btn_gen_diag = tk.Button( pnl_diag, text="📐 Convertir Pseudocódigo a Diagrama de Flujo", command=self._generar_diagrama, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove", cursor="hand2" ) 
        btn_gen_diag.pack(fill="x", pady=4) 

        self.txt_res_diag = tk.Text(pnl_diag, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid", wrap="word") 
        self.txt_res_diag.pack(fill="both", expand=True, padx=4, pady=4) 

        self._generar_diagrama() 

    def _generar_diagrama(self): 
        if hasattr(self, "txt_codigo_diagrama") and self.txt_codigo_diagrama is not None:
            code_str = self.txt_codigo_diagrama.get("1.0", tk.END).strip()
        else:
            code_str = self.txt_codigo.get("1.0", tk.END).strip()
        self.txt_res_diag.delete("1.0", tk.END) 
        
        res = generar_diagrama_flujo(code_str)
        nodos = res.get("diagrama_nodos", []) if isinstance(res, dict) else []
        total_nodos = res.get("total_nodos", 0) if isinstance(res, dict) else 0

        self.txt_res_diag.insert(tk.END, f"📐 DIAGRAMA DE FLUJO DE DATOS ({total_nodos} NODOS):\n\n")

        for nodo in nodos:
            if not isinstance(nodo, dict):
                continue
            sub_icon = nodo.get('icono', '')
            tipo_str = str(nodo.get('tipo', '')).upper()
            linea = f" [{nodo.get('id', 0)}] {sub_icon} ({tipo_str}): {nodo.get('texto', '')}\n"
            self.txt_res_diag.insert(tk.END, linea)
            if int(nodo.get('id', 0)) < total_nodos:
                self.txt_res_diag.insert(tk.END, " │\n ▼\n")
                
    # --- TAB 3: TABLAS DE VERDAD --- 
    def _build_tab_logica(self, parent, panel_bg, fg_main, accent): 
        pnl_log = PanelBase(parent, titulo="🔣 Evaluador de Tablas de Verdad &amp; Lógica Proposicional", bg_color=panel_bg) 
        pnl_log.pack(fill="x", pady=(0, 6)) 
        
        f_l = tk.Frame(pnl_log, bg=panel_bg) 
        f_l.pack(fill="x", pady=2) 
        
        tk.Label(f_l, text="Expresión Lógica (con A, B): ", font=("Arial", 8, "bold"), bg=panel_bg).pack(side="left") 
        self.e_expr_log = tk.Entry(f_l, width=30) 
        self.e_expr_log.pack(side="left", padx=6) 
        self.e_expr_log.insert(0, "A AND (B OR NOT A)") 
        
        btn_tv = tk.Button( pnl_log, text="🔣 Generar Tabla de Verdad Completa", command=self._calc_tabla_verdad, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove", cursor="hand2" ) 
        btn_tv.pack(fill="x", pady=4) 
        
        pnl_tv_res = PanelBase(parent, titulo="📊 Matriz de Verdad (2^N Combinaciones)", bg_color=panel_bg) 
        pnl_tv_res.pack(fill="both", expand=True) 
        
        self.txt_res_tv = tk.Text(pnl_tv_res, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid", wrap="word") 
        self.txt_res_tv.pack(fill="both", expand=True, padx=2, pady=2) 
        self._calc_tabla_verdad() 
        
    def _calc_tabla_verdad(self): 
        expr = self.e_expr_log.get().strip() 
        self.txt_res_tv.delete("1.0", tk.END) 
        
        res = generar_tabla_verdad(expr) 
        
        self.txt_res_tv.insert(tk.END, f"🔣 TABLA DE VERDAD PARA: {res['expresion']}\n\n")
        header = " | ".join([f"{v:<6}" for v in res["variables"]]) + " | RESULTADO FINAL\n"
        self.txt_res_tv.insert(tk.END, header)
        self.txt_res_tv.insert(tk.END, "-" * 50 + "\n") 
        
        for fila in res["filas_tabla"]: 
            row_str = " | ".join([f"{fila[v]:<6}" for v in res["variables"]]) + f" | {fila['RESULTADO']}\n" 
            self.txt_res_tv.insert(tk.END, row_str) 
            
    # --- TAB 4: GLOSARIO --- 
    def _build_tab_glosario(self, parent, panel_bg, fg_main, accent): 
        self.glosario_ui = GlosarioCentralUI(
            parent,
            titulo="📚 Glosario de Fundamentos de Programación y Algoritmos",
            data_path=Path(__file__).resolve().parents[4] / "persistance" / "glosario_programacion.json",
        )
        self.glosario_ui.entries = [
            {
                "nombre": term,
                "categorias": ["Programación", "Lógica"],
                "subcategorias": ["Concepto"],
                "contenido": defn,
            }
            for term, defn in DICCIONARIO_PROGRAMACION.items()
        ] + list(getattr(self.glosario_ui, "entries", []))
        if hasattr(self.glosario_ui, "_aplicar_filtro"):
            self.glosario_ui._aplicar_filtro()