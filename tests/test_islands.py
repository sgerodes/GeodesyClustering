# def test_layout_creation():
#     sticky_layout = Cluster(layout=layout1)
#     assert sticky_layout.get_slime_count() == 2
#     assert sticky_layout.get_honey_count() == 3
#     assert sticky_layout.height == 3
#     assert sticky_layout.width == 4
#
#
# def test_islands():
#     sticky_layout = Cluster(layout=layout1)
#     assert StickyScore.calculate_groups(sticky_layout) == 2
#
#     sticky_layout2 = Cluster(layout=layout2)
#     assert StickyScore.calculate_groups(sticky_layout2) == 4
#
#     assert StickyScore(sticky_layout).is_better_than(StickyScore.of_cluster(sticky_layout2))
