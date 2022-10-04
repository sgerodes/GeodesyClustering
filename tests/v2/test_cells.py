from src.v2.enums import GeodeProjectionType, StickyType, CellType, GENERIC_CELL_TYPE


def test_emptiness():
    empty = StickyType.EMTPY
    slime = StickyType.SLIME
    honey = StickyType.HONEY

    assert slime.is_non_empty()
    assert honey.is_non_empty()
    assert not empty.is_non_empty()

