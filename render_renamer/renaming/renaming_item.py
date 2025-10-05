"""Items that need to be renamed."""


import enum
import logging
from pathlib import Path
from typing import Any
from uuid import UUID, uuid4


logger = logging.getLogger()


class RenamingItemStatus(enum.Enum):
    """Status of `RenamingItem`."""
    SRC = enum.auto()
    TMP = enum.auto()
    DST = enum.auto()


class RenamingItem:
    """Item that need to be renamed."""
    src: Path
    dst: Path | None
    tmp_name: UUID
    variables: dict[str, Any] = {}
    template: str | None
    status: RenamingItemStatus = RenamingItemStatus.SRC

    def __init__(
        self, src: Path, dst: Path | None = None,
        variables: dict[str, Any] | None = None,
        template: str | None = None,
        status: RenamingItemStatus = RenamingItemStatus.SRC
    ) -> None:
        self.src: Path = src
        self.dst: Path | None = dst
        self.tmp_name: UUID = uuid4()
        self.variables: dict[str, Any] = {} if not variables else variables
        self.template: str | None = template
        self.status: RenamingItemStatus = status

        self._generate_basic_variables()

    def __repr__(self) -> str:
        return f"<ReamingItem \"{self.src}\">"

    @property
    def tmp(self) -> Path:
        """Temporary file name."""
        return self.src.parent / str(self.tmp_name)

    def _generate_basic_variables(self) -> None:
        """Generate basic variables."""
        variables: dict[str, Any] = {
            "self": self.src,
            "size": self.src.lstat().st_size,
        }
        self.variables.update(variables)

    def has_changed(self) -> bool | None:
        """Check if the source and destination are different."""
        return None if (not self.dst) else (self.src != self.dst)
