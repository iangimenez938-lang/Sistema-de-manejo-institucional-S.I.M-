import importlib.util
import pathlib
import shutil
import tempfile
import unittest


def load_launcher_module():
    launcher_path = pathlib.Path(__file__).resolve().parents[1] / "app-content" / "launcher.py"
    spec = importlib.util.spec_from_file_location("launcher_module", launcher_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_launcher_in_packaged_layout():
    root = pathlib.Path(tempfile.mkdtemp())
    project_root = pathlib.Path(__file__).resolve().parents[1]
    app_dir = root / "app-content"

    shutil.copytree(project_root / "app-content", app_dir)
    shutil.copy2(project_root / "app-content" / "launcher.py", root / "launcher.py")

    spec = importlib.util.spec_from_file_location("launcher_package_layout", root / "launcher.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LauncherImportTests(unittest.TestCase):
    def test_launcher_reexports_ui_components_and_creditos_entrypoint(self):
        module = load_launcher_module()

        self.assertTrue(hasattr(module, "HeaderBar"))
        self.assertTrue(hasattr(module, "SelectorMateriaUI"))
        self.assertTrue(hasattr(module, "StatusBar"))
        self.assertTrue(hasattr(module, "PanelBase"))
        self.assertTrue(hasattr(module, "CardButton"))
        self.assertTrue(hasattr(module, "mostrar_creditos"))
        self.assertTrue(callable(module.mostrar_creditos))

    def test_launcher_imports_when_app_content_sits_next_to_launcher(self):
        module = load_launcher_in_packaged_layout()
        self.assertTrue(hasattr(module, "mostrar_creditos"))


if __name__ == "__main__":
    unittest.main()
