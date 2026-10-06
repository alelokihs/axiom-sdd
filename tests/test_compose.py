"""Consumer ownership regression tests using only temporary projects."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "cli"))
from axiomcli import compose


class ComposeOwnershipTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.target = Path(self.temp.name)

    def test_fresh_profile_seed_and_report(self):
        result = compose.install(self.target, "fullstack-feature")
        self.assertEqual(
            (self.target / "sdd/profile.yaml").read_bytes(),
            (compose.ROOT / "profiles/fullstack-feature.yaml").read_bytes(),
        )
        self.assertEqual(result["copied"].count("sdd/profile.yaml"), 1)

    def test_base_does_not_report_nonexistent_profile(self):
        for update in (False, True):
            with self.subTest(update=update):
                result = compose.install(self.target, "base", update=update)
                self.assertFalse((self.target / "sdd/profile.yaml").exists())
                self.assertNotIn("sdd/profile.yaml", result["copied"])

    def test_reinstall_and_update_preserve_all_project_owned_bytes(self):
        compose.install(self.target, "fullstack-feature")
        custom = {}
        for relative in compose.PROJECT_OWNED:
            path = self.target / relative
            if path.is_dir():
                path /= "custom.md"
            path.parent.mkdir(parents=True, exist_ok=True)
            custom[path] = ("# Custom project policy\r\n" + relative + "\r\n").encode()
            path.write_bytes(custom[path])

        for update in (False, True, True):
            with self.subTest(update=update):
                result = compose.install(self.target, "fullstack-feature", update=update)
                for path, expected in custom.items():
                    self.assertEqual(path.read_bytes(), expected, str(path))
                self.assertNotIn("sdd/profile.yaml", result["copied"])

    def test_update_recreates_missing_profile_seed(self):
        compose.install(self.target, "fullstack-feature")
        path = self.target / "sdd/profile.yaml"
        path.unlink()
        result = compose.install(self.target, "fullstack-feature", update=True)
        self.assertEqual(path.read_bytes(), (compose.ROOT / "profiles/fullstack-feature.yaml").read_bytes())
        self.assertIn("sdd/profile.yaml", result["copied"])

    def test_update_refreshes_framework_owned_files(self):
        compose.install(self.target, "fullstack-feature")
        sources = {
            "sdd/core/evidence.md": "core/evidence.md",
            "sdd/templates/EVIDENCE.md": "templates/EVIDENCE.md",
            "sdd/agents/bootstrap.agent.md": "agents/bootstrap.agent.md",
            "sdd/workflow.yaml": "workflows/standard.yaml",
            "sdd/profile-defaults.yaml": "profiles/_defaults.yaml",
        }
        for relative in sources:
            (self.target / relative).write_text("old framework version\n", encoding="utf-8")
        result = compose.install(self.target, "fullstack-feature", update=True)
        for relative, source in sources.items():
            self.assertEqual((self.target / relative).read_bytes(), (compose.ROOT / source).read_bytes())
            self.assertIn(relative, result["copied"])


if __name__ == "__main__":
    unittest.main()
