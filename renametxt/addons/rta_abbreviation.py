"""Rename.TXT addon for abbreviation."""


from typing import Any

from renamming.renamming import RenammingItem

from . import RenameTXTAddonType
from .addons import RenameTXTAddon


class RTAAbbreviation(RenameTXTAddon):
    """Rename.TXT addon for abbreviation."""
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
        variables: dict[str, Any] = {}
        return variables
