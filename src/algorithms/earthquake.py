from src.classes import *
from itertools import product
from tests import layouts
import typing as t


def solve(gp: GeodesyProjection):
    cluster = Cluster(height=gp.height, width=gp.width)
    for h in range(gp.height):
        for w in range(gp.width):
            gp_elem = gp.get_elem(h, w)
            if gp_elem == GeodesyProjectionType.SHARD:
                cluster.set_elem_tuple((h, w), StickyType.SLIME)
