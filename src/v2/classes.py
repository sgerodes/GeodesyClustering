from .enums import GeodProjectionType, StickyType, CellType
import typing as t
from collections import defaultdict


class Cell:
    def __init__(self, h: int, w: int):
        self.h = h
        self.w = w
        self.type = None


class ProjectionCell(Cell):
    def __init__(self, h: int, w: int, _type: GeodProjectionType):
        super().__init__(h, w)
        self.type = _type


class StickyCell(Cell):
    def __init__(self, h: int, w: int, _type: StickyType):
        super().__init__(h, w)
        self.type = _type


class GridLike:
    empty_types = {
        ProjectionCell: GeodProjectionType.EMPTY,
        StickyCell: StickyType.EMTPY
    }

    def __init__(self, height: int, width: int, cell_type: t.Type[t.Union[ProjectionCell, StickyCell]]):
        empty_type = GridLike.empty_types.get(cell_type)
        self.grid = [[cell_type(h, w, empty_type) for w in range(width)] for h in range(height)]

        self.neighbours: t.Dict[Cell, t.Set[Cell]] = dict()
        self.populate_neighbours()

        self.type_to_cell: t.Dict[CellType, t.Set[Cell]] = defaultdict(set)
        self.populate_type_to_cell()

    def populate_type_to_cell(self):
        height = len(self.grid)
        width = len(self.grid[0] if len(self.grid) > 0 else 0)
        for h in range(height):
            for w in range(width):
                current_cell = self.get_elem(h, w)
                self.type_to_cell[current_cell.type].add(current_cell)

    def populate_neighbours(self):
        height = len(self.grid)
        width = len(self.grid[0] if len(self.grid) > 0 else 0)
        for h in range(height):
            for w in range(width):
                current_cell = self.get_elem(h, w)
                neigh = [(h-1, w), (h+1, w), (h, w-1), (h, w+1)]
                neigh = [n for n in neigh if 0 <= n[0] < height and 0 <= n[1] < width]
                self.neighbours[current_cell] = {self.get_elem(*n) for n in neigh}

    def get_elem(self, h, w) -> Cell:
        return self.grid[h][w]

    def set_elem_type(self, h, w, _type: CellType):
        current_cell = self.grid[h][w]
        current_type = current_cell.type
        self.type_to_cell[current_type].remove(current_cell)
        self.grid[h][w].type = _type
        self.type_to_cell[_type].add(current_cell)

    def count_cell_with_type(self, _type: CellType):
        return len(self.type_to_cell[_type])

    def get_neighbors_by_coordinate(self, h, w) -> t.Set[Cell]:
        return self.neighbours[self.get_elem(h, w)]

    def get_neighbors_by_cell(self, cell: Cell) -> t.Set[Cell]:
        return self.neighbours[cell]


class Geode(GridLike):
    def __init__(self, height, width):
        super().__init__(height, width, ProjectionCell)

    def get_elem(self, h, w) -> ProjectionCell:
        return super().get_elem(h, w)


class Cluster(GridLike):
    def __init__(self, height, width):
        super().__init__(height, width, StickyCell)


class Group:
    pass


class GroupManager:
    pass