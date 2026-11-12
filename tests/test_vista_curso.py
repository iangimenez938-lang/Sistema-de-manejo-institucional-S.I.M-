import pathlib
import sys
import tkinter as tk
import unittest


def load_vista_curso_module():
    app_content = pathlib.Path(__file__).resolve().parents[1] / "app-content"
    if str(app_content) not in sys.path:
        sys.path.insert(0, str(app_content))

    import vistas.vista_curso as module
    return module


class VistaCursoUITests(unittest.TestCase):
    def test_curso_ui_builds_and_exposes_required_helpers(self):
        module = load_vista_curso_module()
        root = tk.Tk()
        root.withdraw()

        try:
            frame = module.VistaCursoUI(
                root,
                contexto={"ciclo": "Ciclo Básico", "especialidad": "Informática"},
                on_materia_selected_callback=lambda *args, **kwargs: None,
                on_back_callback=lambda: None,
            )
            self.assertTrue(hasattr(frame, "frame_tabla_grid"))
            self.assertTrue(hasattr(frame, "_build_ui"))
            self.assertTrue(hasattr(frame, "_obtener_estilo_materia"))
            self.assertEqual(frame.canvas.winfo_manager(), "pack")
            self.assertEqual(frame.scrollbar.winfo_manager(), "pack")
            self.assertIn("Lengua", frame.horario_matriz[0].get("lunes", ""))
            self.assertIn("#d0ebff", frame._obtener_estilo_materia("Lengua").get("bg"))

            frame.contexto = {"modulo_central": "historia", "materia": "historia"}
            payloads = []
            frame.on_materia_click = lambda ctx: payloads.append(ctx)
            frame._al_hacer_clic_materia("matematica")
            self.assertEqual(payloads[0]["materia"], "matematica")
            self.assertEqual(payloads[0]["modulo_central"], "matematica")

            frame.contexto = {"ciclo": "Ciclo Básico", "especialidad": "Informática", "modulo_central": "historia", "materia": "historia"}
            docente_payloads = []
            frame.on_docente_click = lambda ctx: docente_payloads.append(ctx)
            frame._abrir_ficha_docente_materia("Matemática")
            self.assertEqual(docente_payloads[0]["materia"], "Matemática")
            self.assertEqual(docente_payloads[0]["ciclo"], "Ciclo Básico")
        finally:
            root.destroy()


if __name__ == "__main__":
    unittest.main()
