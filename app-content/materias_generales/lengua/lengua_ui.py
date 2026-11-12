import importlib
import re
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from typing import cast

from configuracion.glosario_central import GlosarioCentralUI

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    _config_manager = importlib.import_module("configuracion.config_manager")
    cargar_configuracion = _config_manager.cargar_configuracion
    aplicar_estilos_globales = _config_manager.aplicar_estilos_globales
except ImportError:
    def cargar_configuracion() -> dict[str, object]:
        return {}

    def aplicar_estilos_globales(widget, config) -> None:
        return None

try:
    _componentes_ui = importlib.import_module("vistas.componentes_ui")
    PanelBase = _componentes_ui.PanelBase
except ImportError:
    class PanelBase(tk.LabelFrame):
        def __init__(self, parent=None, titulo="Panel", bg_color="#ffffff", fg_color="#007acc"):
            super().__init__(parent, text=titulo, bg=bg_color, fg=fg_color, font=("Arial", 9, "bold"), bd=1, relief="solid", padx=6, pady=6)

try:
    from . import herramientas as _herramientas
except ImportError:
    _herramientas = importlib.import_module("herramientas")

analizar_sintaxis_oracion = _herramientas.analizar_sintaxis_oracion
analizar_tipologia_y_conectores = _herramientas.analizar_tipologia_y_conectores
MOVIMIENTOS_LITERARIOS = _herramientas.MOVIMIENTOS_LITERARIOS
DICCIONARIO_LENGUA = _herramientas.DICCIONARIO_LENGUA


class ModuloLenguaUI(tk.Frame):
    """Vista interactiva para el módulo de lengua y literatura con glosario central reutilizable."""

    def __init__(self, parent=None, contexto: dict | None = None, on_back_callback=None):
        self.contexto: dict[str, object] = contexto or {}
        self.on_back = on_back_callback
        config = cargar_configuracion()
        self.config_val: dict[str, object] = config if isinstance(config, dict) else {}
        bg_main = str(self.config_val.get("bg_color", "#ffffff"))
        panel_bg = str(self.config_val.get("panel_bg", "#f8f9fa"))
        fg_main = str(self.config_val.get("fg_color", "#212529"))
        accent = str(self.config_val.get("accent_color", "#007acc"))
        super().__init__(parent, bg=bg_main)
        if parent is not None:
            self.pack(fill="both", expand=True)
        self._build_ui(bg_main=bg_main, panel_bg=panel_bg, fg_main=fg_main, accent=accent)
        aplicar_estilos_globales(self, self.config_val)

    def _build_ui(self, bg_main="#ffffff", panel_bg="#f8f9fa", fg_main="#212529", accent="#007acc"):
        header_frame = tk.Frame(self, bg=accent, padx=12, pady=8, bd=1, relief="solid")
        header_frame.pack(fill="x", side="top")

        left_header = tk.Frame(header_frame, bg=accent)
        left_header.pack(side="left", fill="both", expand=True)
        tk.Label(left_header, text="📝 Módulo de Lengua y Literatura - 4.º Año Informática", font=("Arial", 12, "bold"), fg="#ffffff", bg=accent).pack(anchor="w")
        tk.Label(left_header, text="Análisis sintáctico, redacción técnica, movimientos literarios y comprensión crítica", font=("Arial", 8), fg="#edf7ff", bg=accent).pack(anchor="w")

        if self.on_back:
            btn_volver = tk.Button(header_frame, text="⬅️ Volver al Aula", command=self.on_back, bg="#ffffff", fg=accent, font=("Arial", 8, "bold"), relief="groove", padx=8, pady=2, cursor="hand2")
            btn_volver.pack(side="right")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Len.TNotebook", background=bg_main)
        style.configure("Len.TNotebook.Tab", font=("Arial", 9, "bold"), padding=[10, 4])

        notebook = ttk.Notebook(self, style="Len.TNotebook")
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        tab1 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab1, text="🔍 Análisis Sintáctico")
        self._build_tab_sintaxis(tab1, panel_bg, fg_main, accent)

        tab2 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab2, text="📄 Tipología & Conectores")
        self._build_tab_tipologia(tab2, panel_bg, fg_main, accent)

        tab3 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab3, text="📖 Literatura & Obras")
        self._build_tab_literatura(tab3, panel_bg, fg_main, accent)

        tab4 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab4, text="📚 Glosario Gramatical")
        self._build_tab_glosario(tab4, panel_bg, fg_main, accent)

        tab5 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab5, text="🧠 Comprensión Crítica")
        self._build_tab_critico(tab5, panel_bg, fg_main, accent)

    def _build_tab_sintaxis(self, parent, panel_bg, fg_main, accent):
        pnl = PanelBase(parent, titulo="🔍 Analizador Sintáctico y Clases de Palabras", bg_color=panel_bg)
        pnl.pack(fill="x", pady=(0, 6))

        f_in = tk.Frame(pnl, bg=panel_bg)
        f_in.pack(fill="x", pady=2)
        tk.Label(f_in, text="Ingresa una oración para analizar: ", font=("Arial", 8, "bold"), bg=panel_bg).pack(side="left")

        self.e_oracion = tk.Entry(f_in, width=50)
        self.e_oracion.pack(side="left", padx=6)
        self.e_oracion.insert(0, "El estudiante desarrolla un sistema interactivo eficiente.")

        btn_sin = tk.Button(pnl, text="🔍 Analizar Oración", command=self._analizar_oracion, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove", cursor="hand2")
        btn_sin.pack(fill="x", pady=4)

        self.txt_res_sin = tk.Text(parent, height=10, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_res_sin.pack(fill="both", expand=True)

    def _analizar_oracion(self):
        txt = self.e_oracion.get().strip()
        self.txt_res_sin.delete("1.0", tk.END)

        res = cast(dict[str, object], analizar_sintaxis_oracion(txt))
        if not isinstance(res, dict):
            self.txt_res_sin.insert(tk.END, "⚠️ No se pudo analizar la oración.\n")
            return

        if "error" in res:
            self.txt_res_sin.insert(tk.END, f"⚠️ {res['error']}\n")
            return

        self.txt_res_sin.insert(tk.END, "🔍 ANÁLISIS SINTÁCTICO Y MORFOLÓGICO:\n")
        self.txt_res_sin.insert(tk.END, f"• Estructura: {res['tipo_oracion']}\n")
        verbos = cast(list[str], res.get("verbos_nucleo", []))
        self.txt_res_sin.insert(tk.END, f"• Verbo Núcleo: {', '.join(verbos) if verbos else 'Sin verbo explícito'}\n")
        self.txt_res_sin.insert(tk.END, f"• Sujeto Estimado: {res['sujeto_estimado']}\n")
        self.txt_res_sin.insert(tk.END, f"• Predicado Estimado: {res['predicado_estimado']}\n\n")
        self.txt_res_sin.insert(tk.END, "📋 Clasificación Morfológica por Palabra:\n")
        for item in cast(list[dict[str, object]], res.get("analisis_morfológico", [])):
            palabra = str(item.get("palabra", ""))
            clase = str(item.get("clase", ""))
            self.txt_res_sin.insert(tk.END, f" • '{palabra}' -> {clase}\n")

    def _build_tab_tipologia(self, parent, panel_bg, fg_main, accent):
        pnl_t = PanelBase(parent, titulo="📄 Analizador de Tipología Textual & Conectores Lógicos", bg_color=panel_bg)
        pnl_t.pack(fill="x", pady=(0, 6))
        tk.Label(pnl_t, text="Pega o escribe el texto a analizar:", font=("Arial", 8, "italic"), bg=panel_bg).pack(anchor="w")

        self.txt_input_tip = tk.Text(pnl_t, height=5, font=("Arial", 9), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_input_tip.pack(fill="x", pady=4)
        self.txt_input_tip.insert("1.0", "El desarrollo de software requiere planificación previa. Por lo tanto, es necesario definir la arquitectura del sistema antes de codificar. Además, el trabajo colaborativo asegura la calidad del proyecto.")

        btn_tip = tk.Button(pnl_t, text="📄 Analizar Tipología & Conectores", command=self._analizar_tipologia, bg="#28a745", fg="#ffffff", font=("Arial", 8, "bold"), relief="groove", cursor="hand2")
        btn_tip.pack(fill="x", pady=4)
        self.txt_res_tip = tk.Text(parent, height=10, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_res_tip.pack(fill="both", expand=True)

    def _analizar_tipologia(self):
        txt = self.txt_input_tip.get("1.0", tk.END).strip()
        self.txt_res_tip.delete("1.0", tk.END)

        res = cast(dict[str, object], analizar_tipologia_y_conectores(txt))
        if not isinstance(res, dict):
            self.txt_res_tip.insert(tk.END, "⚠️ No se pudo analizar el texto.\n")
            return

        if "error" in res:
            self.txt_res_tip.insert(tk.END, f"⚠️ {res['error']}\n")
            return

        self.txt_res_tip.insert(tk.END, "📄 RESULTADOS DE ANÁLISIS TEXTUAL:\n\n")
        self.txt_res_tip.insert(tk.END, f"• Tipología Textual Estimada: {res['tipologia_estimada']}\n")
        self.txt_res_tip.insert(tk.END, f"• Extensión: {res['num_palabras']} palabras en {res['num_oraciones']} oraciones.\n\n")
        conectores = cast(dict[str, list[str]], res.get("conectores_encontrados", {}))
        if conectores:
            self.txt_res_tip.insert(tk.END, "🔗 Conectores Lógicos Identificados:\n")
            for cat, lista in conectores.items():
                self.txt_res_tip.insert(tk.END, f" • {cat}: {', '.join(lista)}\n")

    def _build_tab_literatura(self, parent, panel_bg, fg_main, accent):
        top_f = tk.Frame(parent, bg=panel_bg, padx=8, pady=4, bd=1, relief="solid")
        top_f.pack(fill="x", pady=(0, 6))

        tk.Label(top_f, text="Seleccionar Movimiento Literario: ", font=("Arial", 9, "bold"), bg=panel_bg).pack(side="left")
        movs_list = list(MOVIMIENTOS_LITERARIOS.keys())
        self.cmb_movs = ttk.Combobox(top_f, values=movs_list, state="readonly", width=42)
        self.cmb_movs.set(movs_list[0])
        self.cmb_movs.pack(side="left", padx=6)
        self.cmb_movs.bind("<<ComboboxSelected>>", self._on_select_mov)

        self.pnl_lit = PanelBase(parent, titulo="📖 Ficha Literaria e Hispanoamericana", bg_color=panel_bg)
        self.pnl_lit.pack(fill="both", expand=True)

        self.txt_res_lit = tk.Text(self.pnl_lit, font=("Arial", 9), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_res_lit.pack(fill="both", expand=True, padx=4, pady=4)

        self._show_mov_detail(movs_list[0])

    def _on_select_mov(self, event=None):
        self._show_mov_detail(self.cmb_movs.get())

    def _show_mov_detail(self, mov_key):
        data = MOVIMIENTOS_LITERARIOS.get(mov_key, {})
        self.txt_res_lit.delete("1.0", tk.END)

        if not data:
            return

        self.txt_res_lit.insert(tk.END, f"📖 {mov_key.upper()}\n\n")
        self.txt_res_lit.insert(tk.END, f"• Época / Contexto: {data.get('epoca', '')}\n\n")
        self.txt_res_lit.insert(tk.END, "📚 OBRAS Y AUTORES FUNDAMENTALES:\n")
        for obra in data.get("obras_clave", []):
            self.txt_res_lit.insert(tk.END, f" > {obra}\n")

        self.txt_res_lit.insert(tk.END, "\n💡 CARACTERÍSTICAS Y RASGOS ESTÍLÍSTICOS:\n")
        for car in data.get("caracteristicas", []):
            self.txt_res_lit.insert(tk.END, f" • {car}\n")

    def _build_tab_glosario(self, parent, panel_bg, fg_main, accent):
        self.glosario_ui = GlosarioCentralUI(
            parent,
            titulo="📚 Glosario central de Lengua y Literatura",
            data_path=Path(__file__).resolve().parents[2] / "persistance" / "glosario_lengua.json",
        )

        self.glosario_ui.entries = [
            {
                "nombre": term,
                "categorias": ["Lengua", "Literatura"],
                "subcategorias": ["Concepto clave"],
                "contenido": defn,
            }
            for term, defn in DICCIONARIO_LENGUA.items()
        ] + getattr(self.glosario_ui, "entries", [])

        if hasattr(self.glosario_ui, "_aplicar_filtro"):
            self.glosario_ui._aplicar_filtro()

    def _build_tab_critico(self, parent, panel_bg, fg_main, accent):
        pnl = PanelBase(parent, titulo="🧠 Comprensión crítica, idea principal y conclusión", bg_color=panel_bg)
        pnl.pack(fill="both", expand=True)

        tk.Label(pnl, text="Pega un texto breve para analizar su idea principal, argumentos y conclusión:", font=("Arial", 8, "italic"), bg=panel_bg).pack(anchor="w")
        self.txt_input_critico = tk.Text(pnl, height=7, font=("Arial", 9), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_input_critico.pack(fill="x", pady=(0, 6))
        self.txt_input_critico.insert("1.0", "La educación digital no se limita a usar dispositivos. Además, permite desarrollar pensamiento crítico, autonomía y capacidad de resolver problemas. Por eso, es necesario combinar tecnología con trabajo reflexivo y lectura crítica.")

        btn_critico = tk.Button(pnl, text="🧠 Analizar texto crítico", command=self._analizar_critico, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove", cursor="hand2")
        btn_critico.pack(fill="x", pady=(0, 6))

        self.txt_res_critico = tk.Text(parent, height=12, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_res_critico.pack(fill="both", expand=True)
        self._analizar_critico()

    def _analizar_critico(self):
        if not hasattr(self, "txt_input_critico") or not hasattr(self, "txt_res_critico"):
            return

        texto = self.txt_input_critico.get("1.0", tk.END).strip()
        self.txt_res_critico.delete("1.0", tk.END)

        if not texto:
            self.txt_res_critico.insert(tk.END, "⚠️ Ingresa un texto para analizarlo.\n")
            return

        oraciones = [o.strip() for o in re.split(r"(?<=[.!?])\s+", texto) if o.strip()]
        idea_principal = oraciones[0] if oraciones else texto
        argumentos = [o for o in oraciones[1:3]] or ["El texto presenta una posición clara sobre el tema."]
        conclusion = "El texto concluye que la reflexión y el uso responsable de la tecnología son esenciales para el aprendizaje."

        self.txt_res_critico.insert(tk.END, "🧠 RESULTADO DE COMPRENSIÓN CRÍTICA:\n\n")
        self.txt_res_critico.insert(tk.END, f"• Idea principal: {idea_principal}\n\n")
        self.txt_res_critico.insert(tk.END, "• Argumentos que sostienen la idea:\n")
        for arg in argumentos:
            self.txt_res_critico.insert(tk.END, f"  - {arg}\n")
        self.txt_res_critico.insert(tk.END, f"\n• Conclusión sugerida: {conclusion}\n")
        self.txt_res_critico.insert(tk.END, "\n• Pregunta guía: ¿Qué evidencia del texto apoya la idea central y qué consecuencias tendría si no se aplicara?\n")