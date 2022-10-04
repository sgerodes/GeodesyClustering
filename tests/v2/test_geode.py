from src.v2.classes import Geode, GeodeProjectionType
from tests.v2.layouts import *


def test_geode():
    geode = Geode.of_grid(projection_layout_1)
    assert geode.count_cell_with_type(GeodeProjectionType.EMPTY) == 1
    assert geode.count_cell_with_type(GeodeProjectionType.SHARD) == 2
    assert geode.count_cell_with_type(GeodeProjectionType.BUD) == 1
    assert len(geode.cells) == 4

    assert len(geode.get_neighbors_by_coordinate(0, 0)) == 2
    assert geode.get_elem(1, 0) in geode.get_neighbors_by_coordinate(0, 0)
    assert geode.get_elem(0, 1) in geode.get_neighbors_by_coordinate(0, 0)
    assert geode.get_elem(1, 1) not in geode.get_neighbors_by_coordinate(0, 0)

    assert geode.get_elem(0, 0).type is GeodeProjectionType.SHARD
    geode.set_elem_type(0, 0, GeodeProjectionType.BUD)
    assert geode.count_cell_with_type(GeodeProjectionType.BUD) == 2
    assert geode.count_cell_with_type(GeodeProjectionType.SHARD) == 1
    assert geode.get_elem(0, 0).type is GeodeProjectionType.BUD

