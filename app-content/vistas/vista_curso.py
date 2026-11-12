import tkinter as tk 
from tkinter import ttk, messagebox 

try: HAS_TKINTER = True 
except ImportError: HAS_TKINTER = False 

from .componentes_ui import PanelBase, CardButton 

try:
    from informacion_materias.docentes.docentes_manager import DocentesManager as _DocentesManager
except ImportError:
    class FallbackDocentesManager:
        def obtener_docente_materia(self, ciclo, anio, esp_o_div, materia):
            return {
                "nombre": "Docente a designar",
                "cursos": f"{anio}º Año {esp_o_div}",
                "telefono": "+54 3777 0000-0000",
                "email": "consultas@escuelatecnica.edu.ar",
                "horarios_tabla": [],
            }

        def asignar_docente(self, *args, **kwargs):
            return True

    _DocentesManager = FallbackDocentesManager

try: 
    from configuracion.config_manager import cargar_configuracion, aplicar_estilos_globales 
except ImportError: 
    import sys 
    from pathlib import Path 
    BASE_DIR = Path(__file__).resolve().parent.parent 
    if str(BASE_DIR) not in sys.path: 
        sys.path.insert(0, str(BASE_DIR)) 
    
from configuracion.config_manager import cargar_configuracion, aplicar_estilos_globales 

try: 
    from informacion_materias.docentes.docentes_ui import VistaDocentePage 
except ImportError: 
    VistaDocentePage = None 
        
# 🔑 REGISTRO CENTRALIZADO DE MATERIAS E ÍCONOS 
REGISTRO_MATERIAS = { "matematica": {"nombre": "Matemática", "icon": "📐", "modulo_path": "materias_generales.matematica"}, "lengua": {"nombre": "Lengua", "icon": "📝", "modulo_path": "materias_generales.lengua"}, "historia": {"nombre": "Historia", "icon": "📜", "modulo_path": "materias_generales.historia"}, "ingles": {"nombre": "Inglés", "icon": "🗣️", "modulo_path": "materias_generales.ingles"}, "ed_fisica": {"nombre": "Educación Física", "icon": "⚽", "modulo_path": "materias_generales.ed_fisica"}, "fisica": {"nombre": "Física", "icon": "⚡", "modulo_path": "materias_generales.fisica"}, "quimica": {"nombre": "Química", "icon": "🧪", "modulo_path": "materias_generales.quimica"}, "economia": {"nombre": "Economía", "icon": "📊", "modulo_path": "materias_generales.economia"}, "tecnologia": {"nombre": "Tecnología", "icon": "⚙️", "modulo_path": "materias_generales.tecnologia"}, "tic": {"nombre": "TIC", "icon": "💻", "modulo_path": "materias_generales.tic"}, "informatica": {"nombre": "Informática", "icon": "💻", "modulo_path": "materias_taller.informatica"}, "labs_programacion": {"nombre": "Labs. Programación", "icon": "💻", "modulo_path": "materias_taller.informatica.labs_programacion"}, "labs_hardware": {"nombre": "Labs. Hardware", "icon": "🖥️", "modulo_path": "materias_taller.informatica.labs_hardware"}, "labs_aplicaciones": {"nombre": "Labs. Aplicaciones", "icon": "📱", "modulo_path": "materias_taller.informatica.labs_aplicaciones"}, "labs_sistemas": {"nombre": "Labs. Sistemas", "icon": "🛠️", "modulo_path": "materias_taller.informatica.labs_sistemas"}, } 

def obtener_info_materia(nombre: str): 
    nom_lower = nombre.lower() 
    for key, info in REGISTRO_MATERIAS.items(): 
        if key in nom_lower or info["nombre"].lower() in nom_lower: 
            return key, info 
    return "materia_generica", {"nombre": nombre, "icon": "📖", "modulo_path": None}

COLORES_MATERIAS = { 
    "lengua": {"bg": "#d0ebff", "fg": "#1864ab"},
    "matematica": {"bg": "#ffe8cc", "fg": "#d9480f"},
    "historia": {"bg": "#f4e7ce", "fg": "#5f4b32"},
    "economia": {"bg": "#eebefa", "fg": "#862e9c"},
    "programacion": {"bg": "#d3f9d8", "fg": "#2b8a3e"},
    "hardware": {"bg": "#e9fac8", "fg": "#5c940d"},
    "sistemas": {"bg": "#e3fafc", "fg": "#0b7285"},
    "aplicaciones": {"bg": "#e8f5e9", "fg": "#1b5e20"},
    "fisica": {"bg": "#fff3bf", "fg": "#e67700"},
    "ingles": {"bg": "#ffc9c9", "fg": "#c92a2a"},
    "ed_fisica": {"bg": "#b2f2bb", "fg": "#2b8a3e"},
    "educacion_fisica": {"bg": "#b2f2bb", "fg": "#2b8a3e"},
    "educacion fisica": {"bg": "#b2f2bb", "fg": "#2b8a3e"},
    "tecnologia": {"bg": "#dbeafe", "fg": "#1d4ed8"},
    "tic": {"bg": "#dbe4ff", "fg": "#4338ca"},
    "quimica": {"bg": "#fee2e2", "fg": "#b91c1c"},
    "biologia": {"bg": "#dcfce7", "fg": "#166534"},
    "geografia": {"bg": "#fce7f3", "fg": "#9d174d"},
    "dibujo": {"bg": "#f3e8ff", "fg": "#7e22ce"},
    "taller": {"bg": "#e6ccb2", "fg": "#7f4f24"},
    "recreo": {"bg": "#e9ecef", "fg": "#495057"},
    "defecto": {"bg": "#ffffff", "fg": "#212529"},
    "libre": {"bg": "#ffffff", "fg": "#212529"},
} 

class VistaCursoUI(tk.Frame): 
    """Pantalla del Curso con Horarios Dinámicos por Turno (Mañana y Tarde) según Ciclo y Especialidad.""" 
    
    def __init__(self, parent=None, contexto: dict | None = None, on_materia_selected_callback=None, on_back_callback=None, on_docente_selected_callback=None): 
        if not HAS_TKINTER: 
            return 
        
        
        self.config_val = cargar_configuracion() 
        bg_main = self.config_val.get("bg_color", "#ffffff") 
        panel_bg = self.config_val.get("panel_bg", "#f8f9fa") 
        fg_main = self.config_val.get("fg_color", "#212529") 
        accent = self.config_val.get("accent_color", "#007acc") 
        super().__init__(parent, bg=bg_main) 
        self.pack(fill="both", expand=True) 
        self.contexto = contexto or {} 
        self.on_materia_click = on_materia_selected_callback 
        self.on_back = on_back_callback 
        self.on_docente_click = on_docente_selected_callback
        self.manager = _DocentesManager()
        self.horario_matriz = self._obtener_horario_base() 
        
        # 📜 Contenedor Canvas y Scrollbar Único 
        self.canvas = tk.Canvas(self, bg=bg_main, highlightthickness=0, bd=0) 
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview) 
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg_main, padx=14, pady=12)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw") 
        
        def _update_scroll_region(event=None): 
            self.canvas.configure(scrollregion=self.canvas.bbox("all")) 
            
        def _on_canvas_configure(event): 
            self.canvas.itemconfig(self.canvas_window, width=event.width) 
            _update_scroll_region() 
            
        self.canvas.bind("<Configure>", _on_canvas_configure) 
        self.scrollable_frame.bind("<Configure>", _update_scroll_region) 
        self.canvas.configure(yscrollcommand=self.scrollbar.set) 
        self.canvas.pack(side="left", fill="both", expand=True) 
        self.scrollbar.pack(side="right", fill="y") 
        
        # Construcción de la UI dentro del marco scrollable 
        self._build_ui(self.scrollable_frame, bg_main=bg_main, panel_bg=panel_bg, fg_main=fg_main, accent=accent) 
        # Aplicar tema global y renderizar tabla al final 
        aplicar_estilos_globales(self, self.config_val) 
        self._renderizar_tabla_horario_grid() 

    def _obtener_materias_por_contexto(self) -> list: 
        if self.contexto.get("lista_materias"): 
            return self.contexto["lista_materias"] 
        
        ciclo = self.contexto.get("ciclo", "Ciclo Básico") 
        especialidad = self.contexto.get("especialidad", "Informática") 
        
        if ciclo == "Ciclo Avanzado" and especialidad == "Informática": 
            return [ "Historia", "Matemática", "Economía", "Tecnología", "TIC", "Física", "Inglés", "Lengua", "Labs. Programación", "Labs. Hardware", "Labs. Aplicaciones", "Labs. Sistemas", "Educación Física" ] 
        else: return ["Lengua", "Matemática", "Historia", "Inglés", "Educación Física", "Física", "Química", "Biología", "Geografía", "Dibujo Técnico", "Tecnología", "Taller"]

        return materias

    def _al_hacer_clic_materia(self, materia):
        if isinstance(materia, str):
            contexto_materia = {**self.contexto, "materia": materia, "modulo_central": materia}
        else:
            contexto_materia = {**self.contexto, **(materia or {})}

        if self.on_materia_click:
            self.on_materia_click(contexto_materia)

    def _build_seccion_docentes(self, parent_frame, accent, panel_bg, fg_main, bg_main, materias_lista): 
        """ Construye la sección de docentes con una grilla de botones interactivos para TODAS las materias del curso. """ 
        
        pnl_docentes = PanelBase(parent_frame, titulo="👨‍🏫 Equipo Docente del Curso", bg_color=panel_bg) 
        pnl_docentes.configure(fg=accent, bg=panel_bg) 
        pnl_docentes.pack(fill="x", pady=(0, 12)) 
        
        top_doc_frame = tk.Frame(pnl_docentes, bg=panel_bg) 
        top_doc_frame.pack(fill="x", pady=(0, 6)) 
        
        tk.Label( top_doc_frame, text="Haz clic en cualquier asignatura o docente para abrir su ficha interactiva:", font=("Arial", 8, "italic"), bg=panel_bg, fg=fg_main ).pack(side="left", anchor="w") 
        grid_doc = tk.Frame(pnl_docentes, bg=panel_bg) 
        grid_doc.pack(fill="x", expand=True) 
        
        # Contexto del curso actual 
        ciclo = self.contexto.get("ciclo", "Ciclo Básico") 
        anio = self.contexto.get("anio", 1) 
        esp_div = str((self.contexto.get("division") if ciclo == "Ciclo Básico" else self.contexto.get("especialidad", "A")) or "A") 
        
        # Grilla de 3 columnas para todas las materias 
        cols = 3 
        for i, mat in enumerate(materias_lista): 
            r = i // cols 
            c = i % cols 
            
            # Obtener datos persistidos del docente desde el manager 
            doc_info = self.manager.obtener_docente_materia(ciclo, anio, esp_div, mat) 
            nombre_prof = doc_info.get("nombre", "Docente a designar") 
            
            _, info_mat = obtener_info_materia(mat) 
            icon = info_mat.get("icon", "📖") 
            
            # Botón interactivo por materia/docente 
            btn_doc = tk.Button( grid_doc, text=f"{icon} {mat}: {nombre_prof}", command=lambda m=mat: self._abrir_ficha_docente_materia(m), bg="#ffffff", fg=fg_main, font=("Arial", 8, "bold"), relief="groove", bd=1, padx=6, pady=4, cursor="hand2", anchor="w", justify="left" ) 
            btn_doc.grid(row=r, column=c, padx=4, pady=3, sticky="nsew") 
            
        for c in range(cols): 
            grid_doc.columnconfigure(c, weight=1) 
            
    def _abrir_ficha_docente_materia(self, materia_nombre: str): 
        """Abre la ficha del docente dentro de la misma vista de contenido, sin pop-up.""" 
        ctx_docente = dict(self.contexto)
        ctx_docente["materia"] = materia_nombre

        if self.on_docente_click:
            self.on_docente_click(ctx_docente)
            return

        if not VistaDocentePage:
            messagebox.showinfo("Docentes", f"Ficha del docente para {materia_nombre}.")
            return

        for child in list(self.winfo_children()):
            child.destroy()

        def _cerrar_y_recargar():
            self._recargar_vista_curso()

        VistaDocentePage(self, contexto=ctx_docente, on_back_callback=_cerrar_y_recargar)

    def _abrir_pantalla_docentes(self, materia_nombre="Matemática"): 
        ctx_docente = dict(self.contexto)
        ctx_docente["materia"] = materia_nombre

        if self.on_docente_click:
            self.on_docente_click(ctx_docente)
            return

        if not VistaDocentePage:
            messagebox.showinfo("Docentes", "Módulo de gestión de docentes conectado.")
            return

        for child in list(self.winfo_children()):
            child.destroy()

        def _cerrar_y_recargar():
            self._recargar_vista_curso()

        VistaDocentePage(self, contexto=ctx_docente, on_back_callback=_cerrar_y_recargar)
            
    def _recargar_vista_curso(self): 
        """Reconstruye la vista del curso al regresar desde la Ficha Docente."""
        for child in list(self.winfo_children()):
            child.destroy()

        self.config_val = cargar_configuracion()
        bg_main = self.config_val.get("bg_color", "#ffffff")
        panel_bg = self.config_val.get("panel_bg", "#f8f9fa")
        fg_main = self.config_val.get("fg_color", "#212529")
        accent = self.config_val.get("accent_color", "#007acc")

        self.configure(bg=bg_main)
        self.horario_matriz = self._obtener_horario_base()

        self.canvas = tk.Canvas(self, bg=bg_main, highlightthickness=0, bd=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg_main, padx=14, pady=12)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        def _update_scroll_region(event=None):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        def _on_canvas_configure(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)
            _update_scroll_region()

        self.canvas.bind("<Configure>", _on_canvas_configure)
        self.scrollable_frame.bind("<Configure>", _update_scroll_region)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self._build_ui(self.scrollable_frame, bg_main=bg_main, panel_bg=panel_bg, fg_main=fg_main, accent=accent)
        aplicar_estilos_globales(self, self.config_val)
        self._renderizar_tabla_horario_grid()

    def _build_seccion_horarios_colorida(self, parent_frame, accent, panel_bg, fg_main, materias_lista):
        """Crea el bloque de tabla de horarios y la renderiza."""
        self.frame_tabla_grid = tk.Frame(parent_frame, bg=panel_bg, padx=4, pady=4)
        self.frame_tabla_grid.pack(fill="x", pady=(0, 12))
        self._renderizar_tabla_horario_grid()

    def _build_ui(self, parent_frame, bg_main="#ffffff", panel_bg="#f8f9fa", fg_main="#212529", accent="#007acc"): 
        ciclo = self.contexto.get("ciclo", "Ciclo Básico") 
        anio = self.contexto.get("anio", 1) 
        division = self.contexto.get("division", "A") 
        especialidad = self.contexto.get("especialidad", "Informática") 
        
        # 1. 🔝 Encabezado del Curso (Empaquetado arriba de todo) 
        header_frame = tk.Frame(parent_frame, bg=accent, padx=12, pady=8, bd=1, relief="solid") 
        header_frame.pack(side="top", fill="x", pady=(0, 10)) 
        
        titulo_curso = f"🏫 {anio}º Año - División '{division}'" if ciclo == "Ciclo Básico" else f"🏫 {anio}º Año - Especialidad en {especialidad}" 
        subtitulo_curso = "Ciclo Básico Técnico (1º a 3º Año)" if ciclo == "Ciclo Básico" else "Ciclo Avanzado Profesional (4º a 7º Año)"
        tk.Label(header_frame, text=titulo_curso, font=("Arial", 12, "bold"), fg="#ffffff", bg=accent, justify="left").pack(anchor="w", fill="x") 
        tk.Label(header_frame, text=subtitulo_curso, font=("Arial", 8, "bold"), fg="#edf7ff", bg=accent, justify="left").pack(anchor="w", fill="x") 
        
        # 2. Información General 
        pnl_info = PanelBase(parent_frame, titulo="📋 Información General del Curso", bg_color=panel_bg) 
        pnl_info.configure(fg=accent, bg=panel_bg) 
        pnl_info.pack(side="top", fill="x", pady=(0, 12)) 
        info_txt = ( 
            f"• Preceptor/Tutor del Curso: Prof. A designar por Dirección Escolar\n" 
            f"• Modalidad: Técnico Secundaria en {especialidad if ciclo == 'Ciclo Avanzado' else 'Ciclo Básico'}\n" 
            f"• Régimen Horario: Turno Mañana y Turno Tarde con Salida a Domicilio intermedia." 
        ) 
        tk.Label(pnl_info, text=info_txt, font=("Arial", 8), bg=panel_bg, fg=fg_main, justify="left").pack(anchor="w", pady=2, fill="x") 
        
        # 3. Asignaturas Disponibles 
        tk.Label(parent_frame, text="📚 Asignaturas Disponibles (Haz clic para ingresar):", font=("Arial", 10, "bold"), fg=accent, bg=bg_main).pack(anchor="w", side="top", pady=(0, 6), fill="x") 
        materias_lista = self._obtener_materias_por_contexto() 
        
        frame_materias_grid = tk.Frame(parent_frame, bg=panel_bg, padx=4, pady=4) 
        frame_materias_grid.pack(side="top", fill="x", pady=(0, 16)) 
        col_max = 4 
        for idx, mat in enumerate(materias_lista): 
            row = idx // col_max 
            col = idx % col_max 
            
            _, info = obtener_info_materia(mat) 
            btn_mat = CardButton( frame_materias_grid, text=mat, command=lambda m=mat: self._al_hacer_clic_materia(m), icon=info.get("icon", "📖"), bg=panel_bg, fg=accent ) 
            btn_mat.grid(row=row, column=col, padx=4, pady=4, sticky="nsew") 
        for c in range(col_max): 
            frame_materias_grid.columnconfigure(c, weight=1) 
        
        # 4 y 5. Docentes y Horarios 
        self._build_seccion_docentes(parent_frame, accent, panel_bg, fg_main, bg_main, materias_lista) 
        self._build_seccion_horarios_colorida(parent_frame, accent, panel_bg, fg_main, materias_lista)
                               
    def _obtener_estilo_materia(self, nombre: str):
        """Devuelve estilo visual según la materia o franja del horario."""
        nombre_limpio = (nombre or "").strip()
        nombre_norm = nombre_limpio.lower()
        nombre_norm = nombre_norm.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ü", "u")
        nombre_norm = nombre_norm.replace("-", " ").replace("_", " ").replace(".", " ")
        nombre_norm = "".join(ch for ch in nombre_norm if ch.isalnum() or ch.isspace())
        nombre_norm = " ".join(nombre_norm.split())

        if not nombre_norm or nombre_norm in {"---", ""}:
            return {"bg": "#ffffff", "fg": "#212529"}

        if "recreo" in nombre_norm or "almuerzo" in nombre_norm:
            return {"bg": "#e9ecef", "fg": "#495057"}

        for clave, estilo in COLORES_MATERIAS.items():
            clave_norm = clave.lower()
            clave_norm = clave_norm.replace("á", "a").replace("é", "e").replace("í", "i").replace("ó", "o").replace("ú", "u").replace("ü", "u")
            clave_norm = clave_norm.replace("-", " ").replace("_", " ").replace(".", " ")
            clave_norm = "".join(ch for ch in clave_norm if ch.isalnum() or ch.isspace())
            clave_norm = " ".join(clave_norm.split())
            if clave_norm in nombre_norm or clave_norm in nombre_norm.replace(" ", "") or nombre_norm.replace(" ", "") in clave_norm or clave_norm in nombre_norm.replace(" ", ""):
                return estilo

        if "labs" in nombre_norm:
            return {"bg": "#d3f9d8", "fg": "#2b8a3e"}

        if "taller" in nombre_norm:
            return {"bg": "#e6ccb2", "fg": "#7f4f24"}

        return {"bg": "#ffffff", "fg": "#212529"}

    def _obtener_horario_base(self): 
        ciclo = self.contexto.get("ciclo", "Ciclo Básico") 
        especialidad = self.contexto.get("especialidad", "Informática")

        if ciclo == "Ciclo Avanzado" and especialidad == "Informática":
            return [
                {"bloque": "🌅 07:00 - 07:40 (M1)", "lunes": "---", "martes": "---", "miercoles": "---", "jueves": "Labs. Sistemas", "viernes": "Labs. Aplicaciones"},
                {"bloque": "🌅 07:40 - 08:20 (M2)", "lunes": "---", "martes": "---", "miercoles": "---", "jueves": "Labs. Sistemas", "viernes": "Labs. Hardware"},
                {"bloque": "☕ Recreo (08:20 - 08:30)", "lunes": "RECREO", "martes": "RECREO", "miercoles": "RECREO", "jueves": "RECREO", "viernes": "RECREO"},
                {"bloque": "🌅 08:30 - 09:10 (M3)", "lunes": "---", "martes": "---", "miercoles": "Labs. Programación", "jueves": "Labs. Sistemas", "viernes": "Labs. Hardware"},
                {"bloque": "🌅 09:10 - 09:50 (M4)", "lunes": "---", "martes": "---", "miercoles": "Labs. Programación", "jueves": "Labs. Aplicaciones", "viernes": "Labs. Hardware"},
                {"bloque": "🌅 09:50 - 10:30 (M5)", "lunes": "---", "martes": "---", "miercoles": "Labs. Programación", "jueves": "Labs. Aplicaciones", "viernes": "---"},
                {"bloque": "🏠 Salida a Domicilio (11:00 - 14:00)", "lunes": "SALIDA A DOMICILIO", "martes": "SALIDA A DOMICILIO", "miercoles": "SALIDA A DOMICILIO", "jueves": "SALIDA A DOMICILIO", "viernes": "SALIDA A DOMICILIO"},
                {"bloque": "🌆 14:00 - 14:40 (T1)", "lunes": "Economía", "martes": "TIC", "miercoles": "Historia", "jueves": "Tecnología", "viernes": "TIC"},
                {"bloque": "🌆 14:40 - 15:20 (T2)", "lunes": "Economía", "martes": "TIC", "miercoles": "Historia", "jueves": "Tecnología", "viernes": "TIC"},
                {"bloque": "☕ Recreo (15:20 - 15:30)", "lunes": "RECREO", "martes": "RECREO", "miercoles": "RECREO", "jueves": "RECREO", "viernes": "RECREO"},
                {"bloque": "🌆 15:30 - 16:10 (T3)", "lunes": "Matemática", "martes": "Economía", "miercoles": "Inglés", "jueves": "Lengua", "viernes": "Inglés"},
                {"bloque": "🌆 16:10 - 16:50 (T4)", "lunes": "Historia", "martes": "Economía", "miercoles": "Matemática", "jueves": "Lengua", "viernes": "Inglés"},
                {"bloque": "☕ Recreo (16:50 - 17:00)", "lunes": "RECREO", "martes": "RECREO", "miercoles": "RECREO", "jueves": "RECREO", "viernes": "RECREO"},
                {"bloque": "🌆 17:00 - 17:40 (T5)", "lunes": "Tecnología", "martes": "Física", "miercoles": "Matemática", "jueves": "Matemática", "viernes": "Física"},
                {"bloque": "🌆 17:40 - 18:20 (T6)", "lunes": "Tecnología", "martes": "Física", "miercoles": "Matemática", "jueves": "Matemática", "viernes": "Física"},
            ]

        return [
            {"bloque": "🌅 07:00 - 07:40 (M1)", "lunes": "Lengua", "martes": "Matemática", "miercoles": "Historia", "jueves": "Inglés", "viernes": "Tecnología"},
            {"bloque": "🌅 07:40 - 08:20 (M2)", "lunes": "Matemática", "martes": "Lengua", "miercoles": "Inglés", "jueves": "Historia", "viernes": "Física"},
            {"bloque": "☕ Recreo (08:20 - 08:30)", "lunes": "RECREO", "martes": "RECREO", "miercoles": "RECREO", "jueves": "RECREO", "viernes": "RECREO"},
            {"bloque": "🌅 08:30 - 09:10 (M3)", "lunes": "Historia", "martes": "Economía", "miercoles": "Tecnología", "jueves": "Matemática", "viernes": "Inglés"},
            {"bloque": "🌅 09:10 - 09:50 (M4)", "lunes": "Física", "martes": "Tecnología", "miercoles": "Matemática", "jueves": "Lengua", "viernes": "Historia"},
            {"bloque": "🏠 Salida a Domicilio (11:00 - 14:00)", "lunes": "SALIDA A DOMICILIO", "martes": "SALIDA A DOMICILIO", "miercoles": "SALIDA A DOMICILIO", "jueves": "SALIDA A DOMICILIO", "viernes": "SALIDA A DOMICILIO"},
            {"bloque": "🌆 14:00 - 14:40 (T1)", "lunes": "Lengua", "martes": "Historia", "miercoles": "Matemática", "jueves": "Economía", "viernes": "TIC"},
            {"bloque": "🌆 14:40 - 15:20 (T2)", "lunes": "Inglés", "martes": "Tecnología", "miercoles": "Economía", "jueves": "Física", "viernes": "Matemática"},
            {"bloque": "☕ Recreo (15:20 - 15:30)", "lunes": "RECREO", "martes": "RECREO", "miercoles": "RECREO", "jueves": "RECREO", "viernes": "RECREO"},
            {"bloque": "🌆 15:30 - 16:10 (T3)", "lunes": "Tecnología", "martes": "Física", "miercoles": "Lengua", "jueves": "Matemática", "viernes": "Economía"},
            {"bloque": "🌆 16:10 - 16:50 (T4)", "lunes": "Historia", "martes": "Inglés", "miercoles": "Tecnología", "jueves": "Lengua", "viernes": "Física"},
        ]

    def _renderizar_tabla_horario_grid(self): 
        setattr(self.frame_tabla_grid, "_skip_theme", True)
        for w in self.frame_tabla_grid.winfo_children(): 
            w.destroy() 
            
        dias = ["Franja / Horario", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes"] 
        
        header_bg = self.config_val.get("accent_color", "#2563eb")
        for c, dia in enumerate(dias): 
            lbl_h = tk.Label(self.frame_tabla_grid, text=dia, font=("Arial", 8, "bold"), bg=header_bg, fg="#ffffff", padx=4, pady=4, bd=1, relief="solid")
            setattr(lbl_h, "_skip_theme", True)
            lbl_h.grid(row=0, column=c, sticky="nsew")

        # ⏰ DIBUJAR COLUMNA DE HORAS (Columna 0) 
        for r, fila in enumerate(self.horario_matriz, start=1):
            es_salida = "SALIDA" in fila["bloque"].upper() or "DOMICILIO" in fila["bloque"].upper()
            lbl_bloque = tk.Label(
                self.frame_tabla_grid,
                text=fila["bloque"],
                font=("Arial", 7, "bold"),
                bg="#dbeafe" if not es_salida else "#cfe2ff",
                fg="#1e3a8a" if not es_salida else "#0f172a",
                padx=4,
                pady=3,
                bd=1,
                relief="solid",
                wraplength=130,
                justify="center",
            )
            setattr(lbl_bloque, "_skip_theme", True)
            lbl_bloque.grid(row=r, column=0, sticky="nsew")
        
        # Celdas por día (Columnas 1 a 5) 
        dias_keys = ["lunes", "martes", "miercoles", "jueves", "viernes"] 
        num_filas = len(self.horario_matriz) 
        
        for col_idx, k in enumerate(dias_keys, start=1): 
            r_idx = 0 
            while r_idx < num_filas: 
                mat_nombre = self.horario_matriz[r_idx].get(k, "---") 
                
                span = 1 
                if mat_nombre not in ["RECREO", "SALIDA A DOMICILIO", "---", ""]: 
                    while (r_idx + span < num_filas and self.horario_matriz[r_idx + span].get(k) == mat_nombre): 
                        span += 1 
                        
                estilo = self._obtener_estilo_materia(mat_nombre) 
                grid_row = r_idx + 1 
                lbl_celda = tk.Label( self.frame_tabla_grid, text=mat_nombre, font=("Arial", 8, "bold" if "RECREO" not in mat_nombre and "SALIDA" not in mat_nombre else "normal"), bg=estilo["bg"], fg=estilo["fg"], padx=2, pady=3, bd=1, relief="solid", wraplength=110, justify="center" ) 
                setattr(lbl_celda, "_skip_theme", True)
                lbl_celda.grid(row=grid_row, column=col_idx, rowspan=span, sticky="nsew") 
                
                r_idx += span 
        
        # 🎯 Reserva de 140px fijos para la columna 0 (Horas) 
        self.frame_tabla_grid.columnconfigure(0, weight=0, minsize=140) 
        for c in range(1, 6): 
            self.frame_tabla_grid.columnconfigure(c, weight=1, uniform="hor_col") 
        for r in range(num_filas + 1): 
            self.frame_tabla_grid.rowconfigure(r, weight=1)