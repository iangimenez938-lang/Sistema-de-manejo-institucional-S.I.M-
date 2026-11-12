import importlib
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

MODULE_DIR = Path(__file__).resolve().parent
if str(MODULE_DIR) not in sys.path:
    sys.path.insert(0, str(MODULE_DIR))

try:
    from configuracion.config_manager import cargar_configuracion, aplicar_estilos_globales
    from vistas.componentes_ui import PanelBase
except ImportError:
    def cargar_configuracion() -> dict:
        return {}

    def aplicar_estilos_globales(widget, config) -> None:
        return None

    class PanelBase(tk.LabelFrame):
        def __init__(self, parent=None, titulo="Panel", bg_color="#ffffff", fg_color="#007acc"):
            super().__init__(parent, text=titulo, bg=bg_color, fg=fg_color, font=("Arial", 9, "bold"), bd=1, relief="solid", padx=6, pady=6)

try:
    from . import herramientas as _herramientas
except ImportError:
    _herramientas = importlib.import_module("herramientas")

obtener_eventos_ordenados = _herramientas.obtener_eventos_ordenados
calcular_lapso_temporal = _herramientas.calcular_lapso_temporal
CUADROS_COMPARATIVOS = _herramientas.CUADROS_COMPARATIVOS
analizar_texto_historico = _herramientas.analizar_texto_historico
DICCIONARIO_HISTORIA = _herramientas.DICCIONARIO_HISTORIA


class ModuloHistoriaUI(tk.Frame):
    def __init__(self, parent=None, contexto=None, on_back_callback=None):
        self.contexto = contexto or {}
        self.on_back = on_back_callback
        config = cargar_configuracion()
        self.config_val = config if isinstance(config, dict) else {}
        bg_main = str(self.config_val.get("bg_color", "#ffffff"))
        panel_bg = str(self.config_val.get("panel_bg", "#f8f9fa"))
        fg_main = str(self.config_val.get("fg_color", "#212529"))
        accent = str(self.config_val.get("accent_color", "#007acc"))
        self.eventos_historia = [
            {"anio": int(evento["anio"]), "titulo": evento["evento"], "descripcion": evento["descripcion"], "categoria": evento["categoria"]}
            for evento in obtener_eventos_ordenados()
        ]
        super().__init__(parent, bg=bg_main)
        self.pack(fill="both", expand=True)
        self._build_ui(bg_main, panel_bg, fg_main, accent)
        aplicar_estilos_globales(self, self.config_val)

    def _build_ui(self, bg_main, panel_bg, fg_main, accent):
        header = tk.Frame(self, bg=accent, padx=12, pady=8)
        header.pack(fill="x")
        tk.Label(header, text="🏛️ Historia y sociedad", bg=accent, fg="#ffffff", font=("Arial", 12, "bold")).pack(anchor="w")
        if self.on_back:
            tk.Button(header, text="⬅️ Volver", bg="#ffffff", fg=accent, command=self.on_back).pack(side="right")
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)
        for title, builder in [
            ("🕰️ Línea del tiempo", self._build_tab_timeline),
            ("📊 Comparación", self._build_tab_comparacion),
            ("📝 Análisis", self._build_tab_analisis),
            ("📚 Glosario", self._build_tab_glosario),
        ]:
            tab = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
            notebook.add(tab, text=title)
            builder(tab, panel_bg, fg_main, accent)

    def _build_tab_timeline(self, parent, panel_bg, fg_main, accent):
        panel = PanelBase(parent, titulo="🕰️ Línea del tiempo histórica", bg_color=panel_bg)
        panel.pack(fill="both", expand=True)

        form = tk.Frame(panel, bg=panel_bg)
        form.pack(fill="x", pady=(0, 8))

        tk.Label(form, text="Año:", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=0, sticky="w", padx=(0, 6), pady=2)
        self.entry_anio = tk.Entry(form, width=10)
        self.entry_anio.grid(row=0, column=1, padx=4, pady=2)
        self.entry_anio.insert(0, "2020")

        tk.Label(form, text="Título:", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=2, sticky="w", padx=(10, 6), pady=2)
        self.entry_titulo = tk.Entry(form, width=28)
        self.entry_titulo.grid(row=0, column=3, padx=4, pady=2)

        tk.Label(form, text="Descripción:", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=1, column=0, sticky="w", padx=(0, 6), pady=2)
        self.entry_descripcion = tk.Entry(form, width=52)
        self.entry_descripcion.grid(row=1, column=1, columnspan=3, sticky="ew", padx=4, pady=2)

        tk.Label(form, text="Año inicio:", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=2, column=0, sticky="w", padx=(0, 6), pady=(6, 2))
        self.entry_anio_inicio = tk.Entry(form, width=10)
        self.entry_anio_inicio.grid(row=2, column=1, sticky="w", padx=4, pady=(6, 2))
        self.entry_anio_inicio.insert(0, "1810")

        tk.Label(form, text="Año fin:", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=2, column=2, sticky="w", padx=(10, 6), pady=(6, 2))
        self.entry_anio_fin = tk.Entry(form, width=10)
        self.entry_anio_fin.grid(row=2, column=3, sticky="w", padx=4, pady=(6, 2))
        self.entry_anio_fin.insert(0, "1983")

        buttons = tk.Frame(panel, bg=panel_bg)
        buttons.pack(fill="x", pady=(0, 8))
        tk.Button(
            buttons,
            text="Agregar evento",
            command=self._agregar_evento_manual,
            bg=accent,
            fg="#ffffff",
            font=("Arial", 8, "bold"),
            relief="groove",
            cursor="hand2",
        ).pack(side="left", padx=(0, 8))
        tk.Button(
            buttons,
            text="Calcular lapso",
            command=self._calcular_lapso_historico,
            bg="#6c757d",
            fg="#ffffff",
            font=("Arial", 8, "bold"),
            relief="groove",
            cursor="hand2",
        ).pack(side="left", padx=(0, 8))
        tk.Button(
            buttons,
            text="Restaurar eventos base",
            command=self._restaurar_eventos_base,
            bg="#e9ecef",
            fg="#212529",
            font=("Arial", 8, "bold"),
            relief="groove",
            cursor="hand2",
        ).pack(side="left")

        self.tabla_eventos = ttk.Treeview(panel, columns=("anio", "titulo", "descripcion"), show="headings", height=8)
        self.tabla_eventos.heading("anio", text="Año")
        self.tabla_eventos.heading("titulo", text="Título")
        self.tabla_eventos.heading("descripcion", text="Descripción")
        self.tabla_eventos.column("anio", width=80, anchor="center")
        self.tabla_eventos.column("titulo", width=200)
        self.tabla_eventos.column("descripcion", width=420)
        self.tabla_eventos.pack(fill="both", expand=True, pady=(0, 8))

        self.txt_timeline = tk.Text(panel, height=10, font=("Consolas", 9), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_timeline.pack(fill="both", expand=True, padx=4, pady=4)
        self._mostrar_timeline()

    def _version_base_eventos(self):
        return [
            {"anio": int(evento["anio"]), "titulo": evento["evento"], "descripcion": evento["descripcion"], "categoria": evento["categoria"]}
            for evento in obtener_eventos_ordenados()
        ]

    def _restaurar_eventos_base(self):
        self.eventos_historia = self._version_base_eventos()
        self._mostrar_timeline()

    def _agregar_evento_manual(self):
        try:
            anio = int(self.entry_anio.get().strip())
        except ValueError:
            self.txt_timeline.insert(tk.END, "\n⚠️ El año debe ser un número válido.\n")
            return

        titulo = (self.entry_titulo.get() or "Sin título").strip()
        descripcion = (self.entry_descripcion.get() or "").strip()
        if not titulo:
            titulo = "Evento sin título"

        self.eventos_historia.append({
            "anio": anio,
            "titulo": titulo,
            "descripcion": descripcion,
            "categoria": "Evento agregado por el usuario",
        })
        self.eventos_historia = sorted(self.eventos_historia, key=lambda item: int(item["anio"]))
        for entry in (self.entry_anio, self.entry_titulo, self.entry_descripcion):
            if hasattr(entry, "delete"):
                entry.delete(0, tk.END)
        self._mostrar_timeline()

    def _mostrar_timeline(self):
        self.eventos_historia = sorted(self.eventos_historia, key=lambda item: int(item["anio"]))

        for item in self.tabla_eventos.get_children():
            self.tabla_eventos.delete(item)

        for evento in self.eventos_historia:
            self.tabla_eventos.insert("", "end", values=(evento["anio"], evento["titulo"], evento["descripcion"]))

        if hasattr(self, "txt_timeline"):
            self.txt_timeline.delete("1.0", tk.END)
            self.txt_timeline.insert(tk.END, "🕰️ LÍNEA DEL TIEMPO HISTÓRICA\n\n")
            for evento in self.eventos_historia:
                self.txt_timeline.insert(tk.END, f"{evento['anio']} - {evento['titulo']}\n")
                self.txt_timeline.insert(tk.END, f"  • {evento['descripcion']}\n\n")

    def _calcular_lapso_historico(self):
        try:
            anio_inicio = int(self.entry_anio_inicio.get())
            anio_fin = int(self.entry_anio_fin.get())
            res = calcular_lapso_temporal(anio_inicio, anio_fin)
            self.txt_timeline.insert(tk.END, "\n📏 LAPSO TEMPORAL CALCULADO\n")
            self.txt_timeline.insert(tk.END, f"• Desde {res['anio_inicio']} hasta {res['anio_fin']}\n")
            self.txt_timeline.insert(tk.END, f"• Diferencia: {res['diferencia_anios']} años ({res['diferencia_siglos']} siglos)\n")
        except ValueError:
            self.txt_timeline.insert(tk.END, "\n⚠️ Ingresa años válidos.\n")

    def _build_tab_comparacion(self, parent, panel_bg, fg_main, accent):
        panel = PanelBase(parent, titulo="📊 Cuadro comparativo histórico", bg_color=panel_bg)
        panel.pack(fill="both", expand=True)

        self.var_comparacion = tk.StringVar(value=list(CUADROS_COMPARATIVOS.keys())[0])
        options = list(CUADROS_COMPARATIVOS.keys())
        ttk.Combobox(panel, textvariable=self.var_comparacion, values=options, state="readonly", width=50).pack(fill="x", pady=(0, 6))
        self.var_comparacion.trace_add("write", self._mostrar_comparacion_actual)

        self.txt_comparacion = tk.Text(panel, height=12, font=("Consolas", 9), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_comparacion.pack(fill="both", expand=True, padx=4, pady=4)
        self._mostrar_comparacion_actual()

    def _mostrar_comparacion_actual(self, *args):
        nombre = self.var_comparacion.get()
        dato = CUADROS_COMPARATIVOS.get(nombre)
        if not dato:
            return
        self.txt_comparacion.delete("1.0", tk.END)
        self.txt_comparacion.insert(tk.END, f"📊 {nombre}\n\n")
        for eje in dato["ejes"]:
            self.txt_comparacion.insert(tk.END, f"• {eje}\n")
            for lado in ("A", "B"):
                self.txt_comparacion.insert(tk.END, f"  {dato[lado]['nombre']}: {', '.join(dato[lado]['detalles'])}\n")
            self.txt_comparacion.insert(tk.END, "\n")

    def _build_tab_analisis(self, parent, panel_bg, fg_main, accent):
        panel = PanelBase(parent, titulo="📝 Análisis de textos históricos", bg_color=panel_bg)
        panel.pack(fill="both", expand=True)

        self.txt_input_analisis = tk.Text(panel, height=6, font=("Arial", 9), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_input_analisis.pack(fill="x", padx=4, pady=(4, 6))
        self.txt_input_analisis.insert(tk.END, "La Revolución de Mayo marcó el inicio de la lucha por la independencia argentina. La sociedad se reorganizó con nuevas ideas de soberanía, ciudadanía y participación política. Este proceso impulsó la construcción del Estado moderno y el debate sobre la libertad.")

        tk.Button(
            panel,
            text="Analizar documento",
            command=self._analizar_texto_historico_ui,
            bg=accent,
            fg="#ffffff",
            font=("Arial", 8, "bold"),
            relief="groove",
            cursor="hand2",
        ).pack(fill="x", padx=4, pady=(0, 6))

        self.txt_analisis = tk.Text(panel, height=12, font=("Consolas", 9), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_analisis.pack(fill="both", expand=True, padx=4, pady=4)
        self._analizar_texto_historico_ui()

    def _analizar_texto_historico_ui(self):
        texto = self.txt_input_analisis.get("1.0", tk.END)
        res = analizar_texto_historico(texto)
        self.txt_analisis.delete("1.0", tk.END)
        if "error" in res:
            self.txt_analisis.insert(tk.END, f"⚠️ {res['error']}\n")
            return

        self.txt_analisis.insert(tk.END, "📝 ANÁLISIS HISTÓRICO\n\n")
        self.txt_analisis.insert(tk.END, f"• Palabras clave: {', '.join(res.get('palabras_clave', [])) or 'Sin palabras clave detectadas'}\n")
        self.txt_analisis.insert(tk.END, f"• Número de palabras: {res['num_palabras']}\n")
        self.txt_analisis.insert(tk.END, f"• Número de oraciones: {res['num_oraciones']}\n\n")
        self.txt_analisis.insert(tk.END, f"RESUMEN: {res['resumen_analitico']}\n\n")
        for i, item in enumerate(res.get("guia_preguntas_respuestas", []), start=1):
            self.txt_analisis.insert(tk.END, f"P{i}. {item['pregunta']}\n")
            self.txt_analisis.insert(tk.END, f"R{i}. {item['respuesta']}\n\n")

    def _build_tab_glosario(self, parent, panel_bg, fg_main, accent):
        panel = PanelBase(parent, titulo="📚 Glosario de conceptos históricos", bg_color=panel_bg)
        panel.pack(fill="both", expand=True)
        self.txt_glosario_h = tk.Text(panel, height=12, font=("Consolas", 9), bg="#ffffff", bd=1, relief="solid", wrap="word")
        self.txt_glosario_h.pack(fill="both", expand=True, padx=4, pady=4)
        self.txt_glosario_h.insert(tk.END, "📚 GLOSARIO DE CONCEPTOS HISTÓRICOS\n\n")
        for term, definition in DICCIONARIO_HISTORIA.items():
            self.txt_glosario_h.insert(tk.END, f"{term}: {definition}\n\n")
