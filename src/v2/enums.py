from enum import Enum


class CellType:
    pass


class GeodProjectionType(Enum, CellType):
    EMPTY = 0
    BUD = 1
    SHARD = 2


class StickyType(Enum, CellType):
    EMTPY = 0
    SLIME = 1
    HONEY = 2
