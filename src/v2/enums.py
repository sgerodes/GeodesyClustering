from enum import Enum
import typing as t


GENERIC_CELL_TYPE = t.TypeVar("GENERIC_CELL_TYPE", bound='CellType')


class CellType:
    pass


class GeodeProjectionType(CellType, Enum):
    EMPTY = 0
    BUD = 1
    SHARD = 2


class StickyType(CellType, Enum):
    EMTPY = 0
    SLIME = 1
    HONEY = 2

    def is_non_empty(self):
        return self.value >= 1
