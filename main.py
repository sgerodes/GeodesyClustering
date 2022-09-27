from src import read_resource_geodes


if __name__ == '__main__':
    for g in read_resource_geodes():
        r = repr(g)
        print(r, '\n')
