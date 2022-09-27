from src.classes import *


def test_group_manager():
    cluster = Cluster(height=5, width=5)
    gm = GroupManager(cluster)
    gm.set_coordinate_tuple((0, 0), StickyType.SLIME)
    assert gm.group_count() == 1

    gm.set_coordinate_tuple((1, 1), StickyType.SLIME)
    assert gm.group_count() == 2

    gm.set_coordinate_tuple((0, 1), StickyType.SLIME)
    assert gm.group_count() == 1

    #gm.remove_coordinate_tuple((0, 1))
    #assert gm.group_count() == 2
