"""ABC of Addon for Rename.TXT."""


from abc import ABCMeta, abstractmethod
import enum
from typing import Any

from renamming.renamming import RenammingItem

from . import RenameTXTAddonType


class RenameTXTAddonExecuteWhen(enum.Enum):
    """
    Enumeration representing the execution timing of the Rename.TXT addon.

    Attributes:
        BEFORE_EDIT: Indicates that the addon executes before editing.
        AFTER_EDIT: Indicates that the addon executes after editing.
    """
    BEFORE_EDIT = enum.auto()
    AFTER_EDIT = enum.auto()


class RenameTXTAddonMeta(ABCMeta, RenameTXTAddonType):
    """Metaclass of RenameTXTAddon."""

    # Class property define in Metaclass.


class RenameTXTAddon(metaclass=RenameTXTAddonMeta):
    """ABC of Addon for Rename.TXT."""
    @property
    @abstractmethod
    def execute_when(self) -> list[RenameTXTAddonExecuteWhen]:
        """
        The execution timing of the Rename.TXT addon.

        Returns:
            list[RenameTXTAddonExecuteWhen]: A list of possible execution timings (BEFORE_EDIT or AFTER_EDIT).
        """
        return NotImplemented

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
