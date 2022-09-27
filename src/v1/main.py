from classes import *
from itertools import product
from tests import layouts
import typing as t


def main():
    calculate_brute_force(GeodesyProjection(layout=layouts.projection_layout_5))


def calculate_brute_force(geodesy_projection: GeodesyProjection):
    best: t.Optional[Cluster] = None
    best_scoring: t.Optional[StickyScore] = None

    for cluster_layout in variations(StickyType, geodesy_projection.height, geodesy_projection.width):
        cluster = Cluster(layout=cluster_layout)
        if geodesy_projection.is_valid_cluster(cluster):
            if best is None:
                print(f"Found first \n{cluster}\n")
                best = cluster
                best_scoring = StickyScore(cluster)
            else:
                curr = StickyScore(cluster)
                if curr.is_better_than(best_scoring):
                    print(f"Found better \n{cluster}\n")
                    best = cluster
                    best_scoring = curr

    print('best:')
    print(best_scoring)
    print(best)


def variations(items, height, width):
    for one in product(items, repeat=width*height):
        yield [list(one[i*width:(i+1)*width]) for i in range(height)]


if __name__ == '__main__':
    main()
    #for mtx in variations(StickyType, 2, 2):
    #    print(mtx)
    #    print()
