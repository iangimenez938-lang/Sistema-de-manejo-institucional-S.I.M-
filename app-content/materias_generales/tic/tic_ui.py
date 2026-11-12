import importlib
import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

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
            super().__init__(
                parent,
                text=titulo,
                bg=bg_color,
                fg=fg_color,
                font=("Arial", 9, "bold"),
                bd=1,
                relief="solid",
                padx=6,
                pady=6,
            )

try:
    from . import herramientas as _herramientas
except ImportError:
    _herramientas = importlib.import_module("herramientas")

analizar_red_ip = _herramientas.analizar_red_ip
generar_hashes_seguridad = _herramientas.generar_hashes_seguridad
cifrado_cesar_simulado = _herramientas.cifrado_cesar_simulado
PUERTOS_Y_SERVICIOS_TIC = _herramientas.PUERTOS_Y_SERVICIOS_TIC
DICCIONARIO_TIC = _herramientas.DICCIONARIO_TIC


class ModuloTicUI(tk.Frame):
    """Vista interactiva para el módulo TIC."""

    def __init__(self, parent=None, contexto: dict | None = None, on_back_callback=None):
        self.contexto = contexto or {}
        self.on_back = on_back_callback
        config = cargar_configuracion()
        self.config_val = config if isinstance(config, dict) else {}
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
        tk.Label(
            left_header,
            text="💻 Módulo de TIC (Tecnologías de la Información) - 4.º Año Informática",
            font=("Arial", 12, "bold"),
            fg="#ffffff",
            bg=accent,
        ).pack(anchor="w")
        tk.Label(
            left_header,
            text="Redes IP, Direccionamiento, Ciberseguridad, Cifrado, Protocolos Web y Servicios",
            font=("Arial", 8),
            fg="#edf7ff",
            bg=accent,
        ).pack(anchor="w")

        if self.on_back:
            btn_volver = tk.Button(
                header_frame,
                text="⬅️ Volver al Aula",
                command=self.on_back,
                bg="#ffffff",
                fg=accent,
                font=("Arial", 8, "bold"),
                relief="groove",
                padx=8,
                pady=2,
                cursor="hand2",
            )
            btn_volver.pack(side="right")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Tic.TNotebook", background=bg_main)
        style.configure("Tic.TNotebook.Tab", font=("Arial", 9, "bold"), padding=[10, 4])

        notebook = ttk.Notebook(self, style="Tic.TNotebook")
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        tab1 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab1, text="🌐 Redes & Calculadora IP")
        self._build_tab_redes(tab1, panel_bg, fg_main, accent)

        tab2 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab2, text="🔐 Ciberseguridad & Cifrado")
        self._build_tab_seguridad(tab2, panel_bg, fg_main, accent)

        tab3 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab3, text="📡 Guía de Protocolos & Puertos")
        self._build_tab_protocolos(tab3, panel_bg, fg_main, accent)

        tab4 = tk.Frame(notebook, bg=bg_main, padx=8, pady=8)
        notebook.add(tab4, text="📚 Glosario TIC")
        self._build_tab_glosario(tab4, panel_bg, fg_main, accent)

    def _build_tab_redes(self, parent, panel_bg, fg_main, accent):
        pnl = PanelBase(
            parent,
            titulo="🌐 Calculadora de Subredes y Direccionamiento IPv4",
            bg_color=panel_bg,
        )
        pnl.pack(fill="x", pady=(0, 6))

        f_in = tk.Frame(pnl, bg=panel_bg)
        f_in.pack(fill="x", pady=2)
        tk.Label(f_in, text="Dirección IPv4:", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=0, sticky="w")

        self.e_ip = tk.Entry(f_in, width=16, justify="center")
        self.e_ip.grid(row=0, column=1, padx=4)
        self.e_ip.insert(0, "192.168.1.100")

        tk.Label(f_in, text="Máscara CIDR (/):", font=("Arial", 8, "bold"), bg=panel_bg).grid(row=0, column=2, sticky="w")
        self.cmb_cidr = ttk.Combobox(f_in, values=[f"/{i}" for i in range(8, 31)], state="readonly", width=6)
        self.cmb_cidr.set("/24")
        self.cmb_cidr.grid(row=0, column=3, padx=4)

        btn_ip = tk.Button(
            pnl,
            text="🌐 Analizar Red y Rango de IPs Útiles",
            command=self._calc_red_ip,
            bg=accent,
            fg="#ffffff",
            font=("Arial", 8, "bold"),
            relief="groove",
            cursor="hand2",
        )
        btn_ip.pack(fill="x", pady=4)

        self.txt_res_red = tk.Text(parent, height=10, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid")
        self.txt_res_red.pack(fill="both", expand=True)

    def _calc_red_ip(self):
        ip = self.e_ip.get().strip()
        cidr = int(self.cmb_cidr.get().replace("/", ""))
        self.txt_res_red.delete("1.0", tk.END)

        res = analizar_red_ip(ip, cidr)
        if "error" in res:
            self.txt_res_red.insert(tk.END, f"⚠️ {res['error']}\n")
            return

        self.txt_res_red.insert(tk.END, f"🌐 ANÁLISIS DE SUBRED Y DIRECCIONAMIENTO IP ({res['cidr']}):\n\n")
        self.txt_res_red.insert(tk.END, f"• Dirección IP Host: {res['ip_ingresada']} ({res['tipo_ip']}, Clase {res['clase_ip']})\n")
        self.txt_res_red.insert(tk.END, f"• Máscara de Subred: {res['mascara_subred']}\n")
        self.txt_res_red.insert(tk.END, f"• Dirección de Red: {res['direccion_red']}\n")
        self.txt_res_red.insert(tk.END, f"• Dirección de Broadcast: {res['direccion_broadcast']}\n")
        self.txt_res_red.insert(tk.END, f"• Primera IP útil: {res['primera_ip_util']}\n")
        self.txt_res_red.insert(tk.END, f"• Última IP útil: {res['ultima_ip_util']}\n")
        self.txt_res_red.insert(tk.END, f"• Total de hosts útiles: {res['total_hosts_utiles']}\n")

    def _build_tab_seguridad(self, parent, panel_bg, fg_main, accent):
        pnl_h = PanelBase(parent, titulo="🔐 Generador de Hashes e Integridad", bg_color=panel_bg)
        pnl_h.pack(fill="x", pady=(0, 6))

        f_h = tk.Frame(pnl_h, bg=panel_bg)
        f_h.pack(fill="x", pady=2)
        tk.Label(f_h, text="Texto / Contraseña:", font=("Arial", 8, "bold"), bg=panel_bg).pack(side="left")

        self.e_pass = tk.Entry(f_h, width=30)
        self.e_pass.pack(side="left", padx=4)
        self.e_pass.insert(0, "MiContraseñaSegura2026")

        btn_hash = tk.Button(
            pnl_h,
            text="🔐 Generar Huellas Digitales (Hashes)",
            command=self._calc_hash,
            bg=accent,
            fg="#ffffff",
            font=("Arial", 8, "bold"),
            relief="groove",
        )
        btn_hash.pack(fill="x", pady=4)

        pnl_c = PanelBase(parent, titulo="🔑 Cifrado Simulado por Sustitución (César)", bg_color=panel_bg)
        pnl_c.pack(fill="x", pady=(0, 6))

        f_c = tk.Frame(pnl_c, bg=panel_bg)
        f_c.pack(fill="x", pady=2)
        tk.Label(f_c, text="Desplazamiento Clave:", font=("Arial", 8, "bold"), bg=panel_bg).pack(side="left")

        self.e_shift = tk.Entry(f_c, width=6, justify="center")
        self.e_shift.pack(side="left", padx=4)
        self.e_shift.insert(0, "3")

        btn_cif = tk.Button(
            pnl_c,
            text="🔑 Cifrar Mensaje",
            command=lambda: self._cifrar_texto("cifrar"),
            bg="#28a745",
            fg="#ffffff",
            font=("Arial", 8, "bold"),
            relief="groove",
        )
        btn_cif.pack(side="left", padx=4)

        btn_desc = tk.Button(
            pnl_c,
            text="🔓 Descifrar Mensaje",
            command=lambda: self._cifrar_texto("descifrar"),
            bg="#dc3545",
            fg="#ffffff",
            font=("Arial", 8, "bold"),
            relief="groove",
        )
        btn_desc.pack(side="left", padx=4)

        self.txt_res_seg = tk.Text(parent, height=8, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid")
        self.txt_res_seg.pack(fill="both", expand=True)

    def _calc_hash(self):
        txt = self.e_pass.get().strip()
        self.txt_res_seg.delete("1.0", tk.END)

        res = generar_hashes_seguridad(txt)
        if "error" in res:
            self.txt_res_seg.insert(tk.END, f"⚠️ {res['error']}\n")
            return

        self.txt_res_seg.insert(tk.END, "🔐 HASHES DE SEGURIDAD:\n\n")
        self.txt_res_seg.insert(tk.END, f"• MD5: {res['md5']}\n")
        self.txt_res_seg.insert(tk.END, f"• SHA-1: {res['sha1']}\n")
        self.txt_res_seg.insert(tk.END, f"• SHA-256: {res['sha256']}\n")

    def _cifrar_texto(self, modo):
        txt = self.e_pass.get().strip()
        self.txt_res_seg.delete("1.0", tk.END)

        try:
            desplazamiento = int(self.e_shift.get().strip())
        except ValueError:
            messagebox.showerror("Error", "El desplazamiento debe ser un número entero.")
            return

        res = cifrado_cesar_simulado(txt, desplazamiento=desplazamiento, modo=modo)
        self.txt_res_seg.insert(tk.END, f"🔑 RESULTADO ({modo.upper()}):\n\n")
        self.txt_res_seg.insert(tk.END, f"{res['resultado']}\n")

    def _build_tab_protocolos(self, parent, panel_bg, fg_main, accent):
        pnl_proto = PanelBase(parent, titulo="📡 Guía de protocolos y puertos de red", bg_color=panel_bg)
        pnl_proto.pack(fill="both", expand=True)

        self.txt_res_proto = tk.Text(
            pnl_proto,
            font=("Arial", 10),
            bg="#ffffff",
            bd=1,
            relief="solid",
            wrap="word",
            state="disabled",
        )
        self.txt_res_proto.pack(fill="both", expand=True, padx=4, pady=4)

        contenido = ["📡 GUÍA DE PROTOCOLOS Y PUERTOS DE RED:\n"]
        for puerto, info in PUERTOS_Y_SERVICIOS_TIC.items():
            seguro_str = "🛡️ Cifrado / Seguro" if info.get("seguro") else "⚠️ Texto Plano / No Cifrado"
            contenido.append(f"📌 Puerto {puerto} ({info.get('protocolo')}) -> {info.get('servicio')} [{seguro_str}]\n")
            contenido.append(f" └─ {info.get('descripcion')}\n\n")

        self.txt_res_proto.configure(state="normal")
        self.txt_res_proto.insert(tk.END, "".join(contenido))
        self.txt_res_proto.configure(state="disabled")

    def _build_tab_glosario(self, parent, panel_bg, fg_main, accent):
        pnl_glo = PanelBase(parent, titulo="📚 Glosario de Conceptos Clave de TIC", bg_color=panel_bg)
        pnl_glo.pack(fill="both", expand=True)

        self.txt_glosario_tic = tk.Text(pnl_glo, font=("Consolas", 8), bg="#ffffff", bd=1, relief="solid")
        self.txt_glosario_tic.pack(fill="both", expand=True, padx=2, pady=2)
        self.txt_glosario_tic.insert(tk.END, "📚 CONCEPTOS FUNDAMENTALES DE TIC Y REDES:\n\n")

        for term, defn in DICCIONARIO_TIC.items():
            self.txt_glosario_tic.insert(tk.END, f"📌 {term}:\n {defn}\n\n")

