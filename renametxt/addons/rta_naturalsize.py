"""Rename.TXT addon for naturalsize."""


from typing import Any

import humanize

from renamming.renamming import RenammingItem

from . import RenameTXTAddonType
from .addons import RenameTXTAddon


class RTANaturalsize(RenameTXTAddon):
    """Rename.TXT addon for naturalsize."""

    @property
    def acceptable_extension_names(self) -> list[str]:
        return []

    @property
    def depends_on(self) -> list[RenameTXTAddonType]:
        return []

    def __init__(self, global_variables: dict[str, Any] | None = None) -> None:
        pass

    def get_variables(self, item: RenammingItem) -> dict[str, Any]:
        """Retuen the variables."""
        variables: dict[str, Any] = {
            "naturalsize": {
                "size": humanize.naturalsize(item.variables.get("size", 0), binary=True),
            }
        }
        return variables
