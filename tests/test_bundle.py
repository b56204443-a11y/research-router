from pathlib import Path
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
FIND = ROOT / "skills/research-router/scripts/find_modules.py"


def command(script, *args, env=None):
    return subprocess.run([sys.executable, str(script), *map(str, args)], cwd=ROOT,
                          env=env, capture_output=True, text=True)


class RoutingTests(unittest.TestCase):
    def search(self, *args, env=None):
        r = command(FIND, *args, "--json", env=env)
        self.assertEqual(r.returncode, 0, r.stderr)
        return json.loads(r.stdout)

    def test_exact_module_and_resource_path(self):
        result = self.search("--query", "scanpy")
        self.assertEqual([m["name"] for m in result], ["scanpy"])
        self.assertTrue(Path(result[0]["skill_path"]).is_file())

    def test_chinese_statistics(self):
        self.assertEqual(self.search("--query", "统计分析", "--limit", "1")[0]["name"], "statistical-analysis")

    def test_chinese_research_figures(self):
        self.assertEqual(self.search("--query", "科研绘图", "--limit", "1")[0]["name"], "scientific-visualization")

    def test_category_and_no_match(self):
        result = self.search("--list", "--category", "literature")
        self.assertGreater(len(result), 0)
        self.assertTrue(all(m["category"] == "literature" for m in result))
        self.assertEqual(self.search("--query", "zzqxxnevermatches999"), [])

    def test_paths_survive_checkout_relocation(self):
        # Copy only the router, then point it at the full library through the documented override.
        import shutil
        with tempfile.TemporaryDirectory(prefix="research-router-relocate-") as tmp:
            destination = Path(tmp) / "location with spaces" / "research-router"
            shutil.copytree(ROOT / "skills/research-router", destination)
            env = dict(os.environ, RESEARCH_ROUTER_LIBRARY=str(ROOT / "skill-libraries/research-router/modules"))
            r = command(destination / "scripts/find_modules.py", "--query", "scanpy", "--json", env=env)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue(Path(json.loads(r.stdout)[0]["skill_path"]).is_file())

    def test_missing_library_is_actionable_error(self):
        with tempfile.TemporaryDirectory(prefix="research-router-missing-") as tmp:
            r = command(FIND, "--query", "scanpy", "--library-root", Path(tmp) / "missing")
            self.assertNotEqual(r.returncode, 0)
            self.assertIn("module directory not found", r.stderr)


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="research-router-install-")
        self.home = Path(self.temp.name) / "custom codex home"

    def tearDown(self):
        self.temp.cleanup()

    def install(self, *extra):
        return command(ROOT / "scripts/install.py", "--codex-home", self.home, *extra)

    def test_install_and_query_and_uninstall_preserve_other_skill(self):
        unrelated = self.home / "skills/unrelated/SKILL.md"
        unrelated.parent.mkdir(parents=True)
        unrelated.write_text("Existing user skill")
        r = self.install()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual({p.name for p in (self.home / "skills").iterdir()}, {"unrelated", "research-router"})
        find = self.home / "skills/research-router/scripts/find_modules.py"
        r = command(find, "--query", "scanpy", "--json")
        self.assertEqual(r.returncode, 0, r.stderr)
        path = Path(json.loads(r.stdout)[0]["skill_path"])
        self.assertTrue(path.is_file())
        self.assertTrue(path.is_relative_to(self.home.resolve()))
        self.assertTrue((self.home / "skill-libraries/research-router/licenses").is_dir())
        r = command(ROOT / "scripts/uninstall.py", "--codex-home", self.home)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(find.exists())
        self.assertEqual(unrelated.read_text(), "Existing user skill")
        self.assertEqual(len(list((self.home / "research-router-backups").glob("uninstall-*/library/modules/scanpy/SKILL.md"))), 1)

    def test_dry_run_does_not_create_home(self):
        r = self.install("--dry-run")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(self.home.exists())

    def test_replacement_requires_opt_in_and_preserves_backup(self):
        self.assertEqual(self.install().returncode, 0)
        marker = self.home / "skills/research-router/local-edit.txt"
        marker.write_text("Keep my local edit")
        r = self.install()
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(marker.read_text(), "Keep my local edit")
        r = self.install("--replace")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertFalse(marker.exists())
        copies = list((self.home / "research-router-backups").glob("*/0/local-edit.txt"))
        self.assertEqual(len(copies), 1)
        self.assertEqual(copies[0].read_text(), "Keep my local edit")

    def test_uninstall_refuses_unmanaged_library(self):
        marker = self.home / "skill-libraries/research-router/keep.txt"
        marker.parent.mkdir(parents=True)
        marker.write_text("Not installed by this package")
        r = command(ROOT / "scripts/uninstall.py", "--codex-home", self.home)
        self.assertNotEqual(r.returncode, 0)
        self.assertTrue(marker.exists())


class IntegrityTests(unittest.TestCase):
    def test_release_validation(self):
        r = command(ROOT / "scripts/validate.py")
        self.assertEqual(r.returncode, 0, r.stderr)


if __name__ == "__main__":
    unittest.main()
