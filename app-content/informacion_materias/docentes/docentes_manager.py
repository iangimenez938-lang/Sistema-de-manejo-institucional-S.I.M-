import json 
from pathlib import Path 

DATA_DIR = Path(__file__).parent / "data" 
JSON_FILE = DATA_DIR / "docentes_data.json" 

class DocentesManager: 
    """Gestor de persistencia JSON para información docente, contactos y tabla de horarios por curso y materia.""" 
    def __init__(self, filepath=JSON_FILE): 
        self.filepath = Path(filepath) 
        self.data = self._cargar_datos() 
        
    def _cargar_datos(self) -> dict: 
        if not self.filepath.exists(): return {} 
        
        try: 
            with open(self.filepath, "r", encoding="utf-8") as f: 
                contenido = f.read().strip() 
                if not contenido: 
                    return {} 
                return json.loads(contenido) 
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
    
    def _normalizar_docente(self, ciclo: str, anio: int, esp_o_div: str, materia: str, datos_docente: dict | None) -> dict:
        base = {
            "nombre": "Docente a designar",
            "cursos": f"{anio}º Año {esp_o_div}",
            "telefono": "+54 3777 0000-0000",
            "email": "consultas@escuelatecnica.edu.ar",
            "horarios_tabla": [],
        }
        if not isinstance(datos_docente, dict):
            return base

        normalized = dict(base)
        normalized.update(datos_docente)
        normalized["horarios_tabla"] = normalized.get("horarios_tabla", [])
        normalized.pop("horario_consulta", None)
        return normalized

    def obtener_docente_materia(self, ciclo: str, anio: int, esp_o_div: str, materia: str) -> dict: 
        """Obtiene los datos del docente específico de una materia o retorna datos por defecto.""" 
        info_curso = self.obtener_info_curso(ciclo, anio, esp_o_div) 
        docentes = info_curso.get("docentes", {}) 
        if materia in docentes: 
            return self._normalizar_docente(ciclo, anio, esp_o_div, materia, docentes[materia])

        m_lower = materia.lower() 
        for key, val in docentes.items(): 
            if key.lower() == m_lower: 
                return self._normalizar_docente(ciclo, anio, esp_o_div, materia, val)

        return self._normalizar_docente(ciclo, anio, esp_o_div, materia, {
            "nombre": "Docente a designar",
            "cursos": f"{anio}º Año {esp_o_div}",
            "telefono": "+54 3777 0000-0000",
            "email": "consultas@escuelatecnica.edu.ar",
            "horarios_tabla": [],
        })
    
    def asignar_docente(self, ciclo: str, anio: int, esp_o_div: str, materia: str, datos_docente: dict) -> bool: 
        """Agrega o actualiza los datos de un docente para un curso y materia, y los guarda en JSON.""" 
        anio_str = str(anio) 
        self.data.setdefault(ciclo, {})
        self.data[ciclo].setdefault(anio_str, {})
        self.data[ciclo][anio_str].setdefault(esp_o_div, {"preceptor": "A designar", "docentes": {}})

        curso = self.data[ciclo][anio_str][esp_o_div]
        curso.setdefault("docentes", {})

        datos_normalizados = self._normalizar_docente(ciclo, anio, esp_o_div, materia, datos_docente)
        curso["docentes"][materia] = datos_normalizados

        return self.guardar_datos()