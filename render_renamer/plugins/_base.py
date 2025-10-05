"""Base class for all RenderRenamer addons."""
from __future__ import annotations

import abc
from typing import Any
from typing import ClassVar
from dataclasses import dataclass

from render_renamer.renaming.renaming_item import RenamingItem
from ._registry import PluginBase, PluginRegistry


class RenderRenamerAddon(PluginBase, abc.ABC):
    """Base class for all RenderRenamer addons."""
    REGISTRY: ClassVar[PluginRegistry[RenderRenamerAddon]] = PluginRegistry()

    @dataclass
    class Config(abc.ABC):
        """Base class for addon configuration."""

    @property
    def name(self) -> str:
        """Return the name of the addon."""
        return self.__class__.__name__

    def __init__(
        self, config: RenderRenamerAddon.Config | None = None
    ) -> None:
        self.config = config or self.Config()

    def __init_subclass__(cls):
        super().__init_subclass__()
        cls.REGISTRY.register(cls)

    @abc.abstractmethod
    def get_variables(self, item: RenamingItem) -> dict[str, Any]:
        """Extract variables from the source path."""
        return NotImplemented
