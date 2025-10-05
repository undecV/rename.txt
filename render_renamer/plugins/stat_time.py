"""Stat time plugin to extract stat time from filenames."""
from typing import Any
from datetime import datetime

from render_renamer.renaming.renaming_item import RenamingItem
from ._base import RenderRenamerAddon


class RRStatTimeAddon(RenderRenamerAddon):
    """Stat time plugin to extract stat time from filenames."""

    def get_variables(self, item: RenamingItem) -> dict[str, Any]:
        variables: dict[str, Any] = {
            "atime": datetime.fromtimestamp(item.src.lstat().st_atime),
            "mtime": datetime.fromtimestamp(item.src.lstat().st_mtime),
            "ctime": datetime.fromtimestamp(item.src.lstat().st_ctime),
            "birthtime": datetime.fromtimestamp(item.src.lstat().st_birthtime),
        }
        return variables
