import tkinter as tk 
from tkinter import ttk, messagebox 
import sys 
from pathlib import Path 
from typing import Any, cast

from configuracion.glosario_central import GlosarioCentralUI

BASE_DIR = Path(__file__).resolve().parent.parent.parent 
if str(BASE_DIR) not in sys.path: 
    sys.path.insert(0, str(BASE_DIR)) 

def cargar_configuracion() -> dict[str, Any]:
    try:
        from configuracion.config_manager import cargar_configuracion as _load_config
        return _load_config()
    except Exception:
        return {}


def aplicar_estilos_globales(widget: Any, config: dict[str, Any]) -> None:
    try:
        from configuracion.config_manager import aplicar_estilos_globales as _apply_styles
        _apply_styles(widget, config)
    except Exception:
        return None

class PanelBase(tk.LabelFrame):
    def __init__(self, parent=None, titulo="Panel", bg_color="#ffffff", fg_color="#007acc"):
        super().__init__(parent, text=titulo, bg=bg_color, fg=fg_color, font=("Arial", 9, "bold"), bd=1, relief="solid", padx=6, pady=6)

from .herramientas import ( TECHNICAL_GLOSSARY_IT, FALSE_FRIENDS_IT, analyze_technical_text_english ) 

class ModuloInglesUI(tk.Frame): 
    """Vista interactiva para el módulo de inglés técnico con glosario central reutilizable."""

    def __init__(self, parent=None, contexto: dict[str, Any] | None = None, on_back_callback=None): 
        self.contexto = contexto or {}
        self.on_back = on_back_callback
        self.config_val = cargar_configuracion()
        self.cmb_terms = None
        self.pnl_term = None
        self.txt_res_term = None
        self.txt_input_doc = None
        self.txt_res_doc = None
        self.glosario_ui = None
        self.txt_practica = None
        self.txt_res_practica = None
        bg_main = self.config_val.get("bg_color", "#ffffff")
        panel_bg = self.config_val.get("panel_bg", "#f8f9fa")
        fg_main = self.config_val.get("fg_color", "#212529")
        accent = self.config_val.get("accent_color", "#007acc")
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
        tk.Label(left_header, text="🗣️ Módulo de Inglés Técnico - 4.º Año Informática", font=("Arial", 12, "bold"), fg="#ffffff", bg=accent).pack(anchor="w")
        tk.Label(left_header, text="Glosario, falsos amigos y práctica de documentación técnica", font=("Arial", 8), fg="#edf7ff", bg=accent).pack(anchor="w")

        if self.on_back:
            btn_volver = tk.Button(header_frame, text="⬅️ Volver al Aula", command=self.on_back, bg="#ffffff", fg=accent, font=("Arial", 8, "bold"), relief="groove", padx=8, pady=2, cursor="hand2")
            btn_volver.pack(side="right")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Ing.TNotebook", background=bg_main)
        style.configure("Ing.TNotebook.Tab", font=("Arial", 9, "bold"), padding=(8, 4))
        notebook = ttk.Notebook(self, style="Ing.TNotebook")
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        tab1 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab1, text="📚 Glosario IT & Falsos Amigos")
        self._build_tab_glosario(tab1, panel_bg, fg_main, accent)

        tab2 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab2, text="🗣️ Práctica rápida")
        self._build_tab_practica(tab2, panel_bg, fg_main, accent)

        tab3 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab3, text="📄 Analizador de Documentación")
        self._build_tab_analizador_doc(tab3, panel_bg, fg_main, accent)

    def _build_tab_glosario(self, parent, panel_bg, fg_main, accent):
        self.glosario_ui = GlosarioCentralUI(
            parent,
            titulo="📚 Glosario central de Inglés Técnico",
            data_path=Path(__file__).resolve().parents[2] / "persistance" / "glosario_ingles.json",
        )

        entries = [
            {
                "nombre": term,
                "categorias": ["IT", "Vocabulario"],
                "subcategorias": [info.get("category", "Técnica")],
                "contenido": f"Traducción: {info.get('translation', '')}.\n\nDefinición: {info.get('definition', '')}",
            }
            for term, info in TECHNICAL_GLOSSARY_IT.items()
        ]
        entries.extend([
            {
                "nombre": term,
                "categorias": ["False friend", "IT"],
                "subcategorias": ["Falsos amigos"],
                "contenido": f"Falsa traducción común: {info['false_translation']}\n\nSignificado real: {info['correct_meaning']}\n\nEjemplo: {info['example']}",
            }
            for term, info in FALSE_FRIENDS_IT.items()
        ])

        self.glosario_ui.entries = entries + getattr(self.glosario_ui, "entries", [])
        if hasattr(self.glosario_ui, "_aplicar_filtro"):
            self.glosario_ui._aplicar_filtro()

    def _build_tab_practica(self, parent, panel_bg, fg_main, accent):
        pnl = PanelBase(parent, titulo="🗣️ Práctica de vocabulario y frases técnicas", bg_color=panel_bg)
        pnl.pack(fill="both", expand=True)

        self.txt_practica = tk.Text(pnl, height=7, font=("Arial", 9), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_practica.pack(fill="x", pady=(0, 6))
        self.txt_practica.insert(tk.END, "1) The system is deployed after the tests pass.\n2) The library stores the data in a secure repository.\n3) If the compiler raises an error, review the log file.")

        btn = tk.Button(pnl, text="📘 Mostrar guía de práctica", command=self._mostrar_practica, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove", cursor="hand2")
        btn.pack(fill="x", pady=(0, 6))

        self.txt_res_practica = tk.Text(parent, height=12, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_res_practica.pack(fill="both", expand=True)
        self._mostrar_practica()

    def _mostrar_practica(self):
        if self.txt_res_practica is None:
            return
        self.txt_res_practica.delete("1.0", tk.END)
        self.txt_res_practica.insert(tk.END, "🗣️ GUÍA DE PRÁCTICA RÁPIDA:\n\n")
        self.txt_res_practica.insert(tk.END, "• Traducción útil: 'The system is deployed after the tests pass.' -> 'El sistema se despliega cuando las pruebas pasan.'\n")
        self.txt_res_practica.insert(tk.END, "• Frase clave en manuales: 'If the compiler raises an error, review the log file.'\n")
        self.txt_res_practica.insert(tk.END, "• Consejo: usa 'deploy', 'repository', 'library' y 'compiler' en contextos reales de software.\n\n")
        self.txt_res_practica.insert(tk.END, "💡 Ejercicios sugeridos:\n")
        self.txt_res_practica.insert(tk.END, "1. Explica con tus palabras qué hace un compiler.\n")
        self.txt_res_practica.insert(tk.END, "2. Describe la diferencia entre library y framework.\n")
        self.txt_res_practica.insert(tk.END, "3. Escribe una instrucción para deploy de una app web.\n")

    def _build_tab_analizador_doc(self, parent, panel_bg, fg_main, accent):
        pnl_doc = PanelBase(parent, titulo="📄 Analizador de Documentación, Readmes & Errores de Consola", bg_color=panel_bg)
        pnl_doc.pack(fill="x", pady=(0, 6))
        tk.Label(pnl_doc, text="Pega el fragmento de código, Readme o manual en inglés a analizar:", font=("Arial", 8, "italic"), bg=panel_bg, fg=fg_main).pack(anchor="w")

        input_box = tk.Text(pnl_doc, height=5, font=("Arial", 9), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_input_doc = input_box
        input_box.pack(fill="x", pady=4)
        input_box.insert("1.0", "Install the library using npm install. Pass the configuration object as an argument to the compiler function. If an error occurs, data is logged to the database.")

        btn_analizar_doc = tk.Button(pnl_doc, text="🔍 Analizar Documentación, Gramática y Términos IT", command=self._analyze_doc_text, bg="#28a745", fg="#ffffff", font=("Arial", 8, "bold"), relief="groove", cursor="hand2")
        btn_analizar_doc.pack(fill="x", pady=4)

        output_box = tk.Text(parent, height=10, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_res_doc = output_box
        output_box.pack(fill="both", expand=True)

    def _analyze_doc_text(self):
        input_box = cast(tk.Text | None, self.txt_input_doc)
        output_box = cast(tk.Text | None, self.txt_res_doc)
        if input_box is None or output_box is None:
            return

        raw_text = input_box.get("1.0", tk.END).strip()
        output_box.delete("1.0", tk.END)

        res: dict[str, Any] = analyze_technical_text_english(raw_text)
        if "error" in res:
            output_box.insert(tk.END, f"⚠️ {res['error']}\n")
            return

        found_terms = res.get("found_terms", {})
        found_false_friends = res.get("found_false_friends", {})
        grammar_insights = res.get("grammar_insights", [])

        if isinstance(found_terms, dict) and found_terms:
            output_box.insert(tk.END, "🔤 Technical IT Terms Identified:\n")
            for term, data in found_terms.items():
                if isinstance(data, dict):
                    output_box.insert(tk.END, f" • {term} -> {data.get('translation', '')} ({data.get('category', '')})\n")
                output_box.insert(tk.END, "\n")

        if isinstance(found_false_friends, dict) and found_false_friends:
            output_box.insert(tk.END, "⚠️ False Friends Alert:\n")
            for ff, data in found_false_friends.items():
                if isinstance(data, dict):
                    output_box.insert(tk.END, f" • {ff} -> Real meaning: {data.get('correct_meaning', '')}\n")
                output_box.insert(tk.END, "\n")

        if isinstance(grammar_insights, list) and grammar_insights:
            output_box.insert(tk.END, "📝 Grammar Structures Detected:\n")
            for gm in grammar_insights:
                if isinstance(gm, dict):
                    output_box.insert(tk.END, f" • {gm.get('rule', '')}: \"{gm.get('line', '')}\"\n")
                    output_box.insert(tk.END, f" └─ {gm.get('explanation', '')}\n")