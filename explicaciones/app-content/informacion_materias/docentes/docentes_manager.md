import json 
from pathlib import Path 

DATA_DIR = Path(__file__).parent / "data" 
JSON_FILE = DATA_DIR / "docentes_data.json" 

class DocentesManager: 
    """Gestor de información docente y preceptores por curso y materia.""" 
    
    def __init__(self, filepath=JSON_FILE): 
        self.filepath = Path(filepath) 
        self.data = self._cargar_datos() 
        
    def _cargar_datos(self) -> dict: 
        if not self.filepath.exists(): 
            return {} 
        try: 
            with open(self.filepath, "r", encoding="utf-8") as f:
                contenido = f.read().strip()
            if not contenido:
                return {}
            return json.loads(contenido)
        except json.JSONDecodeError as e:
            print(f"Error cargando datos docentes: {e}")
            return {}
        except Exception as e:
            print(f"Error cargando datos docentes: {e}")
            return {}
    
    def guardar_datos(self) -> bool: 
        try: 
            self.filepath.parent.mkdir(parents=True, exist_ok=True) 
            with open(self.filepath, "w", encoding="utf-8") as f: 
                json.dump(self.data, f, ensure_ascii=False, indent=2) 
                return True 
        except Exception as e: 
            print(f"Error guardando datos docentes: {e}") 
            return False 
        
    def obtener_info_curso(self, ciclo: str, anio: int, esp_o_div: str) -> dict: 
        """Obtiene la información del preceptor y la lista de docentes para un curso.""" 
        anio_str = str(anio) 
        curso_data = self.data.get(ciclo, {}).get(anio_str, {}).get(esp_o_div, {}) 
        return { "preceptor": curso_data.get("preceptor", "A designar por Dirección Escolar"), "docentes": curso_data.get("docentes", {}) } 
    
    def obtener_docente_materia(self, ciclo: str, anio: int, esp_o_div: str, materia: str) -> dict: 
        """Obtiene los datos del docente específico de una materia.""" 
        
        info_curso = self.obtener_info_curso(ciclo, anio, esp_o_div) 
        docentes = info_curso.get("docentes", {}) 
        if materia in docentes: 
            return docentes[materia] 
        
        # Búsqueda insensible a mayúsculas/minúsculas 
        m_lower = materia.lower() 
        for key, val in docentes.items(): 
            if key.lower() == m_lower: 
                return val 
            
        return { 
            "nombre": "Docente a designar", 
            "email": "consultas@escuelatecnica.edu.ar", 
            "horario_consulta": "A confirmar", 
            "notas": "Sin observaciones registradas." 
        } 
    
    def asignar_docente(self, ciclo: str, anio: int, esp_o_div: str, materia: str, datos_docente: dict) -> bool: 
        """Agrega o actualiza los datos de un docente para un curso y materia.""" 
        
        anio_str = str(anio) 
        if ciclo not in self.data: 
            self.data[ciclo] = {} 
        if anio_str not in self.data[ciclo]: 
            self.data[ciclo][anio_str] = {} 
        if esp_o_div not in self.data[ciclo][anio_str]: 
            self.data[ciclo][anio_str][esp_o_div] = {"preceptor": "A designar", "docentes": {}} 
            
        self.data[ciclo][anio_str][esp_o_div]["docentes"][materia] = datos_docente 
        return self.guardar_datos()
    