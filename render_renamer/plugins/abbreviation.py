"""Abbreviation plugin to extract abbreviations from filenames."""
from typing import Any
from render_renamer.renaming.renaming_item import RenamingItem
from ._base import RenderRenamerAddon


class RRAbbreviationAddon(RenderRenamerAddon):
    """Abbreviation plugin to extract abbreviations from filenames."""

    def get_variables(self, item: RenamingItem) -> dict[str, Any]:
        variables: dict[str, Any] = {
            "idx": item.variables.get("index"),
            "seq": item.variables.get("sequence"),
        }
        return variables
