import tkinter as tk
from tkinter import ttk, messagebox
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

try:
    from configuracion.config_manager import cargar_configuracion, aplicar_estilos_globales
    from vistas.componentes_ui import PanelBase
except ImportError:  # pragma: no cover - only for minimal fallback during isolated testing.
    def cargar_configuracion() -> dict:
        return {}

    def aplicar_estilos_globales(root, config):
        return None

    class _FallbackPanelBase(tk.LabelFrame):
        def __init__(self, parent=None, titulo="Panel", bg_color="#ffffff", fg_color="#007acc"):
            super().__init__(parent, text=titulo, bg=bg_color, fg=fg_color, font=("Arial", 9, "bold"), bd=1, relief="solid", padx=6, pady=6)

    PanelBase = _FallbackPanelBase

from .matematica_herramientas import (
    resolver_sistema_2x2,
    analizar_funcion_cuadratica,
    optimizacion_programacion_lineal_2d,
)


class ModuloMatematicaUI(tk.Frame):
    """Vista principal interactiva para el módulo de Matemática."""

    def __init__(self, parent=None, contexto: dict | None = None, on_back_callback=None):
        super().__init__(parent, bg="#ffffff")
        self.contexto = contexto or {}
        self.on_back = on_back_callback
        self.config_val = cargar_configuracion()
        bg_main = self.config_val.get("bg_color", "#ffffff")
        panel_bg = self.config_val.get("panel_bg", "#f8f9fa")
        fg_main = self.config_val.get("fg_color", "#212529")
        accent = self.config_val.get("accent_color", "#007acc")
        self.configure(bg=bg_main)
        self.pack(fill="both", expand=True)
        self._build_ui(bg_main=bg_main, panel_bg=panel_bg, fg_main=fg_main, accent=accent)
        aplicar_estilos_globales(self, self.config_val)

    def _build_ui(self, bg_main="#ffffff", panel_bg="#f8f9fa", fg_main="#212529", accent="#007acc"):
        header_frame = tk.Frame(self, bg=accent, padx=12, pady=8, bd=1, relief="solid")
        header_frame.pack(fill="x", side="top")

        left_header = tk.Frame(header_frame, bg=accent)
        left_header.pack(side="left", fill="both", expand=True)

        tk.Label(left_header, text="📐 Módulo de Matemática - 4.º Año Informática", font=("Arial", 12, "bold"), fg="#ffffff", bg=accent).pack(anchor="w")
        tk.Label(left_header, text="Álgebra Aplicada, Funciones, Optimización por Programación Lineal y Vectores 2D/3D", font=("Arial", 8), fg="#edf7ff", bg=accent).pack(anchor="w")

        if self.on_back:
            btn_volver = tk.Button(header_frame, text="⬅️ Volver al Aula", command=self.on_back, bg="#ffffff", fg=accent, font=("Arial", 8, "bold"), relief="groove", padx=8, pady=2, cursor="hand2")
            btn_volver.pack(side="right")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Math.TNotebook", background=bg_main)
        style.configure("Math.TNotebook.Tab", font=("Arial", 9, "bold"), padding=[10, 4])

        notebook = ttk.Notebook(self, style="Math.TNotebook")
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        tab1 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab1, text="🧮 Sistemas & Matrices")
        self._build_tab_sistemas_matrices(tab1, panel_bg, fg_main, accent)

        tab2 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab2, text="📈 Funciones & Modelos")
        self._build_tab_funciones(tab2, panel_bg, fg_main, accent)

        tab3 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab3, text="🎯 Programación Lineal")
        self._build_tab_programacion_lineal(tab3, panel_bg, fg_main, accent)

        tab4 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab4, text="📐 Calculadora Vectorial")
        self._build_tab_vectores(tab4, panel_bg, fg_main, accent)

    def _build_tab_sistemas_matrices(self, parent, panel_bg, fg_main, accent):
        pnl_sis = PanelBase(parent, titulo="⚡ Resolvedor de Sistemas 2x2 (Regla de Cramer)", bg_color=panel_bg)
        pnl_sis.pack(side="left", fill="both", expand=True, padx=4, pady=4)

        f_eq1 = tk.Frame(pnl_sis, bg=panel_bg)
        f_eq1.pack(fill="x", pady=4)
        tk.Label(f_eq1, text="Eq 1: ", font=("Arial", 8, "bold"), bg=panel_bg).pack(side="left")

        self.e_a1 = tk.Entry(f_eq1, width=5, justify="center")
        self.e_a1.pack(side="left")
        self.e_a1.insert(0, "2")
        tk.Label(f_eq1, text=" x + ", font=("Arial", 8), bg=panel_bg).pack(side="left")

        self.e_b1 = tk.Entry(f_eq1, width=5, justify="center")
        self.e_b1.pack(side="left")
        self.e_b1.insert(0, "1")
        tk.Label(f_eq1, text=" y = ", font=("Arial", 8), bg=panel_bg).pack(side="left")
        self.e_c1 = tk.Entry(f_eq1, width=5, justify="center")
        self.e_c1.pack(side="left")
        self.e_c1.insert(0, "8")

        f_eq2 = tk.Frame(pnl_sis, bg=panel_bg)
        f_eq2.pack(fill="x", pady=4)
        tk.Label(f_eq2, text="Eq 2: ", font=("Arial", 8, "bold"), bg=panel_bg).pack(side="left")

        self.e_a2 = tk.Entry(f_eq2, width=5, justify="center")
        self.e_a2.pack(side="left")
        self.e_a2.insert(0, "1")
        tk.Label(f_eq2, text=" x + ", font=("Arial", 8), bg=panel_bg).pack(side="left")

        self.e_b2 = tk.Entry(f_eq2, width=5, justify="center")
        self.e_b2.pack(side="left")
        self.e_b2.insert(0, "-1")
        tk.Label(f_eq2, text=" y = ", font=("Arial", 8), bg=panel_bg).pack(side="left")

        self.e_c2 = tk.Entry(f_eq2, width=5, justify="center")
        self.e_c2.pack(side="left")
        self.e_c2.insert(0, "1")
        tk.Button(pnl_sis, text="🧮 Calcular Sistema Paso a Paso", command=self._calc_sistema_2x2, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove", cursor="hand2").pack(fill="x", pady=6)

        self.txt_res_sis = tk.Text(pnl_sis, height=9, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid")
        self.txt_res_sis.pack(fill="both", expand=True)

        pnl_mat = PanelBase(parent, titulo="📊 Calculadora de Matrices 2x2", bg_color=panel_bg)
        pnl_mat.pack(side="right", fill="both", expand=True, padx=4, pady=4)

        f_mats = tk.Frame(pnl_mat, bg=panel_bg)
        f_mats.pack(fill="x", pady=2)

        f_mA = tk.LabelFrame(f_mats, text="Matriz A", bg=panel_bg, font=("Arial", 8, "bold"))
        f_mA.pack(side="left", fill="both", expand=True, padx=2)
        self.e_a11 = tk.Entry(f_mA, width=4, justify="center")
        self.e_a11.grid(row=0, column=0, padx=2, pady=2)
        self.e_a11.insert(0, "2")
        self.e_a12 = tk.Entry(f_mA, width=4, justify="center")
        self.e_a12.grid(row=0, column=1, padx=2, pady=2)
        self.e_a12.insert(0, "1")
        self.e_a21 = tk.Entry(f_mA, width=4, justify="center")
        self.e_a21.grid(row=1, column=0, padx=2, pady=2)
        self.e_a21.insert(0, "5")
        self.e_a22 = tk.Entry(f_mA, width=4, justify="center")
        self.e_a22.grid(row=1, column=1, padx=2, pady=2)
        self.e_a22.insert(0, "3")

        f_mB = tk.LabelFrame(f_mats, text="Matriz B", bg=panel_bg, font=("Arial", 8, "bold"))
        f_mB.pack(side="right", fill="both", expand=True, padx=2)

        self.e_b11 = tk.Entry(f_mB, width=4, justify="center")
        self.e_b11.grid(row=0, column=0, padx=2, pady=2)
        self.e_b11.insert(0, "1")
        self.e_b12 = tk.Entry(f_mB, width=4, justify="center")
        self.e_b12.grid(row=0, column=1, padx=2, pady=2)
        self.e_b12.insert(0, "-2")
        self.e_b21 = tk.Entry(f_mB, width=4, justify="center")
        self.e_b21.grid(row=1, column=0, padx=2, pady=2)
        self.e_b21.insert(0, "0")
        self.e_b22 = tk.Entry(f_mB, width=4, justify="center")
        self.e_b22.grid(row=1, column=1, padx=2, pady=2)
        self.e_b22.insert(0, "4")

        f_btns_m = tk.Frame(pnl_mat, bg=panel_bg)
        f_btns_m.pack(fill="x", pady=4)

        tk.Button(f_btns_m, text="Propiedades A (|A|, Inversa)", command=self._calc_prop_A, bg=accent, fg="#ffffff", font=("Arial", 7, "bold"), relief="groove").pack(side="left", fill="x", expand=True, padx=1)
        tk.Button(f_btns_m, text="Multiplicar (A × B)", command=self._calc_prod_AB, bg="#28a745", fg="#ffffff", font=("Arial", 7, "bold"), relief="groove").pack(side="right", fill="x", expand=True, padx=1)

        self.txt_res_mat = tk.Text(pnl_mat, height=9, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid")
        self.txt_res_mat.pack(fill="both", expand=True)

    def _build_tab_funciones(self, parent, panel_bg, fg_main, accent):
        panel = PanelBase(parent, titulo="📈 Funciones & Modelos", bg_color=panel_bg)
        panel.pack(fill="both", expand=True)

        form = tk.Frame(panel, bg=panel_bg)
        form.pack(fill="x", pady=(6, 8))
        tk.Label(form, text="Coeficiente a:", bg=panel_bg, fg=fg_main, font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8), pady=2)
        self.func_a = tk.Entry(form, width=8)
        self.func_a.grid(row=0, column=1, padx=2, pady=2)
        self.func_a.insert(0, "1")

        tk.Label(form, text="Coeficiente b:", bg=panel_bg, fg=fg_main, font=("Arial", 9, "bold")).grid(row=0, column=2, sticky="w", padx=(12, 8), pady=2)
        self.func_b = tk.Entry(form, width=8)
        self.func_b.grid(row=0, column=3, padx=2, pady=2)
        self.func_b.insert(0, "-3")

        tk.Label(form, text="Coeficiente c:", bg=panel_bg, fg=fg_main, font=("Arial", 9, "bold")).grid(row=0, column=4, sticky="w", padx=(12, 8), pady=2)
        self.func_c = tk.Entry(form, width=8)
        self.func_c.grid(row=0, column=5, padx=2, pady=2)
        self.func_c.insert(0, "2")

        tk.Button(form, text="Analizar función", command=self._analizar_funcion, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove").grid(row=1, column=0, columnspan=6, sticky="ew", pady=(8, 2))

        self.funciones_info = tk.Text(panel, height=8, width=40, bg="#ffffff", fg=fg_main, bd=1, relief="solid")
        self.funciones_info.pack(fill="both", expand=True)
        self._analizar_funcion()

    def _build_tab_programacion_lineal(self, parent, panel_bg, fg_main, accent):
        panel = PanelBase(parent, titulo="🎯 Programación Lineal", bg_color=panel_bg)
        panel.pack(fill="both", expand=True)

        form = tk.Frame(panel, bg=panel_bg)
        form.pack(fill="x", pady=(6, 8))

        tk.Label(form, text="Z = c1*x + c2*y", bg=panel_bg, fg=fg_main, font=("Arial", 9, "bold")).grid(row=0, column=0, columnspan=4, sticky="w")
        tk.Label(form, text="c1:", bg=panel_bg, fg=fg_main, font=("Arial", 8, "bold")).grid(row=1, column=0, sticky="w", padx=(0, 6), pady=2)
        self.pl_c1 = tk.Entry(form, width=8)
        self.pl_c1.grid(row=1, column=1, padx=2)
        self.pl_c1.insert(0, "3")

        tk.Label(form, text="c2:", bg=panel_bg, fg=fg_main, font=("Arial", 8, "bold")).grid(row=1, column=2, sticky="w", padx=(12, 6), pady=2)
        self.pl_c2 = tk.Entry(form, width=8)
        self.pl_c2.grid(row=1, column=3, padx=2)
        self.pl_c2.insert(0, "2")

        tk.Label(form, text="Puntos vértice (x,y):", bg=panel_bg, fg=fg_main, font=("Arial", 8, "bold")).grid(row=2, column=0, sticky="w", pady=(8, 2))
        self.pl_vertices = tk.Entry(form, width=36)
        self.pl_vertices.grid(row=2, column=1, columnspan=3, sticky="ew", pady=(8, 2))
        self.pl_vertices.insert(0, "(0,0); (4,0); (0,3); (2,2)")

        tk.Button(form, text="Optimizar", command=self._optimizar_programacion_lineal, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove").grid(row=3, column=0, columnspan=4, sticky="ew", pady=(8, 0))

        self.txt_programacion_lineal = tk.Text(panel, height=8, bg="#ffffff", fg=fg_main, bd=1, relief="solid")
        self.txt_programacion_lineal.pack(fill="both", expand=True, pady=(8, 0))
        self._optimizar_programacion_lineal()

    def _build_tab_vectores(self, parent, panel_bg, fg_main, accent):
        panel = PanelBase(parent, titulo="📐 Calculadora Vectorial", bg_color=panel_bg)
        panel.pack(fill="both", expand=True)

        form = tk.Frame(panel, bg=panel_bg)
        form.pack(fill="x", pady=(6, 8))

        tk.Label(form, text="Vector A (x, y, z):", bg=panel_bg, fg=fg_main, font=("Arial", 8, "bold")).grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.vec_a = tk.Entry(form, width=16)
        self.vec_a.grid(row=0, column=1, padx=2)
        self.vec_a.insert(0, "2, 3, 1")

        tk.Label(form, text="Vector B (x, y, z):", bg=panel_bg, fg=fg_main, font=("Arial", 8, "bold")).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(8, 2))
        self.vec_b = tk.Entry(form, width=16)
        self.vec_b.grid(row=1, column=1, padx=2, pady=(8, 2))
        self.vec_b.insert(0, "1, -2, 4")

        tk.Button(form, text="Calcular suma y producto escalar", command=self._calcular_vectores, bg=accent, fg="#ffffff", font=("Arial", 8, "bold"), relief="groove").grid(row=2, column=0, columnspan=2, sticky="ew", pady=(8, 0))

        self.txt_vectores = tk.Text(panel, height=8, bg="#ffffff", fg=fg_main, bd=1, relief="solid")
        self.txt_vectores.pack(fill="both", expand=True)
        self._calcular_vectores()

    def _analizar_funcion(self):
        try:
            a = float(self.func_a.get())
            b = float(self.func_b.get())
            c = float(self.func_c.get())
            res = analizar_funcion_cuadratica(a, b, c)
            self.funciones_info.delete("1.0", tk.END)
            if "error" in res:
                self.funciones_info.insert(tk.END, f"⚠️ {res['error']}\n")
                return
            self.funciones_info.insert(tk.END, f"f(x) = {a}x² + {b}x + {c}\n\n")
            self.funciones_info.insert(tk.END, f"• Vértice: {res['vertice']}\n")
            self.funciones_info.insert(tk.END, f"• Tipo de vértice: {res['tipo_vertice']}\n")
            self.funciones_info.insert(tk.END, f"• Discriminante: {res['discriminante']}\n")
            self.funciones_info.insert(tk.END, f"• Raíces: {res['raices'] if res['raices'] else 'Sin raíces reales'}\n")
            self.funciones_info.insert(tk.END, f"• Corte en Y: {res['corte_y']}\n")
            self.funciones_info.insert(tk.END, f"• Orientación: {res['orientacion']}\n")
        except Exception:
            messagebox.showerror("Error", "Ingresa valores válidos para a, b y c.")

    def _optimizar_programacion_lineal(self):
        try:
            c1 = float(self.pl_c1.get())
            c2 = float(self.pl_c2.get())
            puntos_texto = self.pl_vertices.get().strip()
            puntos = []
            for item in puntos_texto.replace("(", "").replace(")", "").split(";"):
                if not item.strip():
                    continue
                x_raw, y_raw = item.strip().split(",")
                puntos.append((float(x_raw.strip()), float(y_raw.strip())))

            res = optimizacion_programacion_lineal_2d(c1, c2, puntos, tipo="max")
            self.txt_programacion_lineal.delete("1.0", tk.END)
            if "error" in res:
                self.txt_programacion_lineal.insert(tk.END, f"⚠️ {res['error']}\n")
                return
            self.txt_programacion_lineal.insert(tk.END, "🎯 OPTIMIZACIÓN DE PROGRAMACIÓN LINEAL\n\n")
            for ev in res["evaluaciones"]:
                self.txt_programacion_lineal.insert(tk.END, f"• P({ev['x']}, {ev['y']}) => Z = {ev['z']}\n")
            self.txt_programacion_lineal.insert(tk.END, "\n✅ Óptimo: ")
            self.txt_programacion_lineal.insert(tk.END, f"P({res['optimo']['x']}, {res['optimo']['y']}) con Z = {res['optimo']['z']}\n")
        except Exception:
            messagebox.showerror("Error", "Verifica que los valores de c1, c2 y los vértices estén bien ingresados.")

    def _calcular_vectores(self):
        try:
            vec_a = [float(v.strip()) for v in self.vec_a.get().split(",") if v.strip()]
            vec_b = [float(v.strip()) for v in self.vec_b.get().split(",") if v.strip()]
            if len(vec_a) != 3 or len(vec_b) != 3:
                raise ValueError

            suma = [a + b for a, b in zip(vec_a, vec_b)]
            producto_escalar = sum(a * b for a, b in zip(vec_a, vec_b))
            self.txt_vectores.delete("1.0", tk.END)
            self.txt_vectores.insert(tk.END, "📐 OPERACIONES CON VECTORES\n\n")
            self.txt_vectores.insert(tk.END, f"• Vector A: {vec_a}\n")
            self.txt_vectores.insert(tk.END, f"• Vector B: {vec_b}\n")
            self.txt_vectores.insert(tk.END, f"• Suma A + B: {suma}\n")
            self.txt_vectores.insert(tk.END, f"• Producto escalar A · B: {producto_escalar}\n")
        except Exception:
            messagebox.showerror("Error", "Usa tres valores separados por coma para cada vector, por ejemplo: 2, 3, 1.")

    def _calc_sistema_2x2(self):
        try:
            a1, b1, c1 = float(self.e_a1.get()), float(self.e_b1.get()), float(self.e_c1.get())
            a2, b2, c2 = float(self.e_a2.get()), float(self.e_b2.get()), float(self.e_c2.get())
            res = resolver_sistema_2x2(a1, b1, c1, a2, b2, c2)
            self.txt_res_sis.delete("1.0", tk.END)
            if res["tipo"] == "unico":
                self.txt_res_sis.insert(tk.END, f"📌 Solución Única:\n X = {res['x']}\n Y = {res['y']}\n\n📋 Pasos de Resolución:\n")
                for paso in res["pasos"]:
                    self.txt_res_sis.insert(tk.END, f"• {paso}\n")
            else:
                self.txt_res_sis.insert(tk.END, f"⚠️ {res['mensaje']}\n")
        except Exception:
            messagebox.showerror("Error", "Ingresa números válidos.")

    def _calc_prop_A(self):
        try:
            A = [[float(self.e_a11.get()), float(self.e_a12.get())], [float(self.e_a21.get()), float(self.e_a22.get())]]
            det = (A[0][0] * A[1][1]) - (A[0][1] * A[1][0])
            traza = A[0][0] + A[1][1]
            self.txt_res_mat.delete("1.0", tk.END)
            self.txt_res_mat.insert(tk.END, "📊 Propiedades de Matriz A:\n")
            self.txt_res_mat.insert(tk.END, f"• Determinante |A|: {det}\n")
            self.txt_res_mat.insert(tk.END, f"• Traza Tr(A): {traza}\n")
            if abs(det) > 1e-9:
                inv_det = 1 / det
                inv = [[inv_det * A[1][1], -inv_det * A[0][1]], [-inv_det * A[1][0], inv_det * A[0][0]]]
                self.txt_res_mat.insert(tk.END, f"• Matriz Inversa A⁻¹:\n [{inv[0][0]}, {inv[0][1]}]\n [{inv[1][0]}, {inv[1][1]}]\n")
            else:
                self.txt_res_mat.insert(tk.END, "• Inversa A⁻¹: No existe (|A| = 0)\n")
        except Exception:
            messagebox.showerror("Error", "Ingresa números válidos.")

    def _calc_prod_AB(self):
        try:
            A = [[float(self.e_a11.get()), float(self.e_a12.get())], [float(self.e_a21.get()), float(self.e_a22.get())]]
            B = [[float(self.e_b11.get()), float(self.e_b12.get())], [float(self.e_b21.get()), float(self.e_b22.get())]]
            C = [
                [A[0][0] * B[0][0] + A[0][1] * B[1][0], A[0][0] * B[0][1] + A[0][1] * B[1][1]],
                [A[1][0] * B[0][0] + A[1][1] * B[1][0], A[1][0] * B[0][1] + A[1][1] * B[1][1]],
            ]
            self.txt_res_mat.delete("1.0", tk.END)
            self.txt_res_mat.insert(tk.END, "✖️ Producto de Matrices (C = A × B):\n\n")
            self.txt_res_mat.insert(tk.END, f" [{C[0][0]}, {C[0][1]}]\n [{C[1][0]}, {C[1][1]}]\n")
        except Exception:
            messagebox.showerror("Error", "Ingresa números válidos.")


VistaMatematicaUI = ModuloMatematicaUI
