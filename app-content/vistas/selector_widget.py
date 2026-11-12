import tkinter as tk 
from tkinter import ttk 

try: 
    HAS_TKINTER = True 
except ImportError: 
    HAS_TKINTER = False 
    
class SelectorMateriaUI:
    """Widget de selección dinámica de Ciclo, Año y División/Especialidad para cargar un Curso.""" 
    def __init__(self, parent_frame, on_materia_selected_callback=None): 
        if not HAS_TKINTER: 
            return 
        
        self.parent = parent_frame 
        # Callback para notificar la carga del curso seleccionado 
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
        
        # Botón Cargar Curso (Materia quitada por ser obsoleta) 
        self.btn_cargar = tk.Button( row, text="🚀 Cargar Curso", command=self._al_seleccionar_curso, bg="#007acc", fg="white", font=("Arial", 9, "bold"), relief="groove", cursor="hand2" ) 
        self.btn_cargar.pack(side="left", padx=(10, 0)) 
        
    def _inicializar_ciclos(self): 
        self.cmb_ciclo["values"] = ["Ciclo Básico", "Ciclo Avanzado"] 
        self.cmb_ciclo.set("Ciclo Básico") 
        self._actualizar_por_ciclo() 
        
    def _conectar_eventos(self): 
        self.cmb_ciclo.bind("<<ComboboxSelected>>", lambda e: self._actualizar_por_ciclo()) 
    
    def _actualizar_por_ciclo(self): 
        ciclo = self.cmb_ciclo.get() 
        
        if ciclo == "Ciclo Básico": 
            # Configurar Básico: Años 1, 2, 3 + Divisiones A a F 
            self.cmb_anio["values"] = [1, 2, 3] 
            self.cmb_anio.set(1) 
            # Ocultar Especialidad, Mostrar División 
            self.lbl_especialidad.pack_forget() 
            self.cmb_especialidad.pack_forget() 
            self.lbl_division.pack(side="left", padx=(0, 4), before=self.btn_cargar) 
            self.cmb_division.pack(side="left", padx=(0, 10), before=self.btn_cargar) 
            self.cmb_division["values"] = ["A", "B", "C", "D", "E", "F"] 
            self.cmb_division.set("A") 
        else: 
            # Configurar Avanzado: Años 4, 5, 6, 7 + Especialidades 
            self.cmb_anio["values"] = [4, 5, 6, 7] 
            self.cmb_anio.set(4) 
            # Ocultar División, Mostrar Especialidad 
            self.lbl_division.pack_forget() 
            self.cmb_division.pack_forget() 
            self.lbl_especialidad.pack(side="left", padx=(0, 4), before=self.btn_cargar) 
            self.cmb_especialidad.pack(side="left", padx=(0, 10), before=self.btn_cargar) 
            self.cmb_especialidad["values"] = ["Informática", "Electrónica", "Electromecánica", "Construcciones"] 
            self.cmb_especialidad.set("Informática") 
            
    def _al_seleccionar_curso(self): 
        ciclo = self.cmb_ciclo.get() 
        try: 
            anio = int(self.cmb_anio.get()) 
        except ValueError: 
            anio = 1 
            
        contexto = { "ciclo": ciclo, "anio": anio, "division": self.cmb_division.get() if ciclo == "Ciclo Básico" else "N/A", "especialidad": "General" if ciclo == "Ciclo Básico" else self.cmb_especialidad.get() } 
        
        if self.callback: 
            self.callback(contexto)