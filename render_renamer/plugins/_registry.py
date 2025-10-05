"""Plugin registry implementation."""
from __future__ import annotations
from typing import Generic, TypeVar, Type, Iterator


class PluginBase:
    """Base class for all plugins."""


T = TypeVar("T", bound=PluginBase)


class PluginRegistry(Generic[T]):
    """Registry for plugins."""
    def __init__(self) -> None:
        super().__init__()
        self._registry: dict[Type[T], None] = {}

    def register(self, plugin_cls: Type[T]) -> None:
        """Register a plugin class."""
        if not issubclass(plugin_cls, PluginBase):
            raise TypeError(
                "Plugin must be a subclass of PluginBase, "
                f"got \"{plugin_cls.__name__}\"."
            )
        if plugin_cls in self._registry:
            raise ValueError(
                f"Plugin \"{plugin_cls.__name__}\" is already registered."
            )
        self._registry[plugin_cls] = None

    def plugins(self) -> Iterator[Type[T]]:
        """Iterate over registered plugin classes."""
        yield from self._registry.keys()

    def clear(self) -> None:
        """Clear all registered plugins (for testing)."""
        self._registry.clear()
