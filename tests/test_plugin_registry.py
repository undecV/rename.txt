# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
from __future__ import annotations
import unittest
from typing import ClassVar

from render_renamer.plugins._registry import (
    PluginBase,
    PluginRegistry
)


class TestPluginRegistry(unittest.TestCase):
    def test_register_and_plugins(self):
        class myPluginBase(PluginBase):
            REGISTRY: ClassVar[PluginRegistry[myPluginBase]] = PluginRegistry()

            def __init_subclass__(cls) -> None:
                super().__init_subclass__()
                cls.REGISTRY.register(cls)

        class myPlugin1(myPluginBase):
            pass

        class myPlugin2(myPluginBase):
            pass

        plugins = list(myPluginBase.REGISTRY.plugins())
        self.assertIn(myPlugin1, plugins)
        self.assertIn(myPlugin2, plugins)

    def test_register_non_subclass(self):
        class NotAPlugin:
            pass

        registry = PluginRegistry[PluginBase]()
        with self.assertRaises(TypeError):
            registry.register(NotAPlugin)

    def test_register_duplicate(self):
        class MyPlugin(PluginBase):
            pass

        registry = PluginRegistry[MyPlugin]()
        registry.register(MyPlugin)
        with self.assertRaises(ValueError):
            registry.register(MyPlugin)

    def test_clear(self):
        class MyPlugin(PluginBase):
            pass

        registry = PluginRegistry[MyPlugin]()
        registry.register(MyPlugin)
        registry.clear()
        plugins = list(registry.plugins())
        self.assertEqual(len(plugins), 0)
