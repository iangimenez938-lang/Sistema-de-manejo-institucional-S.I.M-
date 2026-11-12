import sys
import tempfile
import unittest
from pathlib import Path

APP_CONTENT = Path(__file__).resolve().parents[1] / "app-content"
if str(APP_CONTENT) not in sys.path:
    sys.path.insert(0, str(APP_CONTENT))

from informacion_materias.docentes.docentes_manager import DocentesManager


class DocentesManagerTests(unittest.TestCase):
    def test_empty_json_file_is_treated_as_empty_data(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            json_path = Path(tmp_dir) / "docentes_data.json"
            json_path.write_text("", encoding="utf-8")

            manager = DocentesManager(filepath=json_path)

            self.assertEqual(manager.data, {})
            self.assertEqual(manager.obtener_docente_materia("Ciclo Básico", 1, "A", "Lengua"), {
                "nombre": "Docente a designar",
                "cursos": "1º Año A",
                "telefono": "+54 3777 0000-0000",
                "email": "consultas@escuelatecnica.edu.ar",
                "horarios_tabla": [],
            })

    def test_asignar_docente_persists_updates_for_existing_teacher(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            json_path = Path(tmp_dir) / "docentes_data.json"
            manager = DocentesManager(filepath=json_path)

            datos_iniciales = {
                "nombre": "Laura Pérez",
                "cursos": "1º Año A",
                "telefono": "1234",
                "email": "laura@example.com",
                "horarios_tabla": [
                    {"dia": "Lunes", "horario": "M1 (07:00 - 07:40)", "actividad": "Historia", "aula": "Aula 4B"}
                ],
            }

            self.assertTrue(manager.asignar_docente("Ciclo Básico", 1, "A", "Historia", datos_iniciales))

            datos_actualizados = {
                "nombre": "Laura Gómez",
                "cursos": "1º Año A",
                "telefono": "5678",
                "email": "laura.nueva@example.com",
                "horarios_tabla": [
                    {"dia": "Martes", "horario": "M2 (07:40 - 08:20)", "actividad": "Historia", "aula": "Aula 8"}
                ],
            }

            self.assertTrue(manager.asignar_docente("Ciclo Básico", 1, "A", "Historia", datos_actualizados))

            reloaded = DocentesManager(filepath=json_path)
            doc = reloaded.obtener_docente_materia("Ciclo Básico", 1, "A", "Historia")

            self.assertEqual(doc["nombre"], "Laura Gómez")
            self.assertEqual(doc["telefono"], "5678")
            self.assertEqual(doc["horarios_tabla"][0]["dia"], "Martes")
            self.assertEqual(doc["horarios_tabla"][0]["aula"], "Aula 8")


if __name__ == "__main__":
    unittest.main()
