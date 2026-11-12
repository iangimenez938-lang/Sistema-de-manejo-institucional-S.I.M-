import pathlib
import sys
import tkinter as tk
import unittest

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
APP_ROOT = PROJECT_ROOT / "app-content"
if str(APP_ROOT) not in sys.path:
    sys.path.insert(0, str(APP_ROOT))

from configuracion.config_manager import aplicar_estilos_a_widget_tree


class ConfigManagerFontTests(unittest.TestCase):
    def test_aplica_fuente_configurada_en_text_y_entry(self):
        root = tk.Tk()
        root.withdraw()
        try:
            config = {
                "bg_color": "#ffffff",
                "fg_color": "#212529",
                "panel_bg": "#f8f9fa",
                "accent_color": "#007acc",
                "font_family": "Arial",
                "font_size": 15,
            }

            text_widget = tk.Text(root)
            entry_widget = tk.Entry(root)

            aplicar_estilos_a_widget_tree(text_widget, config)
            aplicar_estilos_a_widget_tree(entry_widget, config)

            self.assertEqual(text_widget.cget("font"), "Arial 15")
            self.assertEqual(entry_widget.cget("font"), "Arial 15")
        finally:
            root.destroy()

    def test_aplica_scrollbar_vertical_en_text_widgets(self):
        root = tk.Tk()
        root.withdraw()
        try:
            config = {
                "bg_color": "#ffffff",
                "fg_color": "#212529",
                "panel_bg": "#f8f9fa",
                "accent_color": "#007acc",
                "font_family": "Arial",
                "font_size": 10,
            }

            text_widget = tk.Text(root, width=20, height=5)
            aplicar_estilos_a_widget_tree(text_widget, config)

            self.assertEqual(text_widget.cget("wrap"), "word")
            self.assertTrue(hasattr(text_widget, "_app_scrollbar"))
            self.assertIsNotNone(text_widget._app_scrollbar)
            self.assertEqual(str(text_widget._app_scrollbar.cget("orient")).lower(), "vertical")
            self.assertNotEqual(str(text_widget.cget("yscrollcommand")), "")
        finally:
            root.destroy()


if __name__ == "__main__":
    unittest.main()
