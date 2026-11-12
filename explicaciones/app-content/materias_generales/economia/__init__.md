# esto es temporal hasta que se disenien los moduloes reales de todas las materias

import tkinter as tk 
from informacion_materias.docentes import VistaDocentePage 
from configuracion.config_manager import cargar_configuracion 

class ModuloMateriaBase: 
    def __init__(self, parent_frame, contexto=None): 
        self.parent = parent_frame 
        self.contexto = contexto or {} 
        
        self.config_val = cargar_configuracion() 
        self.main_container = tk.Frame(self.parent, bg=self.config_val.get("bg_color", "#ffffff")) 
        self.main_container.pack(fill="both", expand=True) 
        
        self._build_top_bar() 
        
        self.content_frame = tk.Frame(self.main_container, bg=self.config_val.get("bg_color", "#ffffff")) 
        self.content_frame.pack(fill="both", expand=True, padx=15, pady=15) 
        self._mostrar_pantalla_inicial() 
        
    def _build_top_bar(self): 
        accent = self.config_val.get("accent_color", "#007acc") 
        bar = tk.Frame(self.main_container, bg="#f0f4f8", padx=10, pady=6, bd=1, relief="solid") 
        bar.pack(fill="x", side="top") 
        
        materia_nombre = self.contexto.get("materia", "Asignatura").upper() 
        tk.Label( bar, text=f"📚 {materia_nombre}", font=(self.config_val.get("font_family", "Arial"), 11, "bold"), fg=accent, bg="#f0f4f8" ).pack(side="left") 
        btn_docente = tk.Button( bar, text="👤 Docente", command=self._abrir_pagina_docente, bg=accent, fg="white", font=("Arial", 9, "bold"), relief="groove", cursor="hand2" ) 
        btn_docente.pack(side="right", padx=5) 
        
    def _abrir_pagina_docente(self): 
        for w in self.content_frame.winfo_children(): 
            w.destroy() 
        
        VistaDocentePage( self.content_frame, contexto=self.contexto, on_back_callback=self._mostrar_pantalla_inicial ) 
        
    def _mostrar_pantalla_inicial(self): 
        for w in self.content_frame.winfo_children(): 
            w.destroy() 
            
        tk.Label( self.content_frame, text=f"📂 {self.contexto.get('materia', 'Materia')}\n\n(Espacio reservado para las herramientas de la asignatura)", font=("Arial", 11), fg="#666666", bg=self.config_val.get("bg_color", "#ffffff") ).pack(expand=True) 
        
def build_ui(parent_frame, contexto=None): 
    return ModuloMateriaBase(parent_frame, contexto=contexto)