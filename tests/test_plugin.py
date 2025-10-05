# test_loader.py
import sys
import tempfile
import importlib
import unittest
from pathlib import Path

from render_renamer.plugins import load_plugins, ModuleFilter


class TestLoadPlugins(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

        # 建立假的套件樹
        pkg = self.root / "plugins"
        (pkg).mkdir()
        (pkg / "__init__.py").write_text("")
        (pkg / "core.py").write_text("X = 1\n")
        (pkg / "utils.py").write_text("Y = 2\n")
        (pkg / "bad.py").write_text("raise RuntimeError('boom')\n")

        (pkg / "audio").mkdir()
        (pkg / "audio" / "__init__.py").write_text("")
        (pkg / "audio" / "wav.py").write_text("AUDIO = 'wav'\n")

        (pkg / "video").mkdir()
        (pkg / "video" / "__init__.py").write_text("")
        (pkg / "video" / "mp4.py").write_text("VIDEO = 'mp4'\n")

        # 讓 import 找得到
        sys.path.insert(0, str(self.root))
        # 寫檔後刷新匯入快取
        importlib.invalidate_caches()

        # 測試用過濾器：略過 utils
        def no_utils(full_name: str, ispkg: bool) -> bool:
            return not full_name.endswith(".utils")

        self.no_utils: ModuleFilter = no_utils

    def tearDown(self) -> None:
        # 清掉我們載入的假模組
        for name in list(sys.modules):
            if name == "plugins" or name.startswith("plugins."):
                sys.modules.pop(name, None)
        # 從 sys.path 拿掉臨時路徑
        try:
            sys.path.remove(str(self.root))
        except ValueError:
            pass
        self.tmp.cleanup()

    def test_non_recursive_loads_top_level_modules_and_packages(self) -> None:
        loaded = load_plugins("plugins", recursive=False)
        # 會載入頂層模組與套件本身
        self.assertIn("plugins.core", loaded)
        self.assertIn("plugins.utils", loaded)
        self.assertNotIn("plugins.bad", loaded)  # 壞模組不會載入
        self.assertIn("plugins.audio", loaded)   # 套件本身
        self.assertIn("plugins.video", loaded)
        # 但**不會**深入子模組
        self.assertNotIn("plugins.audio.wav", loaded)
        self.assertNotIn("plugins.video.mp4", loaded)

    def test_recursive_loads_submodules(self) -> None:
        loaded = load_plugins("plugins", recursive=True)
        self.assertIn("plugins.audio.wav", loaded)
        self.assertIn("plugins.video.mp4", loaded)

    def test_predicate_filters_utils(self) -> None:
        loaded = load_plugins("plugins", recursive=True,
                              predicate=self.no_utils)
        self.assertIn("plugins.core", loaded)
        self.assertNotIn("plugins.utils", loaded)
        self.assertIn("plugins.audio.wav", loaded)

    def test_strict_false_logs_and_continues(self) -> None:
        loaded = load_plugins("plugins", recursive=False,
                              predicate=self.no_utils)
        self.assertIn("plugins.core", loaded)
        # 壞模組匯入失敗 → 不會出現在 loaded，但流程不中斷
        self.assertNotIn("plugins.bad", loaded)

    def test_strict_true_raises_on_bad_module(self) -> None:
        with self.assertRaises(Exception):
            load_plugins("plugins", recursive=False, strict=True)

    def test_accepts_module_object(self) -> None:
        pkg = importlib.import_module("plugins")
        loaded = load_plugins(pkg, recursive=True, predicate=self.no_utils)
        self.assertIn("plugins.core", loaded)

    def test_non_package_argument(self) -> None:
        (self.root / "singlemod.py").write_text("Z = 3\n")
        importlib.invalidate_caches()
        mod = importlib.import_module("singlemod")
        loaded = load_plugins(mod, recursive=True)
        self.assertEqual(loaded, ())


if __name__ == "__main__":
    unittest.main(verbosity=2)
