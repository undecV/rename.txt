"""ABC of Addon for Rename.TXT."""


from abc import ABCMeta, abstractmethod
from typing import Any

from renamming.renamming import RenammingItem

from . import RenameTXTAddonType


class RenameTXTAddonMeta(ABCMeta, RenameTXTAddonType):
    """Metaclass of RenameTXTAddon."""


class RenameTXTAddon(metaclass=RenameTXTAddonMeta):
    """ABC of Addon for Rename.TXT."""
    @property
    @abstractmethod
    def acceptable_extension_names(self) -> list[str]:
        """
        Acceptable file extension names for pre-filtering,
        if it is an empty list, all files are accept.
        TODO: The filter has not been implemented yet.
        """
        return NotImplemented

    @property
    @abstractmethod
    def depends_on(self) -> list[RenameTXTAddonType]:
        """
        Other addons that the extension depends on.
        TODO: Addons dependency management has not been implemented yet.
        """
        return NotImplemented

    @abstractmethod
    def __init__(self, global_variables: dict[str, Any] | None = None) -> None:
        pass

    @abstractmethod
    def get_variables(self, item: RenammingItem) -> dict[str, Any]:
        """Retuen the variables."""
        return NotImplemented
