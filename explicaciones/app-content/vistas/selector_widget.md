import tkinter as tk 
from tkinter import ttk, messagebox 

try: 
    HAS_TKINTER = True 
except ImportError: 
    HAS_TKINTER = False 
    
class SelectorMateriaUI: 
    """Widget de selección dinámica de Ciclo, Año, División/Especialidad y Materia.""" 
    
    def __init__(self, parent_frame, on_materia_selected_callback=None): 
        if not HAS_TKINTER: 
            return 
        
        self.parent = parent_frame 
        self.callback = on_materia_selected_callback 
        # Contenedor principal con diseño institucional 
        self.frame_selector = tk.LabelFrame( self.parent, text="🎯 Filtro de Plan de Estudios", font=("Arial", 10, "bold"), padx=10, pady=8, bg="#f8f9fa", fg="#007acc" ) 
        self.frame_selector.pack(fill="x", padx=10, pady=6) 

        self._build_controls() 
        self._conectar_eventos() 
        self._inicializar_ciclos() 
        
    def _build_controls(self): 
        row = tk.Frame(self.frame_selector, bg="#f8f9fa") 
        row.pack(fill="x", pady=2) 
        
        # 1. Ciclo 
        tk.Label(row, text="Ciclo:", font=("Arial", 9, "bold"), bg="#f8f9fa").pack(side="left", padx=(0, 4)) 
        self.cmb_ciclo = ttk.Combobox(row, state="readonly", width=14) 
        self.cmb_ciclo.pack(side="left", padx=(0, 10)) 
        
        # 2. Año 
        tk.Label(row, text="Año:", font=("Arial", 9, "bold"), bg="#f8f9fa").pack(side="left", padx=(0, 4)) 
        self.cmb_anio = ttk.Combobox(row, state="readonly", width=8) 
        self.cmb_anio.pack(side="left", padx=(0, 10)) 
        
        # 3. División (Para Ciclo Básico) 
        self.lbl_division = tk.Label(row, text="División:", font=("Arial", 9, "bold"), bg="#f8f9fa") 
        self.cmb_division = ttk.Combobox(row, state="readonly", width=6) 
        
        # 4. Especialidad (Para Ciclo Avanzado) 
        self.lbl_especialidad = tk.Label(row, text="Especialidad:", font=("Arial", 9, "bold"), bg="#f8f9fa") 
        self.cmb_especialidad = ttk.Combobox(row, state="readonly", width=16) 
        
        # 5. Materia 
        tk.Label(row, text="Materia:", font=("Arial", 9, "bold"), bg="#f8f9fa").pack(side="left", padx=(10, 4)) 
        self.cmb_materia = ttk.Combobox(row, state="readonly", width=22) 
        self.cmb_materia.pack(side="left", padx=(0, 10)) 
        
        # Botón Cargar 
        self.btn_cargar = tk.Button( 
            row, 
            text="🚀 Cargar Materia", 
            command=self._al_seleccionar_materia, 
            bg="#007acc", 
            fg="white", 
            font=("Arial", 9, "bold"), 
            relief="groove", cursor="hand2" 
        ) 
        self.btn_cargar.pack(side="left", padx=(6, 0)) 
        
    def _inicializar_ciclos(self): 
        self.cmb_ciclo["values"] = ["Ciclo Básico", "Ciclo Avanzado"] 
        self.cmb_ciclo.set("Ciclo Básico") 
        self._actualizar_por_ciclo() 
        
    def _conectar_eventos(self): 
        self.cmb_ciclo.bind("<<ComboboxSelected>>", lambda e: self._actualizar_por_ciclo()) 
        self.cmb_anio.bind("<<CoboboxSelected>>", lambda e: self._actualizar_materias())
        self.cmb_especialidad.bind("<<ComboboxSelected>>", lambda e: self._actualizar_materias())

    def _actualizar_por_ciclo(self): 
        ciclo = self.cmb_ciclo.get() 
        if ciclo == "Ciclo Básico": 
            # Configurar Básico: Años 1, 2, 3 + Divisiones A a F 
            self.cmb_anio["values"] = [1, 2, 3] 
            self.cmb_anio.set(1) 
            
            # Ocultar Especialidad, Mostrar División 
            self.lbl_especialidad.pack_forget() 
            self.cmb_especialidad.pack_forget() 
            
            self.lbl_division.pack(side="left", padx=(0, 4), before=self.cmb_materia.master.winfo_children()[8]) 
            self.cmb_division.pack(side="left", padx=(0, 10), before=self.cmb_materia.master.winfo_children()[8]) 
            self.cmb_division["values"] = ["A", "B", "C", "D", "E", "F"] 
            self.cmb_division.set("A") 
        
        else: 
            # Configurar Avanzado: Años 4, 5, 6, 7 + Especialidades 
            self.cmb_anio["values"] = [4, 5, 6, 7] 
            self.cmb_anio.set(4) 
            
            # Ocultar División, Mostrar Especialidad 
            self.lbl_division.pack_forget() 
            self.cmb_division.pack_forget() 
            
            self.lbl_especialidad.pack(side="left", padx=(0, 4), before=self.cmb_materia.master.winfo_children()[8]) 
            self.cmb_especialidad.pack(side="left", padx=(0, 10), before=self.cmb_materia.master.winfo_children()[8]) 
            self.cmb_especialidad["values"] = ["Informática", "Electrónica", "Electromecánica", "Construcciones"] 
            self.cmb_especialidad.set("Informática") 
        
        self._actualizar_materias() 
        
    def _actualizar_materias(self): 
        ciclo = self.cmb_ciclo.get() 
        try: 
            anio = int(self.cmb_anio.get()) 
        except ValueError: 
            anio = 1 
        
        if ciclo == "Ciclo Básico": 
            materias = [ "Lengua", "Artística", "Ética y Ciudadana", "Tecnología", "Inglés", "Historia", "Biología", "Geografía", "Dibujo Técnico", "Matemática", "Educación Física", "Taller" ] 
        else: 
            esp = self.cmb_especialidad.get() 
            if esp == "Informática": 
                materias = [ "Historia", "Matemática", "Economía", "Tecnología", "TIC", "Física", "Inglés", "Lengua", "Labs. Programación", "Labs. Hardware", "Labs. Aplicaciones", "Labs. Sistemas", "Educación Física" ] 
            else: 
                materias = [ "Matemática", "Física", "Química", "Lengua", "Inglés", "Historia", "Especialidad Técnica", "Educación Física" ] 
        
        self.cmb_materia["values"] = materias 
        if materias: 
            self.cmb_materia.set(materias[0])

    def _al_seleccionar_materia(self): 
        ciclo = self.cmb_ciclo.get() 
        materia_nombre = self.cmb_materia.get() 
        
        # Mapeo a identificador del módulo central 
        m_lower = materia_nombre.lower() 
        if "lengua" in m_lower: mod_key = "lengua" 
        elif "matemát" in m_lower or "álgebra" in m_lower: mod_key = "matematica" 
        elif "histor" in m_lower: mod_key = "historia" 
        elif "químic" in m_lower: mod_key = "quimica" 
        elif "físic" in m_lower: mod_key = "fisica" 
        elif "inglés" in m_lower or "ingles" in m_lower: mod_key = "ingles" 
        elif "econ" in m_lower: mod_key = "economia" 
        elif "programaci" in m_lower: mod_key = "programacion" 
        else: mod_key = "materia_generica" 
        
        contexto = { 
            "ciclo": ciclo, 
            "anio": int(self.cmb_anio.get()), 
            "division": self.cmb_division.get() if ciclo == "Ciclo Básico" else "N/A", 
            "especialidad": "General" if ciclo == "Ciclo Básico" else self.cmb_especialidad.get(), 
            "materia": materia_nombre, 
            "modulo_central": mod_key 
        } 
        
        if self.callback: 
            self.callback(contexto)