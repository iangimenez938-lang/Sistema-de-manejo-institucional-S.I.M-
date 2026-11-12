import importlib
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Any
from pathlib import Path

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

    def aplicar_estilos_globales(root, config) -> None:
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

analizar_sistema_tecnologico = _herramientas.analizar_sistema_tecnologico
ETAPAS_PROYECTO_TECNOLOGICO = _herramientas.ETAPAS_PROYECTO_TECNOLOGICO
calcular_presupuesto_proyecto_tec = _herramientas.calcular_presupuesto_proyecto_tec
MATRIZ_IMPACTO_TECNOLOGICO = _herramientas.MATRIZ_IMPACTO_TECNOLOGICO
DICCIONARIO_TECNOLOGIA = _herramientas.DICCIONARIO_TECNOLOGIA


class ModuloTecnologiaUI(tk.Frame):
    """Vista interactiva para el módulo de tecnología."""

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
        self.pack(fill="both", expand=True)
        self._build_ui(bg_main=bg_main, panel_bg=panel_bg, fg_main=fg_main, accent=accent)
        aplicar_estilos_globales(self, self.config_val)

    def _build_ui(self, bg_main="#ffffff", panel_bg="#f8f9fa", fg_main="#212529", accent="#007acc"):
        header_frame = tk.Frame(self, bg=accent, padx=12, pady=8, bd=1, relief="solid")
        header_frame.pack(fill="x", side="top")

        left_header = tk.Frame(header_frame, bg=accent)
        left_header.pack(side="left", fill="both", expand=True)
        tk.Label(left_header, text="⚙️ Módulo de Tecnología & Procesos Tecnológicos - 4.º Año Informática", font=("Arial", 12, "bold"), fg="#ffffff", bg=accent).pack(anchor="w")
        tk.Label(left_header, text="Enfoque Sistémico, Fases del Proyecto Tecnológico, Presupuestos e Impacto Ambiental", font=("Arial", 8), fg="#edf7ff", bg=accent).pack(anchor="w")

        if self.on_back:
            btn_volver = tk.Button(header_frame, text="⬅️ Volver al Aula", command=self.on_back, bg="#ffffff", fg=accent, font=("Arial", 8, "bold"), relief="groove", padx=8, pady=2, cursor="hand2")
            btn_volver.pack(side="right")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Tec.TNotebook", background=bg_main)
        style.configure("Tec.TNotebook.Tab", font=("Arial", 9, "bold"), padding=[10, 4])
        notebook = ttk.Notebook(self, style="Tec.TNotebook")
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        tab1 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab1, text="⚙️ Análisis Sistémico")
        self._build_tab_sistemico(tab1, panel_bg, fg_main, accent)

        tab2 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab2, text="🛠️ Proyecto Tecnológico")
        self._build_tab_proyecto(tab2, panel_bg, fg_main, accent)

        tab3 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab3, text="🌱 Impacto Ambiental & E-Waste")
        self._build_tab_impacto(tab3, panel_bg, fg_main, accent)

        tab4 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab4, text="📚 Glosario Tecnológico")
        self._build_tab_glosario(tab4, panel_bg, fg_main, accent)

    def _font_default(self):
        return ("Arial", max(9, int(self.config_val.get("font_size", 10))))

    def _build_tab_sistemico(self, parent, panel_bg, fg_main, accent):
        pnl = PanelBase(parent, titulo="⚙️ Modelado de Sistemas Tecnológicos (Materia, Energía e Información)", bg_color=panel_bg)
        pnl.pack(fill="x", pady=(0, 6))

        f_in = tk.Frame(pnl, bg=panel_bg)
        f_in.pack(fill="x", pady=2)
        tk.Label(f_in, text="Nombre del Sistema: ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=0, sticky="w")

        self.e_sys = tk.Entry(f_in, width=20)
        self.e_sys.grid(row=0, column=1, padx=4)
        self.e_sys.insert(0, "Impresora 3D")

        tk.Label(f_in, text="Entrada Materia: ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=2, sticky="w")
        self.e_mat = tk.Entry(f_in, width=20)
        self.e_mat.grid(row=0, column=3, padx=4)
        self.e_mat.insert(0, "Filamento PLA / Plástico")

        tk.Label(f_in, text="Entrada Energía: ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=1, column=0, sticky="w", pady=4)
        self.e_ene = tk.Entry(f_in, width=20)
        self.e_ene.grid(row=1, column=1, padx=4, pady=4)
        self.e_ene.insert(0, "Energía Eléctrica 220V")

        tk.Label(f_in, text="Entrada Información: ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=1, column=2, sticky="w", pady=4)
        self.e_inf = tk.Entry(f_in, width=20)
        self.e_inf.grid(row=1, column=3, padx=4, pady=4)
        self.e_inf.insert(0, "Archivo G-Code / Diseño 3D")

        btn_sys = tk.Button(pnl, text="⚙️ Analizar Diagrama de Bloques del Sistema", command=self._analizar_sistema, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove", cursor="hand2")
        btn_sys.pack(fill="x", pady=4)

        self.txt_res_sys = tk.Text(parent, height=10, font=self._font_default(), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_res_sys.pack(fill="both", expand=True)

    def _analizar_sistema(self):
        sys_nom = self.e_sys.get().strip()
        mat = self.e_mat.get().strip()
        ene = self.e_ene.get().strip()
        inf = self.e_inf.get().strip()
        self.txt_res_sys.delete("1.0", tk.END)

        res: dict[str, Any] = analizar_sistema_tecnologico(sys_nom, mat, ene, inf, "Extrusión y fundición capa por capa")
        if "error" in res:
            self.txt_res_sys.insert(tk.END, f"⚠️ {res['error']}\n")
            return

        entradas = res.get("entradas", {})
        salidas = res.get("salidas", {})

        if not isinstance(entradas, dict) or not isinstance(salidas, dict):
            self.txt_res_sys.insert(tk.END, "⚠️ No se pudo interpretar la estructura del sistema tecnológico.\n")
            return

        self.txt_res_sys.insert(tk.END, f"⚙️ MODELO SISTÉMICO: {str(res.get('sistema', '')).upper()}\n\n")
        self.txt_res_sys.insert(tk.END, "📥 ENTRADAS AL SISTEMA:\n")
        self.txt_res_sys.insert(tk.END, f" • Materia: {entradas.get('materia', '')}\n")
        self.txt_res_sys.insert(tk.END, f" • Energía: {entradas.get('energia', '')}\n")
        self.txt_res_sys.insert(tk.END, f" • Información: {entradas.get('informacion', '')}\n\n")
        self.txt_res_sys.insert(tk.END, f"⚙️ PROCESO DE TRANSFORMACIÓN:\n > {res.get('proceso', '')}\n\n")
        self.txt_res_sys.insert(tk.END, "📤 SALIDAS GENERADAS:\n")
        self.txt_res_sys.insert(tk.END, f" • Materia: {salidas.get('materia', '')}\n")
        self.txt_res_sys.insert(tk.END, f" • Energía: {salidas.get('energia', '')}\n")
        self.txt_res_sys.insert(tk.END, f" • Información: {salidas.get('informacion', '')}\n\n")
        self.txt_res_sys.insert(tk.END, f"🔄 CONTROL Y REALIMENTACIÓN (FEEDBACK):\n > {res.get('realimentacion_feedback', '')}\n")

    def _build_tab_proyecto(self, parent, panel_bg, fg_main, accent):
        pnl_e = PanelBase(parent, titulo="🛠️ Fases Etapas del Proyecto Tecnológico", bg_color=panel_bg)
        pnl_e.pack(fill="x", pady=(0, 6))

        btn_ver_e = tk.Button(pnl_e, text="📋 Ver Etapas y Entregables del Proyecto Escolar", command=self._mostrar_etapas, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove")
        btn_ver_e.pack(fill="x", pady=2)

        pnl_p = PanelBase(parent, titulo="🧮 Calculadora de Presupuesto del Proyecto", bg_color=panel_bg)
        pnl_p.pack(fill="x", pady=(0, 6))

        f_p = tk.Frame(pnl_p, bg=panel_bg)
        f_p.pack(fill="x", pady=2)

        tk.Label(f_p, text="Horas de Desarrollo: ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=0)
        self.e_hrs = tk.Entry(f_p, width=8, justify="center")
        self.e_hrs.grid(row=0, column=1)
        self.e_hrs.insert(0, "40")

        tk.Label(f_p, text="Costo por Hora ($): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=2)
        self.e_chrs = tk.Entry(f_p, width=8, justify="center")
        self.e_chrs.grid(row=0, column=3)
        self.e_chrs.insert(0, "1500")

        tk.Label(f_p, text="Costo Insumos / Componentes ($): ", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=4)
        self.e_ins = tk.Entry(f_p, width=10, justify="center")
        self.e_ins.grid(row=0, column=5)
        self.e_ins.insert(0, "25000")

        btn_calc_p = tk.Button(pnl_p, text="🧮 Calcular Costo Total y Contingencia", command=self._calc_presupuesto, bg="#28a745", fg="#ffffff", font=("Arial", 8, "bold"), relief="groove")
        btn_calc_p.pack(fill="x", pady=4)

        self.txt_res_proy = tk.Text(parent, height=8, font=self._font_default(), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_res_proy.pack(fill="both", expand=True)
        self._mostrar_etapas()

    def _mostrar_etapas(self):
        if not hasattr(self, "txt_res_proy"):
            return
        self.txt_res_proy.delete("1.0", tk.END)
        self.txt_res_proy.insert(tk.END, "🛠️ GUÍA DE ETAPAS DEL PROYECTO TECNOLÓGICO:\n\n")
        for etapa in ETAPAS_PROYECTO_TECNOLOGICO:
            self.txt_res_proy.insert(tk.END, f"📌 {etapa['etapa'].upper()}\n")
            self.txt_res_proy.insert(tk.END, f" • Descripción: {etapa['descripcion']}\n")
            self.txt_res_proy.insert(tk.END, f" • Entregable: {etapa['entregable']}\n\n")

    def _calc_presupuesto(self):
        self.txt_res_proy.delete("1.0", tk.END)
        try:
            hrs = float(self.e_hrs.get())
            chrs = float(self.e_chrs.get())
            ins = float(self.e_ins.get())

            items = [{"item": "Componentes y Materiales", "costo": ins}]
            res = calcular_presupuesto_proyecto_tec(items, hrs, chrs)

            self.txt_res_proy.insert(tk.END, "🧮 PRESUPUESTO DEL PROYECTO TECNOLÓGICO:\n\n")
            self.txt_res_proy.insert(tk.END, f"• Costo de Materiales/Insumos: ${res['costo_materiales_componentes']}\n")
            self.txt_res_proy.insert(tk.END, f"• Costo Mano de Obra ({hrs}hs x ${chrs}): ${res['costo_mano_obra_desarrollo']}\n")
            self.txt_res_proy.insert(tk.END, f"• Subtotal Proyecto: ${res['subtotal']}\n")
            self.txt_res_proy.insert(tk.END, f"• Contingencia de Imprevistos (10%): ${res['contingencia_10pct']}\n")
            self.txt_res_proy.insert(tk.END, "--------------------------------------------------\n")
            self.txt_res_proy.insert(tk.END, f"💰 COSTO TOTAL DEL PROYECTO: ${res['costo_total_proyecto']} ARS\n")
        except Exception:
            messagebox.showerror("Error", "Ingresa números válidos.")

    def _build_tab_impacto(self, parent, panel_bg, fg_main, accent):
        pnl_imp = PanelBase(parent, titulo="🌱 Matriz de Impacto Ambiental, Obsolescencia y E-Waste", bg_color=panel_bg)
        pnl_imp.pack(fill="both", expand=True)

        self.txt_res_imp = tk.Text(pnl_imp, font=self._font_default(), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_res_imp.pack(fill="both", expand=True, padx=4, pady=4)
        self.txt_res_imp.insert(tk.END, "🌱 ANÁLISIS DE SUSTENTABILIDAD Y TECNOLOGÍA:\n\n")

        for tema, info in MATRIZ_IMPACTO_TECNOLOGICO.items():
            self.txt_res_imp.insert(tk.END, f"📌 {tema.upper()}:\n")
            self.txt_res_imp.insert(tk.END, f" • Definición: {info['definicion']}\n")
            self.txt_res_imp.insert(tk.END, f" ⚠️ Impacto Ambiental: {info['impacto_ambiental']}\n")
            self.txt_res_imp.insert(tk.END, f" 🌱 Alternativa Sostenible: {info['alternativa_sostenible']}\n\n")

    def _build_tab_glosario(self, parent, panel_bg, fg_main, accent):
        self.glosario_ui = GlosarioCentralUI(
            parent,
            titulo="📚 Glosario central de Tecnología",
            data_path=Path(__file__).resolve().parents[2] / "persistance" / "glosario_central.json",
        )

        if hasattr(self.glosario_ui, "entries"):
            self.glosario_ui.entries = [
                {
                    "nombre": term,
                    "categorias": ["Tecnología"],
                    "subcategorias": ["Texto explicativo"],
                    "contenido": defn,
                }
                for term, defn in DICCIONARIO_TECNOLOGIA.items()
            ] + self.glosario_ui.entries

        self.txt_glosario_t = getattr(self.glosario_ui, "form_contenido", None)
        if hasattr(self.glosario_ui, "_aplicar_filtro"):
            self.glosario_ui._aplicar_filtro()

