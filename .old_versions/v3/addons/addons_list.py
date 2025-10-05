"""List of addons for Rename.TXT."""


from . import RenameTXTAddonType
from .rta_abbreviation import RTAAbbreviation
from .rta_naturalsize import RTANaturalsize
from .rta_stattime import RTAStatTime


addons_list: list[RenameTXTAddonType] = [
    RTAAbbreviation,
    RTANaturalsize,
    RTAStatTime,
]
