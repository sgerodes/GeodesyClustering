from __future__ import annotations
from .enums import GeodeProjectionType, StickyType, CellType, GENERIC_CELL_TYPE
import typing as t
from collections import defaultdict


GENERIC_CELL = t.TypeVar("GENERIC_CELL", bound='Cell')


class Cell:
    def __init__(self, h: int, w: int, parent: 'GridLike', _type: GENERIC_CELL_TYPE):
        self.h = h
        self.w = w
        self.type = _type
        self.parent = parent

    def get_neighbors(self) -> t.Set[GENERIC_CELL]:
        return self.parent.get_neighbors_by_cell(self)


class ProjectionCell(Cell):
    def __init__(self, h: int, w: int, parent: 'GridLike', _type: GeodeProjectionType = GeodeProjectionType.EMPTY):
        super().__init__(h, w, parent, _type)


class StickyCell(Cell):
    def __init__(self, h: int, w: int, parent: 'GridLike', _type: StickyType = StickyType.EMTPY):
        super().__init__(h, w, parent, _type)


class Group:
    pass


class GroupManager:
    def __init__(self, parent: 'GridLike'):
        self.parent = parent


class GridLike(t.Generic[GENERIC_CELL]):
    def __init__(self, height: int, width: int):
        cell_type = self._get_model_type()
        self.grid: t.List[t.List[GENERIC_CELL]] = [[cell_type(h=h, w=w, parent=self) for w in range(width)] for h in range(height)]
        self.height = height
        self.width = width
        self.cells: t.Tuple[GENERIC_CELL] = tuple(cell for row in self.grid for cell in row)
        self.neighbours: t.Dict[GENERIC_CELL, t.Set[GENERIC_CELL]] = self.create_neighbours()
        self.type_to_cell: t.Dict[CellType, t.Set[GENERIC_CELL]] = self.populate_type_to_cell()

    @classmethod
    def _get_model_type(cls) -> t.Type[GENERIC_CELL]:
        # returns the actual cell type of the grid
        return t.get_args(cls.__orig_bases__[0])[0]  # noqa

    @classmethod
    def of_grid(cls, grid: t.List[t.List[CellType]]) -> GridLike:
        height = len(grid)
        width = len(grid[0])
        gl = cls(height, width)
        for h in range(height):
            for w in range(width):
                gl.set_elem_type(h, w, grid[h][w])
        return gl

    def populate_type_to_cell(self):
        type_to_cell = defaultdict(set)
        for cell in self.cells:
            type_to_cell[cell.type].add(cell)
        return type_to_cell

    def create_neighbours(self):
        neighbours = dict()
        for cell in self.cells:
            h = cell.h
            w = cell.w
            current_cell = self.get_elem(h, w)
            neigh = [(h-1, w), (h+1, w), (h, w-1), (h, w+1)]
            neigh = [n for n in neigh if 0 <= n[0] < self.height and 0 <= n[1] < self.width]
            neighbours[current_cell] = {self.get_elem(*n) for n in neigh}
        return neighbours

    def get_elem(self, h, w) -> GENERIC_CELL:
        return self.grid[h][w]

    def set_elem_type(self, h, w, _type: CellType):
        current_cell = self.grid[h][w]
        current_type = current_cell.type
        self.type_to_cell[current_type].remove(current_cell)
        self.grid[h][w].type = _type
        self.type_to_cell[_type].add(current_cell)

    def count_cell_with_type(self, _type: CellType):
        return len(self.type_to_cell[_type])

    def get_neighbors_by_coordinate(self, h, w) -> t.Set[GENERIC_CELL]:
        return self.get_neighbors_by_cell(self.get_elem(h, w))

    def get_neighbors_by_cell(self, cell: GENERIC_CELL) -> t.Set[GENERIC_CELL]:
        return self.neighbours[cell]


class Geode(GridLike[ProjectionCell]):
    pass


class Cluster(GridLike[StickyCell]):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group_manager = GroupManager(parent=self)

