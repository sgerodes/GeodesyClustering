import typing as t
import random
import enum
import math


class GridUtils:
    @staticmethod
    def get_manhattan_neighbour_coordinates(max_height, max_width, curr_height, curr_width) -> t.Set[t.Tuple]:
        ret = ((curr_height + 1, curr_width), (curr_height - 1, curr_width), (curr_height, curr_width + 1),
               (curr_height, curr_width - 1))
        return {coord for coord in ret if 0 <= coord[0] < max_height and 0 <= coord[1] < max_width}


class GeodBlockType(enum.Enum):
    BUDDING_AMETHYST = 0
    AIR = 1


class Axis(enum.Enum):
    X = 0
    Y = 1
    Z = 2


class GeodeMockUtils:
    MIN_X = 10  # this number is made up, not real data
    MIN_Y = 10  # this number is made up, not real data
    MIN_Z = 10  # this number is made up, not real data
    MAX_X = 13
    MAX_Y = 14
    MAX_Z = 15
    BUD_SPAWN_ATTEMPTS = 100
    BUD_SPAWN_SUCCESS_RATE_MIN = 0.25
    BUD_SPAWN_SUCCESS_RATE_MAX = 0.5
    BUD_DISTANCE_FROM_CENTRE = 0.6

    @staticmethod
    def generate_mock_geode(min_x=MIN_X, min_y=MIN_Y, min_z=MIN_Z,
                            max_x=MAX_X, max_y=MAX_Y, max_z=MAX_Z):
        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)
        z = random.randint(min_z, max_z)
        volume = x * y * z
        max_volume = GeodeMockUtils.MAX_X * GeodeMockUtils.MAX_Y * GeodeMockUtils.MAX_Z
        min_volume = GeodeMockUtils.MIN_X * GeodeMockUtils.MIN_Y * GeodeMockUtils.MIN_Z
        bud_spawn_success_rate = (volume - min_volume) / (max_volume - min_volume) \
                                 * (GeodeMockUtils.BUD_SPAWN_SUCCESS_RATE_MAX - GeodeMockUtils.BUD_SPAWN_SUCCESS_RATE_MIN)
        bud_spawn_success_rate += GeodeMockUtils.BUD_SPAWN_SUCCESS_RATE_MIN

        geode = [[[GeodBlockType.AIR for _ in range(z)] for _ in range(y)] for _ in range(x)]

        geode_centre = (x//2, y//2, z//2)
        bud_radius = (x - geode_centre[0]) // (1 / GeodeMockUtils.BUD_DISTANCE_FROM_CENTRE)

        buds_coords = [GeodeMockUtils.get_random_point_on_a_sphere(geode_centre, bud_radius)
                       for _ in range(GeodeMockUtils.BUD_SPAWN_ATTEMPTS)
                       if random.random() < bud_spawn_success_rate]

        for x, y, z in buds_coords:
            geode[x][y][z] = GeodBlockType.BUDDING_AMETHYST

        return geode

    @staticmethod
    def get_random_point_on_a_sphere(centre, radius):
        theta = random.random() * math.pi * random.choice((-1, 1))
        phi = random.random() * math.pi * random.choice((-1, 1))
        return (
            round(centre[0] + radius * math.sin(theta) * math.cos(phi) * (random.random()*0.2+0.9)),
            round(centre[1] + radius * math.sin(theta) * math.sin(phi) * (random.random()*0.2+0.9)),
            round(centre[2] + radius * math.cos(theta) * (random.random()*0.2+0.9))
        )

    @staticmethod
    def get_projection(geode, axis: Axis):
        x_max = len(geode)
        y_max = len(geode[0])
        z_max = len(geode[0][0])
        if axis is Axis.X:
            projection = [[GeodBlockType.AIR for _ in range(z_max)] for _ in range(y_max)]
            for x in range(x_max):
                for y in range(y_max):
                    for z in range(z_max):
                        if geode[x][y][z] is GeodBlockType.BUDDING_AMETHYST:
                            projection[y][z] = GeodBlockType.BUDDING_AMETHYST
        elif axis is Axis.Y:
            projection = [[GeodBlockType.AIR for _ in range(z_max)] for _ in range(x_max)]
            for x in range(x_max):
                for y in range(y_max):
                    for z in range(z_max):
                        if geode[x][y][z] is GeodBlockType.BUDDING_AMETHYST:
                            projection[x][z] = GeodBlockType.BUDDING_AMETHYST
        elif axis is Axis.Z:
            projection = [[GeodBlockType.AIR for _ in range(y_max)] for _ in range(x_max)]
            for x in range(x_max):
                for y in range(y_max):
                    for z in range(z_max):
                        if geode[x][y][z] is GeodBlockType.BUDDING_AMETHYST:
                            projection[x][y] = GeodBlockType.BUDDING_AMETHYST
        return projection


size = 15
g = GeodeMockUtils.generate_mock_geode(min_x=size, min_y=size, min_z=size, max_x=size, max_y=size, max_z=size)
px = GeodeMockUtils.get_projection(g, Axis.X)
py = GeodeMockUtils.get_projection(g, Axis.Y)
pz = GeodeMockUtils.get_projection(g, Axis.Z)

m = {
    GeodBlockType.BUDDING_AMETHYST: '#',
    GeodBlockType.AIR: ' ',
}

for row in px:
    print(''.join([m.get(elem) for elem in row]))

for row in py:
    print(''.join([m.get(elem) for elem in row]))

for row in pz:
    print(''.join([m.get(elem) for elem in row]))


print()
