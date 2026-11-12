import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class RepositoryBootstrapTests(unittest.TestCase):
    def test_required_docs_exist(self):
        for path in [
            "README.md",
            "CONTRIBUTING.md",
            "SECURITY.md",
            "docs/ARCHITECTURE.md",
            "docs/SOURCES.md",
            "docs/DATA_DICTIONARY.md",
            "docs/ROADMAP.md",
        ]:
            with self.subTest(path=path):
                self.assertTrue((ROOT / path).is_file(), path)

    def test_readme_does_not_claim_live_integration(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Ainda não existe alimentação em tempo real", readme)

if __name__ == "__main__":
    unittest.main()
