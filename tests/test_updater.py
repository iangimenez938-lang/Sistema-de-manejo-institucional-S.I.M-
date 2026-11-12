import unittest

from updater import is_newer_version, parse_version


class UpdaterTests(unittest.TestCase):
    def test_parse_version_handles_text_and_numbers(self):
        self.assertEqual(parse_version("1.2.3"), (1, 2, 3))
        self.assertEqual(parse_version("v1.2.3-beta"), (1, 2, 3))
        self.assertEqual(parse_version("2"), (2,))

    def test_is_newer_version_detects_updates(self):
        self.assertTrue(is_newer_version("1.2.3", "1.2.2"))
        self.assertFalse(is_newer_version("1.2.2", "1.2.3"))
        self.assertFalse(is_newer_version("1.2.2", "1.2.2"))

    def test_manifest_json_example(self):
        manifest = {
            "version": "1.2.3",
            "download_url": "https://example.com/app.exe"
        }
        self.assertEqual(manifest["version"], "1.2.3")
        self.assertTrue(manifest["download_url"].startswith("http"))


if __name__ == "__main__":
    unittest.main()
