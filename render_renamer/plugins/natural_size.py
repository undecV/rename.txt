"""Natural size plugin to extract natural size from filenames."""

from typing import Any
from render_renamer.renaming.renaming_item import RenamingItem
from render_renamer.utilities.miscellaneous import readable_size
from ._base import RenderRenamerAddon


class RRNaturalSizeAddon(RenderRenamerAddon):
    """Natural size plugin to extract natural size from filenames."""

    def get_variables(self, item: RenamingItem) -> dict[str, Any]:
        variables: dict[str, Any] = {
            "natural": {
                "size": readable_size(item.variables.get("size", 0)),
            }
        }
        return variables
