from constants import *


class InvalidMap(Exception):
    pass


def is_walkable(x, y, s, m):
    """Return whether the given coordinate resides inside the map
    and its status is NORMAL.
    """
    return x >= 0 and x < s and \
        y >= 0 and y < s and \
        m[y][x] != BLOCKED


def make_graph(s):
    """
    Generate an adjacency-list-represented graph from a multi-line string.

    :Parameters:
        s : str
            A multi-line string representing the maze.
            A sample string is as follows:
            s = '''
                1001
                0100
                1001
                '''

    :Return:
        graph : {(x1, y1): {(x2, y2): dist, ... }, ... }
            The graph is in ajacency list representation.
            The graph generated using the sample input above is as follows:
            graph = {(0, 1): {},
                     (1, 2): {(2, 1): 14, (2, 2): 10},
                     (3, 1): {(2, 0): 14, (2, 1): 10, (2, 2): 14},
                     (2, 1): {(1, 2): 14, (2, 0): 10, (1, 0): 14, (3, 1): 10, (2, 2): 10},
                     (2, 0): {(1, 0): 10, (3, 1): 14, (2, 1): 10},
                     (2, 2): {(1, 2): 10, (3, 1): 14, (2, 1): 10},
                     (1, 0): {(2, 0): 10, (2, 1): 14}}

        source : (x, y)
            source coordinate

        target : (x, y)
            target coordinate

    """
    try:
        nodes_map = [list(row) for row in s.split()]
        size = len(nodes_map)
    except:
        raise InvalidMap("The given raw map may be invalid")

    # put all available nodes into the graph
    g = dict([((x, y), {})
              for x in range(size)
              for y in range(size)
              if nodes_map[y][x] != BLOCKED])
    source = None
    target = None

    for x in range(size):
        for y in range(size):
            if nodes_map[y][x] == SOURCE:
                source = (x, y)
            elif nodes_map[y][x] == TARGET:
                target = (x, y)
            if is_walkable(x, y, size, nodes_map):
                for i in range(len(XOFFSET)):
                    # inspect horizontal and vertical adjacent nodes
                    nx = x + XOFFSET[i]
                    ny = y + YOFFSET[i]
                    if is_walkable(nx, ny, size, nodes_map):
                        g[(x, y)][(nx, ny)] = DIST
                        # further inspect diagonal nodes
                        nx = x + DAXOFFSET[i]
                        ny = y + DAYOFFSET[i]
                        if is_walkable(nx, ny, size, nodes_map):
                            g[(x, y)][(nx, ny)] = DDIST
                        nx = x + DBXOFFSET[i]
                        ny = y + DBYOFFSET[i]
                        if is_walkable(nx, ny, size, nodes_map):
                            g[(x, y)][(nx, ny)] = DDIST
    return g, source, target
