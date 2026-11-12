import tkinter as tk 
from tkinter import ttk, messagebox 

try: 
    HAS_TKINTER = True 
except ImportError: 
    HAS_TKINTER = False 
    
from .componentes_ui import PanelBase, CardButton 

try: 
    from configuracion.config_manager import cargar_configuracion, aplicar_estilos_globales 
except ImportError: 
    import sys 
    from pathlib import Path 
    
    BASE_DIR = Path(__file__).resolve().parent.parent 
    if str(BASE_DIR) not in sys.path: 
        sys.path.insert(0, str(BASE_DIR)) 
        
from configuracion.config_manager import cargar_configuracion, aplicar_estilos_globales 
# 📚 MALLA CURRICULAR COMPLETA DEL PROYECTO TÉCNICO 
MALLA_CURRICULAR = { 
    "Ciclo Básico": { 
        "1": [ 
            "Lengua", "Artística", "Ética y Ciudadana", "Tecnología", "Inglés", 
            "Historia", "Biología", "Geografía", "Dibujo Técnico", "Matemática", 
            "Educación Física", "Ajuste 1", "Carpintería 1", "Electricidad 1", "Computación 1" 
        ], 
        "2": [ 
            "Geografía", "Dibujo Técnico", "Física", "Matemática", "Tecnología", 
            "Inglés", "Historia", "Ética y Ciudadana", "Biología", "Lengua", 
            "Artística", "Educación Física", "Ajuste y Electricidad 2", "Carpintería 2", 
            "Herrería y Soldadura 2", "Computación 2" 
        ], 
        "3": [ 
            "Artística", "Química", "Geografía", "Tecnología", "Lengua", 
            "Física", "Matemática", "Dibujo Técnico", "Historia", "Ética y Ciudadana", 
            "Educación Física", "Máquinas y Herramientas", "Construcciones", "Electricidad 3", "Computación y Electrónica" 
        ] 
    }, 
    "Ciclo Avanzado": { 
        "4": { 
            "Informática": [ 
                "Historia", "Matemática", "Economía", "Tecnología", "TIC", 
                "Física", "Inglés", "Lengua", "Labs. Programación", "Labs. Hardware", 
                "Labs. Aplicaciones", "Labs. Sistemas", "Educación Física" 
            ], 
            "Electrónica": [ 
                "Matemática", "Química", "Historia", "Economía", "Tecnología", 
                "Lengua", "Inglés", "Física", "Educación Física", "Montajes de Proyectos Electrónicos", 
                "Aplicaciones de Electrónica Analógica 1", "Aplicaciones de Electrónica Digital" 
            ], 
            "Electromecánica": [ 
                "Historia", "Matemática", "Química", "Física", "Lengua", 
                "Tecnología", "Inglés", "Economía", "Educación Física", "Instalaciones Eléctricas", 
                "Diseño y Procesamiento Mecánico", "Representación Gráfica" 
            ], 
            "Construcciones": [ 
                "Historia", "Matemática", "Inglés", "Lengua", "Materiales en Construcción", 
                "Economía", "Física", "Química", "Educación Física", "Introducción al Proyecto", 
                "Representación Gráfica e Interpretación de Planos", "Tecnología Aplicada a la Construcción" 
            ] 
        }, 
        "5": { 
            "Informática": [ 
                "Sistemas Digitales 1", "Lengua", "TIC 2", "Cultura Emprendedora", "Seguridad e Higiene", 
                "Análisis Matemático", "Geografía Económica y Regional", "Inglés", "Educación Física", "Labs. Hardware", 
                "Labs. Sistemas 2", "Labs. Programación 2", "Labs. Aplicaciones" 
            ], 
            "Electrónica": [ 
                "Cultura Emprendedora", "Tecnología", "Análisis Matemático", "Análisis de Modelos Circuitales", "Geografía Económica y Regional", 
                "Labs. Mediciones Eléctricas 1", "Inglés", "Lenguajes Electrónicos", "Lengua", "Educación Física", 
                "Aplicaciones de la Electrónica Analógica 2", "Diseño Asistido y Simulación Electrónica", "Montaje de Proyectos Electrónicos 2" 
            ], 
            "Electromecánica": [ 
                "Labs. Mediciones Eléctricas 1", "Electromecánica 1", "Geografía Económica y Regional", "Mecánica Técnica", "Análisis Matemático", 
                "Cultura Emprendedora", "Inglés", "Lengua", "Educación Física", "Ensayo de Componentes Electromecánicos", 
                "Diseño y Procesamiento Mecánico 2", "Ensayo de Materiales" 
            ], 
            "Construcciones": [ 
                "Proyecto 1", "Estática y Resistencia de Materiales", "Cultura Emprendedora", "Instalaciones Electromecánicas", "Geografía Económica y Regional", 
                "Análisis Matemático", "Legislación de la Construcción", "Fundaciones y Albañilería", "Inglés", "Lengua", 
                "Educación Física", "Sistemas Constructivos", "Cálculo de Estructuras 1" 
            ] 
        }, 
        "6": { 
            "Informática": [ 
                "Seguridad Informática", "Sistemas Digitales 2", "Estadística y Probabilidad", "Gestión Organizacional", "Base de Datos 1", 
                "Inglés", "Comercialización de Productos y Sistemas Informáticos", "Lengua", "Educación Física", "Labs. Programación 3", 
                "Labs. Hardware 3", "Labs. Redes 3", "Labs. Sistemas 3" 
            ], 
            "Electrónica": [ 
                "Estadística y Probabilidad", "Labs. Mediciones Eléctricas 2", "Lengua", "Máquinas Eléctricas", "Inglés", 
                "Gestión Organizacional", "Derechos del Trabajo", "Sistemas de Comunicaciones 1", "Educación Física", "Montaje de Proyectos Electrónicos 3", 
                "Aplicaciones de la Electrónica Analógica 3", "Lenguaje Electrónico 3", "Aplicaciones de la Electrónica Digital 3" 
            ], 
            "Electromecánica": [ 
                "Sistemas Mecánicos 1", "Gestión Organizacional", "Electromecánica 2", "Estadística y Probabilidad", "Inglés", 
                "Máquinas Térmicas", "Labs. Mediciones Eléctricas 2", "Lengua", "Educación Física", "Ensayo en Equipos Electromecánicos", 
                "Montaje Electromecánico", "CNC", "CAD-CAM" 
            ], 
            "Construcciones": [ 
                "Estadística y Probabilidad", "Proyecto 2", "Construcciones Metálicas y de Madera", "Construcciones Complementarias", "Instalaciones Sanitarias", 
                "Instalaciones de Gas", "Gestión Organizacional", "Inglés", "Lengua", "Educación Física", 
                "Cálculo de Estructuras 2", "Sistemas Constructivos 2" 
            ] 
        }, 
        "7": { 
            "Informática": [ 
                "Política y Ciudadanía", "Derechos del Trabajo", "Modelos y Sistemas", "Base de Datos 2", "Álgebra Lineal", "Prácticas Profesionalizantes", 
                "Educación Física", "Diseño e Implementación de Sistemas Computacionales", "Instalación, Mantenimiento y Reparación de Sistemas Computacionales" 
            ], 
            "Electrónica": [ 
                "Seguridad e Higiene Industrial", "Política y Ciudadanía", "Sistemas de Comunicaciones 2", "Prácticas Profesionalizantes", 
                "Educación Física", "Control Electrónico de Procesos Industriales", "Electrónica Industrial", "Electrónica Aplicada" 
            ], 
            "Electromecánica": [ 
                "Control de Procesos Industriales", "Derechos del Trabajo", "Política y Ciudadanía", "Seguridad, Higiene y Protección Ambiental", 
                "Sistemas Mecánicos 2", "Educación Física", "Labs. Metrología y Control de Calidad", "Mantenimiento Electromecánico" 
            ], 
            "Construcciones": [ 
                "Proyecto 3", "Prácticas Profesionalizantes", "Instalaciones Térmicas", "Política y Ciudadanía", "Topografía y Obras Viales", 
                "Cómputo y Presupuesto", "Educación Física", "Ejercicio Legal de la Profesión", "Proyecto y Dirección de Instalaciones", "Dirección de Obras" 
            ] 
        } 
    } 
} 
    
class VistaCursoUI(tk.Frame): 
    """Pantalla genérica que renderiza las materias específicas de cualquier curso/especialidad.""" 
    
    def __init__(self, parent, contexto: dict, on_materia_selected_callback, on_back_callback=None): 
        self.config_val = cargar_configuracion() 
        bg_main = self.config_val.get("bg_color", "#ffffff") 
        panel_bg = self.config_val.get("panel_bg", "#f8f9fa") 
        fg_main = self.config_val.get("fg_color", "#212529") 
        accent = self.config_val.get("accent_color", "#007acc") 
        
        super().__init__(parent, bg=bg_main, padx=20, pady=20) 
        self.pack(fill="both", expand=True) 
        self.contexto = contexto or {} 
        self.on_materia_click = on_materia_selected_callback 
        self.on_back = on_back_callback 
        self._build_ui(bg_main=bg_main, panel_bg=panel_bg, fg_main=fg_main, accent=accent) 
        aplicar_estilos_globales(self, self.config_val) 
        
    def _obtener_materias_por_contexto(self) -> list: 
        """Determina automáticamente qué asignaturas mostrar según la selección.""" 
        if self.contexto.get("lista_materias"): 
            return self.contexto["lista_materias"] 
        
        ciclo = self.contexto.get("ciclo", "Ciclo Básico") 
        anio = str(self.contexto.get("anio", 1)) 
        especialidad = self.contexto.get("especialidad", "Informática") 
        if ciclo == "Ciclo Básico": 
            return MALLA_CURRICULAR.get("Ciclo Básico", {}).get( anio, ["Lengua", "Matemática", "Historia", "Inglés", "Educación Física"] ) 
        else: 
            return MALLA_CURRICULAR.get("Ciclo Avanzado", {}).get(anio, {}).get( especialidad, ["Lengua", "Matemática", "Historia", "Inglés", "Educación Física"] ) 

    def _mapear_materia_a_modulo(self, materia: str) -> str:
        """Devuelve la clave del módulo asociado a una materia conocida."""
        m_lower = (materia or "").lower()
        if "lengua" in m_lower:
            return "lengua"
        if "matemát" in m_lower or "algebra" in m_lower or "álgebra" in m_lower or "calculo" in m_lower:
            return "matematica"
        if "histor" in m_lower:
            return "historia"
        if "químic" in m_lower or "quimic" in m_lower:
            return "quimica"
        if "físic" in m_lower or "fisic" in m_lower:
            return "fisica"
        if "inglés" in m_lower or "ingles" in m_lower:
            return "ingles"
        if "econ" in m_lower:
            return "economia"
        if "programaci" in m_lower:
            return "programacion"
        return "materia_generica"

    def _al_hacer_clic_materia(self, materia: str):
        """Notifica la materia seleccionada al callback principal de la app."""
        if self.on_materia_click is None:
            return
        contexto = dict(self.contexto)
        contexto["materia"] = materia
        contexto["modulo_central"] = self._mapear_materia_a_modulo(materia)
        self.on_materia_click(contexto)
        
    def _build_ui(self, bg_main="#ffffff", panel_bg="#f8f9fa", fg_main="#212529", accent="#007acc"): 
        # 1. Crear Canvas y Scrollbar Vertical 
        self.canvas = tk.Canvas(self, bg=bg_main, highlightthickness=0, bd=0) 
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview) 
        # 2. Contenedor interno desplazable 
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg_main, padx=12, pady=10) 
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw") 
        
        # Ajuste dinámico del alto y ancho del scroll 
        def _update_scroll_region(event=None): 
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        def _on_canvas_configure(event): 
            self.canvas.itemconfig(self.canvas_window, width=event.width) 

        self.scrollable_frame.bind("<Configure>", _update_scroll_region)
        self.canvas.bind("<Configure>", _on_canvas_configure)
        self.canvas.configure(yscrollcommand=self.scrollbar.set) 
        
        self.canvas.pack(side="left", fill="both", expand=True) 
        self.scrollbar.pack(side="right", fill="y") 
        
        # Soporte para Rueda de Mouse (MouseWheel) 
        def _on_mousewheel(event): 
            if event.delta: 
                self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units") 
            elif event.num == 4: 
                self.canvas.yview_scroll(-2, "units") 
            elif event.num == 5: 
                self.canvas.yview_scroll(2, "units")

        def _enable_mousewheel(event):
            widget = event.widget
            widget.bind("<MouseWheel>", _on_mousewheel)
            widget.bind("<Button-4>", _on_mousewheel)
            widget.bind("<Button-5>", _on_mousewheel)

        def _disable_mousewheel(event):
            widget = event.widget
            widget.unbind("<MouseWheel>")
            widget.unbind("<Button-4>")
            widget.unbind("<Button-5>")

        self.canvas.bind("<Enter>", _enable_mousewheel)
        self.canvas.bind("<Leave>", _disable_mousewheel)

        ciclo = self.contexto.get("ciclo", "Ciclo Básico") 
        anio = self.contexto.get("anio", 1) 
        division = self.contexto.get("division", "A") 
        especialidad = self.contexto.get("especialidad", "Informática") 
        
        # 1. Encabezado del Curso 
        header_frame = tk.Frame(self.scrollable_frame, bg=accent, padx=12, pady=8, bd=1, relief="solid") 
        header_frame.pack(fill="x", pady=(0, 16)) 
        
        if ciclo == "Ciclo Básico": 
            titulo_curso = f"🏫 {anio}º Año - División '{division}'" 
            subtitulo_curso = "Ciclo Básico Técnico (1º a 3º Año)" 
        else: 
            titulo_curso = f"🏫 {anio}º Año - Especialidad en {especialidad}" 
            subtitulo_curso = "Ciclo Avanzado Profesional (4º a 7º Año)" 
            
        tk.Label(header_frame, text=titulo_curso, font=("Arial", 14, "bold"), fg="#ffffff", bg=accent, justify="left").pack(anchor="w", fill="x") 
        tk.Label(header_frame, text=subtitulo_curso, font=("Arial", 9, "bold"), fg="#edf7ff", bg=accent, justify="left").pack(anchor="w", fill="x") 
        
        # 2. Información del Curso 
        pnl_info = PanelBase(self, titulo="📋 Información General del Curso & Equipo Docente", bg_color=panel_bg) 
        pnl_info.configure(fg=accent, bg=panel_bg) 
        pnl_info.pack(fill="x", pady=(0, 16)) 
        info_txt = ( 
            f"• Preceptor/Tutor del Curso: A designar por Dirección Escolarn" 
            f"• Modalidad: Técnico Secundaria en {especialidad if ciclo == 'Ciclo Avanzado' else 'Ciclo Básico'}n" 
            f"• Malla Curricular: Conectada dinámicamente con 'informacion_materias/docentes/' y 'temarios/'" 
            ) 
        tk.Label(pnl_info, text=info_txt, font=("Arial", 9), bg=panel_bg, fg=fg_main, justify="left").pack(anchor="w", pady=4, fill="x") 
        
        # 3. Grilla de Materias Disponibles 
        tk.Label(self, text="📚 Asignaturas Disponibles (Haz clic para ingresar):", font=("Arial", 11, "bold"), fg=accent, bg=bg_main).pack(anchor="w", pady=(0, 8), fill="x") 
        
        frame_materias_grid = tk.Frame(self, bg=panel_bg) 
        frame_materias_grid.pack(fill="both", expand=True) 
        
        materias_lista = self._obtener_materias_por_contexto() 
        col_max = 4 
        for idx, mat in enumerate(materias_lista): 
            row = idx // col_max 
            col = idx % col_max 
            
            # Permitir que la fila también se expanda de forma uniforme 
            frame_materias_grid.rowconfigure(row, weight=1) 
            
            m_lower = mat.lower() 
            if "lengua" in m_lower: icon = "📝" 
            elif "matemát" in m_lower or "álgebra" in m_lower or "cálculo" in m_lower: icon = "📐" 
            elif "histor" in m_lower or "ética" in m_lower or "ciudadanía" in m_lower: icon = "📜" 
            elif "econ" in m_lower or "comercial" in m_lower or "gestión" in m_lower: icon = "📊" 
            elif "tecnolog" in m_lower or "mecan" in m_lower or "diseño" in m_lower: icon = "⚙️" 
            elif "tic" in m_lower or "programac" in m_lower or "software" in m_lower: icon = "💻" 
            elif "físic" in m_lower or "químic" in m_lower or "electr" in m_lower: icon = "⚡" 
            elif "biolog" in m_lower or "salud" in m_lower or "higiene" in m_lower: icon = "🌿" 
            elif "geograf" in m_lower or "topograf" in m_lower: icon = "🗺️" 
            elif "inglés" in m_lower or "ingles" in m_lower: icon = "🗣️" 
            elif "educación física" in m_lower or "ed_fisica" in m_lower: icon = "⚽" 
            elif "hardware" in m_lower or "sistemas" in m_lower or "redes" in m_lower or "circuitos" in m_lower: icon = "🖥️" 
            elif "taller" in m_lower or "carpinter" in m_lower or "electricid" in m_lower or "ajuste" in m_lower or "herrer" in m_lower or "obras" in m_lower: icon = "🔧" 
            elif "dibujo" in m_lower or "construc" in m_lower or "proyecto" in m_lower or "planos" in m_lower: icon = "📐" 
            else: icon = "📖" 
            
            btn_mat = CardButton( frame_materias_grid, text=mat, command=lambda m=mat: self._al_hacer_clic_materia(m), icon=icon, bg=panel_bg, fg=accent ) 
            # 🔑 sticky="nsew" hace que todas las tarjetas llenen el casillero de la grilla por completo 
            btn_mat.grid(row=row, column=col, padx=4, pady=4, sticky="nsew") 
            
        # 🔑 uniform="materia_col" obliga a que TODAS las columnas midan exactamente lo mismo 
        for c in range(col_max): 
            frame_materias_grid.columnconfigure(c, weight=1, uniform="materia_col")