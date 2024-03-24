"""Items that need to be renamed."""


import enum
import logging
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4

from rich.logging import RichHandler


logging.basicConfig(level=logging.DEBUG, format="%(message)s", handlers=(RichHandler(), ))
log = logging.getLogger()


class RenammingItemStatus(enum.Enum):
    """Status of `RenammingItem`."""
    SRC = enum.auto()
    TMP = enum.auto()
    DST = enum.auto()


class RenammingItem:
    """Item that need to be renamed."""
    src: Path
    dst: Path | None
    uuid: UUID
    variables: dict[str, Any] = {}
    template: str | None
    status: RenammingItemStatus = RenammingItemStatus.SRC

    def __init__(
        self, src: Path, dst: Path | None = None,
        variables: dict[str, Any] | None = None,
        template: str | None = None,
        status: RenammingItemStatus = RenammingItemStatus.SRC
    ) -> None:
        self.src: Path = src
        self.dst: Path | None = dst
        self.uuid = uuid4()
        self.variables: dict[str, Any] = {} if not variables else variables
        self.template: str | None = template
        self.status: RenammingItemStatus = status

        self._generate_basic_variables()

    def __repr__(self) -> str:
        return f"<ReammingItem \"{self.src}\">"

    @property
    def tmp(self) -> Path:
        """Temporary file name."""
        return self.src.parent / str(self.uuid)

    def _generate_basic_variables(self) -> None:
        """Generate basic variables."""
        variables: dict[str, Any] = {
            "self": self.src,
            "size": self.src.lstat().st_size,
        }
        self.variables.update(variables)

    def has_changed(self) -> bool | None:
        """
        Checks if the source path of the item is different than the destination path,
        indicating the item has changed and needs to be renamed.

        Returns:
            bool: True if item has changed, False if not changed.
            None: If destination is None.
        """
        return None if (not self.dst) else (self.src != self.dst)
