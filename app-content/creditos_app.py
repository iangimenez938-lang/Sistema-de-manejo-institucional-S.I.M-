import json
from pathlib import Path
import tkinter as tk 
from tkinter import ttk, messagebox 


def _get_project_version():
    try:
        manifest_path = Path(__file__).resolve().parent.parent / "version.json"
        payload = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
        version = payload.get("version")
        if version:
            return str(version)
    except (FileNotFoundError, json.JSONDecodeError, OSError, TypeError, ValueError):
        pass
    return "1.3.2"


class CreditosWindow(tk.Toplevel): 
    """Ventana emergente de créditos e información institucional.""" 
    
    def __init__(self, parent): 
        super().__init__(parent) 
        self.title("Créditos - Plataforma Educativa Técnica") 
        self.geometry("500x380") 
        self.resizable(False, False) 
        self.configure(bg="#ffffff") 
        
        # Centrar ventana respecto al padre 
        self.transient(parent) 
        self.grab_set() 
        self._build_ui() 
        
    def _build_ui(self): 
        # Header 
        header = tk.Frame(self, bg="#007acc", padx=15, pady=12) 
        header.pack(fill="x") 
        
        tk.Label( header, text="ℹ️ Plataforma Educativa Técnica", font=("Arial", 12, "bold"), fg="#ffffff", bg="#007acc" ).pack(anchor="w") 
        tk.Label( header, text="Sistema Modular por Ciclos, Años y Especialidades", font=("Arial", 9), fg="#e0f2fe", bg="#007acc" ).pack(anchor="w") 
        
        # Contenido 
        body = tk.Frame(self, bg="#ffffff", padx=20, pady=15) 
        body.pack(fill="both", expand=True) 
        
        version_text = _get_project_version()
        info_text = (
            "🏛️ Escuela de Educación Técnica\n"
            "--------------------------------------------------\n"
            f"• Versión: {version_text} (Modular)\n"
            "• Desarrollo: Sistema de integración curricular\n"
            "• Arquitectura: Python + Tkinter\n\n"
            "Desarrollador principal: Gimenez Ian\n"
            "Desarrollador asistente: GithHub Copilot chat, Gemini NotebookLM\n"
            "Especialidades Integradas:\n"
            "• Ciclo Básico (1º a 3º Año - Divisiones A a F)\n"
            "• Ciclo Avanzado (4º a 7º Año):\n"
            " - Informática\n"
            " - Electrónica\n"
            " - Electromecánica\n"
            " - Construcciones\n\n"
            "© 2026 - Todos los derechos reservados."
        )
        
        tk.Label( body, text=info_text, font=("Arial", 9), bg="#ffffff", justify="left", anchor="w" ).pack(fill="both", expand=True) 
        # Botón Cerrar 
        btn_cerrar = tk.Button( self, text="Cerrar", command=self.destroy, bg="#007acc", fg="white", font=("Arial", 9, "bold"), padx=15, pady=4, relief="groove" ) 
        btn_cerrar.pack(pady=(0, 15)) 
        
def mostrar_creditos(parent): 
    """Función para abrir la ventana de créditos desde cualquier módulo.""" 
    return CreditosWindow(parent) 
    
__all__ = ["CreditosWindow", "mostrar_creditos"]