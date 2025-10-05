"""Plugin loading utilities."""

from __future__ import annotations

import importlib
import logging
import pkgutil
from types import ModuleType
from typing import Iterator, Protocol

log = logging.getLogger(__name__)


class ModuleFilter(Protocol):
    """Callable to decide if a module should be imported.

    Args:
        full_name: e.g. 'plugins.audio.wav'.
        ispkg: True if it's a package, False if it's a single module.

    Returns:
        True to import, False to skip.
    """

    def __call__(self, full_name: str, ispkg: bool) -> bool: ...


def _iter_submodules(
    pkg: ModuleType,
    *,
    recursive: bool = False,
    predicate: ModuleFilter | None = None,
) -> Iterator[str]:
    """Yield fully qualified submodule names under a package."""
    path = getattr(pkg, "__path__", None)
    if not path:
        return
    for mi in pkgutil.iter_modules(path):
        if mi.name.startswith("_"):
            continue
        full = f"{pkg.__name__}.{mi.name}"
        if predicate is None or predicate(full, mi.ispkg):
            yield full
        if recursive and mi.ispkg:
            try:
                subpkg = importlib.import_module(full)
            except Exception:  # pylint: disable=W0718
                log.exception("Failed to import subpackage: %s", full)
                continue
            yield from _iter_submodules(
                subpkg, recursive=True, predicate=predicate
            )


def load_plugins(
    package: str | ModuleType | None = None,
    *,
    recursive: bool = False,
    predicate: ModuleFilter | None = None,
    strict: bool = False,
) -> tuple[str, ...]:
    """Import plugin modules and return loaded module names."""
    if package is None:
        package = __name__
    try:
        pkg = importlib.import_module(package) if isinstance(
            package, str
        ) else package
    except Exception as exception:  # pylint: disable=W0718
        raise ImportError(
            f"Cannot import package \"{package}\": {exception}"
        ) from exception

    loaded: list[str] = []
    for name in _iter_submodules(
        pkg, recursive=recursive, predicate=predicate
    ):
        try:
            importlib.import_module(name)
            loaded.append(name)
            log.debug("Loaded plugin: %s", name)
        except Exception as exception:  # pylint: disable=W0718
            log.exception(
                "Failed to import plugin module \"%s\": %s", name, exception
            )
            if strict:
                raise exception
    return tuple(loaded)


__all__ = ["ModuleFilter", "load_plugins"]
