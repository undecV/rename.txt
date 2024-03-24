"""
Rename.TXT addon for Stat Time.
Datetime object of item.lstat().
"""


from datetime import datetime
from typing import Any

from renamming.renamming import RenammingItem

from . import RenameTXTAddonType
from .addons import RenameTXTAddon


class RTAStatTime(RenameTXTAddon):
    """
    Rename.TXT addon for Stat Time.
    Datetime object of item.lstat().
    """

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
            "atime": datetime.fromtimestamp(item.src.lstat().st_atime),
            "mtime": datetime.fromtimestamp(item.src.lstat().st_mtime),
            "ctime": datetime.fromtimestamp(item.src.lstat().st_ctime),
        }
        return variables
