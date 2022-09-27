import typing as t
from src.v1.classes import GeodesyProjectionType, GeodesyProjection


test_resources_mapping = {
    '#': GeodesyProjectionType.BUD,
    '.': GeodesyProjectionType.SHARD,
    ' ': GeodesyProjectionType.EMPTY,
}


def is_line_empty(line: str):
    # return line.replace(' ', '').replace('\n', '') == ''
    return line == '\n'


def geod_projection_from_string(geod: t.List[str]) -> GeodesyProjection:
    layout: t.List[t.List[GeodesyProjectionType]] = list()
    for line in geod:
        line = line.replace('..', '.')
        line = line.replace('##', '#')
        line = line.replace('  ', ' ')
        line = line.replace('\n', ' ')
        layout.append([test_resources_mapping[c] for c in line])
    return GeodesyProjection(layout=layout)


def read_resource_geodes() -> t.List[GeodesyProjection]:
    with open('resources/geodes.txt', 'r') as f:
        gp_list = list()
        geod = list()
        for line in f.readlines():
            if not is_line_empty(line):
                geod.append(line)
            if is_line_empty(line) and geod:
                gp_list.append(geod_projection_from_string(geod))
                geod = list()
        return gp_list

