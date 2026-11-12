import sys 
import os 
from pathlib import Path 
import tkinter as tk 
from tkinter import ttk, messagebox 
import importlib 

# Diccionario de rutas para importación dinámica 
MAPEO_MATERIAS = { 
    # Materias Generales (Preexistentes y Nuevas) 
    "historia": "materias_generales.historia", 
    "matematica": "materias_generales.matematica", 
    "economia": "materias_generales.economia", 
    "lengua": "materias_generales.lengua",
    "tecnologia": "materias_generales.tecnologia", 
    "tic": "materias_generales.tic", 
    "fisica": "materias_generales.fisica", 
    "ingles": "materias_generales.ingles", 
    "ed_fisica": "materias_generales.ed_fisica", 
    # Laboratorios Específicos de 4to Informática 
    "labs_programacion": "materias_especificas.informatica_4to.labs_programacion", 
    "labs_hardware": "materias_especificas.informatica_4to.labs_hardware", 
    "labs_aplicaciones": "materias_especificas.informatica_4to.labs_aplicaciones", 
    "labs_sistemas": "materias_especificas.informatica_4to.labs_sistemas", 
}

# Asegurar que el directorio raíz 'app-content' esté en el sys.path 
BASE_DIR = Path(__file__).parent.resolve() 
if str(BASE_DIR) not in sys.path: 
    sys.path.insert(0, str(BASE_DIR)) 
    
try: 
    HAS_TKINTER = True 
except ImportError: 
    HAS_TKINTER = False 
    
# 1. IMPORTACIONES PRESERVADAS + NUEVAS (Aditivas) 
from creditos_app import mostrar_creditos 
from configuracion.opciones_app import build_opciones_app_ui 
from configuracion.config_manager import cargar_configuracion, aplicar_estilos_ttk, aplicar_estilos_globales 
from vistas import ( SelectorMateriaUI, HeaderBar, StatusBar, PanelBase, CardButton, VistaCursoUI ) 

class LauncherApp: 
    """Lanzador Principal del Sistema Educativo Técnico.""" 
    
    def __init__(self, root): 
        if not HAS_TKINTER: 
            print("Error: Tkinter no está disponible en el sistema.") 
            return 
        
        self.root = root 
        
        # ✅ NUEVO: Carga e Inyección de Estilos Globales al arrancar  
        self.config = cargar_configuracion() 
        aplicar_estilos_ttk(self.root, self.config) 
        
        self.root.title("Sistema Educativo Técnico - Lanzador General") 
        self.root.geometry("1150x750") 
        self.root.minsize(950, 650) 
        self.contexto_actual = {}  
        
        # ✅ PRESERVADO + MEJORADO: HeaderBar con botones de navegación  
        self.header = HeaderBar(
            self.root,
            titulo="🏛️ Escuela de Educación Técnica - Plataforma Educativa",
            subtitulo="Gestión Modular por Ciclos, Cursos y Materias Centrales",
            bg_color=self.config.get("accent_color", "#007acc"),
            fg_title="#ffffff",
            fg_subtitle="#edf7ff",
            button_bg=self.config.get("panel_bg", "#f8f9fa"),
            button_fg=self.config.get("accent_color", "#007acc"),
            on_home_click=self._mostrar_pantalla_bienvenida,
            on_config_click=self._abrir_opciones,
            on_creditos_click=self._abrir_creditos,
        )
        
        # ✅ PRESERVADO: Selector Dinámico de Cursos (Ciclo/Año/Esp/Div)  
        self.selector = SelectorMateriaUI( self.root, on_materia_selected_callback=self._cargar_vista_curso )  
        
        # ✅ PRESERVADO: Contenedor Dinámico Principal  
        self.frame_contenido = tk.Frame(self.root, bg="#ffffff", bd=1, relief="solid") 
        self.frame_contenido.pack(fill="both", expand=True, padx=10, pady=(0, 6))  
        
        # ✅ PRESERVADO: Barra de Estado Inferior  
        self.status_bar = StatusBar(self.root, text_inicial="Listo. Selecciona un curso arriba.", bg_color="#1f2937", fg_color="#ffffff") 
        # Cargar la pantalla de bienvenida inicial 
        self._mostrar_pantalla_bienvenida() 
        
    def _limpiar_contenido(self): 
        """Destruye los widgets anteriores antes de cargar una nueva vista.""" 
        for widget in self.frame_contenido.winfo_children(): 
            widget.destroy() 
            
    # ✅ PRESERVADO + MEJORADO: Pantalla de Bienvenida con Accesos  
    def _mostrar_pantalla_bienvenida(self): 
        """Pantalla inicial del lanzador con accesos rápidos e información institucional.""" 
        self._limpiar_contenido() 
        if hasattr(self, 'status_bar'): 
            self.status_bar.set_mensaje("Listo. Selecciona un curso arriba.") 
            
        container = tk.Frame(self.frame_contenido, bg="#ffffff", padx=20, pady=20) 
        container.pack(fill="both", expand=True) 
        
        lbl_bienvenida = tk.Label( container, text="👋 ¡Bienvenido al Portal Educativo TÉCNICO!", font=("Arial", 16, "bold"), fg="#007acc", bg="#ffffff" ) 
        lbl_bienvenida.pack(anchor="w", pady=(0, 6)) 
        
        lbl_desc = tk.Label( container, text=( "Esta aplicación organiza el plan de estudio de la educación técnica secundaria " "en Ciclo Básico (1º a 3º año) y Ciclo Avanzado (4º a 7º año por Especialidad).\n" "Para comenzar, utiliza el selector superior para elegir tu curso o navega desde los accesos rápidos." ), font=("Arial", 10), fg="#555555", bg="#ffffff", justify="left" ) 
        lbl_desc.pack(anchor="w", pady=(0, 16)) 

        aplicar_estilos_globales(container, self.config)
        
        # Panel de Accesos Rápidos (Conservando todos los botones anteriores + agregando Opciones) 
        pnl_accesos = PanelBase(container, titulo="📌 Información y Herramientas del Sistema", bg_color=self.config.get("panel_bg", "#f8f9fa"), fg_color=self.config.get("accent_color", "#007acc")) 
        pnl_accesos.pack(fill="x", pady=8) 
        
        grid_frame = tk.Frame(pnl_accesos, bg=self.config.get("panel_bg", "#f8f9fa")) 
        grid_frame.pack(fill="x", pady=4) 

        aplicar_estilos_globales(pnl_accesos, self.config)
        aplicar_estilos_globales(grid_frame, self.config)
        
        # ⚙️ Personalización Visual (NUEVO) 
        btn_opciones = CardButton(grid_frame, text="Personalización Visual", command=self._abrir_opciones, icon="⚙️", bg=self.config.get("panel_bg", "#f8f9fa"), fg=self.config.get("accent_color", "#007acc"), activebackground="#dfefff")
        btn_opciones.pack(side="left", padx=6) 
        
        # ℹ️ Créditos (PRESERVADO) 
        btn_creditos = CardButton(grid_frame, text="Créditos e Información", command=self._abrir_creditos, icon="ℹ️", bg=self.config.get("panel_bg", "#f8f9fa"), fg=self.config.get("accent_color", "#007acc"), activebackground="#dfefff")
        btn_creditos.pack(side="left", padx=6) 
        
        # 📖 Manual de Uso (PRESERVADO) 
        btn_ayuda = CardButton(grid_frame, text="Manual de Uso y Estructura", command=self._mostrar_manual, icon="📖", bg=self.config.get("panel_bg", "#f8f9fa"), fg=self.config.get("accent_color", "#007acc"), activebackground="#dfefff")
        btn_ayuda.pack(side="left", padx=6)
        
    # ✅ PRESERVADO: Dashboard del Curso  
    def _cargar_vista_curso(self, contexto: dict): 
        """Abre la pantalla del curso con su información y grilla de materias.""" 
        self.contexto_actual = contexto or {} 
        self._limpiar_contenido() 
        ciclo = self.contexto_actual.get("ciclo") 
        anio = self.contexto_actual.get("anio") 
        esp_div = ( self.contexto_actual.get("division") if ciclo == "Ciclo Básico" else self.contexto_actual.get("especialidad") ) 
        
        self.status_bar.set_mensaje(f"🏫 Curso Activo: {anio}º Año ({esp_div}) - {ciclo}") 
        
        # Renderizar la Vista del Curso 
        VistaCursoUI( self.frame_contenido, contexto=self.contexto_actual, on_materia_selected_callback=self._cargar_materia_modulo, on_back_callback=self._mostrar_pantalla_bienvenida )
        aplicar_estilos_globales(self.frame_contenido, self.config)
        
    # ✅ PRESERVADO: Inyección de Módulo Central de Materia  
    def _cargar_materia_modulo(self, contexto: dict): 
        self.contexto_actual = contexto or {} 
        self._limpiar_contenido() 
        
        mod_key = self.contexto_actual.get("modulo_central", "materia_generica") 
        materia_nombre = self.contexto_actual.get("materia", "Sin Nombre") 
        self.status_bar.set_mensaje(f"📚 Materia Activa: {materia_nombre}") 
        
        if mod_key in MAPEO_MATERIAS: 
            try: 
                modulo = importlib.import_module(MAPEO_MATERIAS[mod_key]) 
                if hasattr(modulo, "build_ui"): 
                    modulo.build_ui(self.frame_contenido, contexto=self.contexto_actual) 
                    return 
            except Exception as e: 
                print(f"Error al cargar el módulo '{mod_key}': {e}") 
                
        # Ficha de respaldo si la importación falla o está en ajuste 
        self._mostrar_materia_en_desarrollo(self.contexto_actual)
        
    # ✅ PRESERVADO: Ficha para Materias en Proceso de Desarrollo  
    def _mostrar_materia_en_desarrollo(self, contexto: dict): 
        container = tk.Frame(self.frame_contenido, bg="#ffffff", padx=20, pady=20) 
        container.pack(fill="both", expand=True) 
        aplicar_estilos_globales(container, self.config)
        
        btn_volver = tk.Button( container, text="⬅️ Volver al Curso", command=lambda: self._cargar_vista_curso(contexto), bg="#e0e0e0", font=("Arial", 9, "bold") ) 
        btn_volver.pack(anchor="w", pady=(0, 10)) 
        
        header_frame = tk.Frame(container, bg="#e0f2fe", padx=12, pady=10, bd=1, relief="solid") 
        header_frame.pack(fill="x", pady=(0, 16)) 
        
        tk.Label( header_frame, text=f"📚 {contexto.get('materia', '').upper()}", font=("Arial", 14, "bold"), fg="#007acc", bg="#e0f2fe" ).pack(anchor="w") 
        
        tk.Label( header_frame, text=f"Módulo Central: '{contexto.get('modulo_central')}'", font=("Arial", 10), bg="#e0f2fe" ).pack(anchor="w")  
        
    # ✅ NUEVOS / PRESERVADOS: Métodos de los Botones  
    def _abrir_opciones(self): 
        """Abre la pantalla de personalización visual (colores, fuentes, temas).""" 
        self._limpiar_contenido() 
        if hasattr(self, 'status_bar'): 
            self.status_bar.set_mensaje("⚙️ Personalización Visual del Sistema") 
        build_opciones_app_ui(self.frame_contenido, root=self.root) 
        
    def _abrir_creditos(self): 
        """Abre la ventana emergente de Créditos e Información Institucional.""" 
        mostrar_creditos(self.root) 
        
    def _mostrar_manual(self): 
        """Abre la ventana informativa del Manual de Uso.""" 
        messagebox.showinfo( "Manual de Uso", "1. Selecciona Ciclo, Año y División/Especialidad en el selector superior.\n" "2. Presiona '🚀 Cargar Curso' para ver el Dashboard con las asignaturas.\n" "3. Haz clic en la tarjeta de cualquier materia para ingresar a su módulo central.\n" "4. Utiliza los botones del encabezado para volver a Inicio o ajustar los Colores y Fuentes." ) 
        
def main(): 
    if not HAS_TKINTER: 
        return 
    
    root = tk.Tk() 
    app = LauncherApp(root) 
    root.mainloop() 
    
if __name__ == "__main__": 
    main()