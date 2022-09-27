import enum
import typing as t
from collections import Counter
from copy import deepcopy
from src.v1.constants import PUNCH_LIMIT
from collections import defaultdict
from src.v1.utils import GridUtils


class GeodesyProjectionType(enum.Enum):
    EMPTY = 0
    BUD = 1
    SHARD = 2

    def __repr__(self):
        repr_map: t.Dict[int, str] = {
            0: ' ',
            1: '#',
            2: '.',
        }
        return repr_map[self.value]


class StickyType(enum.Enum):
    EMTPY = 0
    SLIME = 1
    HONEY = 2

    def __repr__(self):
        repr_map: t.Dict[int, str] = {
            0: 'e',
            1: 'S',
            2: 'H',
        }
        return repr_map[self.value]


class Group:
    def __init__(self, group_id, sticky_type: StickyType):
        self.coordinates: t.Set[t.Tuple[int, int]] = set()
        self.group_id: int = group_id
        self.bars = set()  # saves all length 3 bars in a format ((1,1),(1,2),(1,3))
        self.coord_2_bars: t.Dict[t.Tuple, t.Set] = defaultdict(set)  # a multidict
        self.sticky_type: StickyType = sticky_type

    @property
    def size(self):
        return len(self.coordinates)

    def has_bars(self) -> bool:
        return len(self.coord_2_bars) > 0

    def create_bar_from_coordinates(self, c1: t.Tuple, c2: t.Tuple, c3: t.Tuple) -> t.Tuple[t.Tuple, t.Tuple, t.Tuple]:
        # TODO in order to guarantee the saving and removing, the order is the bars needs to be always the same
        return tuple(sorted([c1, c2, c3]))

    def save_bar(self, bar: t.Tuple[t.Tuple, t.Tuple, t.Tuple]):
        # TODO in order to guarantee the saving and removing, the order is the bars needs to be always the same
        self.bars.add(bar)
        for coord in bar:
            self.coord_2_bars[coord].add(bar)

    def remove_bar(self, bar: t.Tuple[t.Tuple, t.Tuple, t.Tuple]):
        self.bars.remove(bar)
        for coord in bar:
            self.coord_2_bars[coord].remove(bar)
            if len(self.coord_2_bars[coord]) == 0:
                del self.coord_2_bars[coord]

    def add_coordinate(self, h, w):
        # O(1) time
        self.add_coordinate_tuple((h, w))

    def remove_coordinate(self, h, w):
        # O(1) time
        self.remove_coordinate_tuple((h, w))

    def has_coordinates(self, h, w):
        # O(1) time
        return self.has_coordinates_tuple((h, w))

    def add_coordinate_tuple(self, coord_tuple: tuple):
        # O(1) time
        self.coordinates.add(coord_tuple)
        # TODO
        # if self.creates_a_bars(coord_tuple):
        #    self.save_bar()

    def remove_coordinate_tuple(self, coord_tuple: tuple):
        # O(1) time
        self.coordinates.remove(coord_tuple)
        # TODO
        # if self.breaks_bars(coord_tuple):
        #    self.remove_bar()

    def has_coordinates_tuple(self, coord_tuple: tuple):
        # O(1) time
        return coord_tuple in self.coordinates

    def __repr__(self):
        return repr(self.coordinates)


class GroupManager:
    def __init__(self, cluster: 'Cluster'):
        self.new_group_id = 0
        self.cluster = cluster
        self.id_2_group: t.Dict[int, Group] = dict()  # group_id to group
        self.coord_2_group: t.Dict[t.Tuple[int, int], Group] = dict()  # coord (h, w) to group
        self.sticky_type_2_group: t.Dict[StickyType, t.Set[Group]] = defaultdict(set)  # sticky_type

    def group_count(self):
        return len(self.id_2_group)

    def get_group_by_coordinate_tuple(self, coord: t.Tuple[int, int]) -> t.Optional[Group]:
        return self.coord_2_group.get(coord)

    def get_group_by_group_id(self, group_id: int) -> t.Optional[Group]:
        return self.id_2_group.get(group_id)

    def set_coordinate_tuple(self, coord: t.Tuple[int, int], st: StickyType) -> Group:
        if coord in self.coord_2_group and self.coord_2_group[coord] != st:
            self.remove_coordinate_tuple(coord)

        neigh = GridUtils.get_manhattan_neighbour_coordinates(max_height=self.cluster.height,
                                                              max_width=self.cluster.width,
                                                              curr_height=coord[0],
                                                              curr_width=coord[1])
        # try to add to a group
        parent_group: t.Optional[Group] = None
        for n in neigh:
            if n in self.coord_2_group:
                neigh_group = self.coord_2_group.get(n)
                if parent_group:
                    self.merge_groups(parent_group, neigh_group)
                else:
                    neigh_group.add_coordinate_tuple(n)
                    parent_group = neigh_group

        # if no group found, create a group
        if not parent_group:
            parent_group = Group(group_id=self.new_group_id, sticky_type=st)
            self.new_group_id += 1
            parent_group.add_coordinate_tuple(coord)
            self.id_2_group[parent_group.group_id] = parent_group
            self.coord_2_group[coord] = parent_group
            self.sticky_type_2_group[st].add(parent_group)

        return parent_group

    def remove_coordinate_tuple(self, coord: t.Tuple[int, int]):
        # means this coordinate will be StickyType.EMTPY
        if coord in self.coord_2_group:
            group = self.coord_2_group.get(coord)
            group.remove_coordinate_tuple(coord)
            del self.coord_2_group[coord]
            self.sticky_type_2_group[group.sticky_type].remove(group)
            if group.size == 0:
                del self.id_2_group[group.group_id]

    @staticmethod
    def is_merging_groups_within_punch_limit(group1: Group, group2: Group) -> bool:
        return group1.size + group2.size <= PUNCH_LIMIT

    @staticmethod
    def is_group_valid_for_flying_machine(group: Group):
        return 2 <= group.size <= PUNCH_LIMIT

    def merge_groups(self, group1: Group, group2: Group):
        for coord in group2.coordinates:
            self.coord_2_group[coord] = group1
            group1.add_coordinate_tuple(coord)
            # group2.remove_coordinate_tuple(coord)  # probably unnecessary, because the group is dropped
        del self.id_2_group[group2.group_id]
        self.sticky_type_2_group[group2.sticky_type].remove(group2)


class Cluster:
    def __init__(self, layout: t.List[t.List[StickyType]] = None,
                 height: int = None,
                 width: int = None):
        self.layout = [[StickyType.EMTPY for _ in range(width)] for _ in range(height)]
        self.sticky_counter = sum(map(Counter, self.layout), Counter())
        self.height = height
        self.width = width
        self.group_manager = GroupManager(self)
    # def __init__(self, layout: t.List[t.List[StickyType]] = None,
    #              height: int = None,
    #              width: int = None):
    #     if layout:
    #         self.layout: t.List[t.List[StickyType]] = layout
    #         self.sticky_counter = sum(map(Counter, layout), Counter())
    #         self.height = len(layout)
    #         self.width = 0 if len(layout) == 0 else len(layout[0])
    #     elif height is not None and width is not None:
    #         self.layout = [[StickyType.EMTPY] * width] * height
    #         self.sticky_counter: t.Dict[StickyType] = Counter()
    #         self.height = height
    #         self.width = width
    #     else:
    #         raise RuntimeError("Wrong init for StickyLayout")

    def get_slime_count(self) -> int:
        return self.sticky_counter[StickyType.SLIME]

    def get_honey_count(self) -> int:
        return self.sticky_counter[StickyType.HONEY]

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def get_elem(self, h, w) -> StickyType:
        return self.layout[h][w]

    def get_elem_tuple(self, coord) -> StickyType:
        return self.get_elem(coord[0], coord[1])

    def set_elem(self, h, w, st: StickyType):
        self.set_elem_tuple((h, w), st)

    def set_elem_tuple(self, coord, st: StickyType):
        h, w = coord
        self.sticky_counter[self.layout[h][w]] -= 1
        self.sticky_counter[st] += 1
        self.layout[h][w] = st
        self.group_manager.set_coordinate_tuple(coord, st)

    def __repr__(self):
        r = list()
        for row in self.layout:
            r.append(repr(row))
        return '\n'.join(r)


class StickyScore:
    def __init__(self, cluster: Cluster):
        self.groups_count = 0
        self.groups_matrix = None
        self.slime_material = cluster.get_slime_count()
        self.honey_material = cluster.get_honey_count()
        self.calculate_groups(cluster)

    @property
    def sticky_material(self):
        return self.slime_material + self.honey_material

    @staticmethod
    def get_manhattan_neighbour_coordinates(max_height, max_width, curr_height, curr_width) -> t.Set[t.Tuple]:
        ret = ((curr_height+1, curr_width), (curr_height-1, curr_width), (curr_height, curr_width+1), (curr_height, curr_width-1))
        return {coord for coord in ret if 0 <= coord[0] < max_height and 0 <= coord[1] < max_width}

    def calculate_groups(self, cluster: Cluster):
        self.groups_matrix = [[0] * cluster.get_width() for _ in range(cluster.get_height())]
        for h in range(cluster.get_height()):
            for w in range(cluster.get_width()):
                curr_type = cluster.get_elem(h, w)
                if curr_type != StickyType.EMTPY and self.groups_matrix[h][w] == 0:
                    self.groups_count += 1
                    coordinates_to_check = [(h, w)]
                    # mark groups with bfs
                    while coordinates_to_check:
                        coord = coordinates_to_check.pop()
                        if cluster.get_elem(coord[0], coord[1]) == curr_type and self.groups_matrix[coord[0]][coord[1]] == 0:
                            self.groups_matrix[coord[0]][coord[1]] = self.groups_count

                            neigh_coords = StickyScore.get_manhattan_neighbour_coordinates(cluster.get_height(),
                                                                                           cluster.get_width(),
                                                                                           coord[0],
                                                                                           coord[1])

                            for nc in neigh_coords:
                                if cluster.get_elem(nc[0], nc[1]) == curr_type and self.groups_matrix[nc[0]][nc[1]] == 0:
                                    coordinates_to_check.append(nc)

    def is_better_than(self, other: 'StickyScore') -> bool:
        # better is defined by firstly having less island, secondly by having less overall blocks
        if self.groups_count < other.groups_count:
            return True
        if self.groups_count == other.groups_count and self.sticky_material < other.sticky_material:
            return True
        return False

    def __repr__(self):
        return f'{self.__class__}({self.groups_count=} {self.sticky_material=})'


class GeodesyProjection:
    def __init__(self, layout: t.List[t.List[GeodesyProjectionType]]):
        self.initial_layout = deepcopy(layout)
        self.layout: t.List[t.List[GeodesyProjectionType]] = deepcopy(layout)
        self.h_offset = 0
        self.w_offset = 0
        #self.reduce_empty_rows()
        self.height = len(self.layout)
        self.width = 0 if len(self.layout) == 0 else len(self.layout[0])
        self.buds_coordinates = set()
        self.shards_coordinates = set()
        self.empty_coordinates = set()
        self.find_all_coordinates()

    def get_elem(self, h, w) -> GeodesyProjectionType:
        return self.layout[h][w]

    def is_valid_cluster(self, cluster: Cluster) -> bool:
        for bud_coord in self.buds_coordinates:
            if cluster.get_elem_tuple(bud_coord) != StickyType.EMTPY:
                return False
        for shard_coord in self.shards_coordinates:
            if cluster.get_elem_tuple(shard_coord) == StickyType.EMTPY:
                return False
        return True

    def find_all_coordinates(self):
        self.find_coordinates_of(GeodesyProjectionType.BUD)
        self.find_coordinates_of(GeodesyProjectionType.SHARD)
        self.find_coordinates_of(GeodesyProjectionType.EMPTY)

    def find_coordinates_of(self, gpt: GeodesyProjectionType):
        for h in range(self.height):
            for w in range(self.width):
                if self.get_elem(h, w).value == gpt.value:
                    if gpt.value == gpt.BUD.value:
                        self.buds_coordinates.add((h, w))
                    elif gpt.value == gpt.SHARD.value:
                        self.shards_coordinates.add((h, w))
                    elif gpt.value == gpt.EMPTY.value:
                        self.empty_coordinates.add((h, w))

    def reduce_empty_rows(self):
        while self.row_is_all_empty(0):
            self.h_offset += 1
            self.layout.pop(0)
        while self.row_is_all_empty(len(self.layout)-1):
            self.layout.pop()
        while self.column_is_all_empty(0):
            self.w_offset += 1
            for row in self.layout:
                row.pop(0)
        while self.column_is_all_empty(len(self.layout[0])-1):
            for row in self.layout:
                row.pop(len(self.layout[0])-1)
        if self.h_offset or self.w_offset:
            print(f'Cluster was reduced {self.h_offset=} {self.w_offset=}')

    def row_is_all_empty(self, row_number: int) -> bool:
        return all(e.value == GeodesyProjectionType.EMPTY.value for e in self.layout[row_number])

    def column_is_all_empty(self, column_number: int) -> bool:
        return all(row[column_number].value == GeodesyProjectionType.EMPTY.value for row in self.layout)

    _repr_mapping = {
        GeodesyProjectionType.BUD: '#',
        GeodesyProjectionType.EMPTY: ' ',
        GeodesyProjectionType.SHARD: '.',
    }

    def __repr__(self):
        r = list()
        for row in self.layout:
            r.append(''.join(GeodesyProjection._repr_mapping[elem] for elem in row))
        return '\n'.join(r)
