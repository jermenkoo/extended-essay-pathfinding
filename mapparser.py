import os

from constants import *

D = {".": "0", "G": "0", "@": "1", "O": "1", "T": "1", "S": "1", "W": "1"}


def replace_all(t, d=D):
    """Replaces the map to be compatible with the testing script."""
    for i, j in d.items():
        t = t.replace(i, j)
    return t


def parsescen(scen):
    r = []
    i = 0
    with open(scen) as f:
        f.readline()
        for line in f:
            # split the scenario line either by space or tab
            # depends on the version of the scenario file
            l = line.split(" ") if not "\t" in line else line.split("\t")
            # parse the coordinates of start, goal and distance between them
            s = (int(l[4]), int(l[5]))
            g = (int(l[6]), int(l[7]))
            d = float(l[8])
            # if the start is different from goal and the shortest-path exists
            if s != g and d > 0.0:
                r.append([s, g])
                i += 1
            # return the 20 scenarios
            if i == 20:
                return r


def parsemap_WHOLE(map):
    """Given a path to the map, returns array of maps according to the scenario"""
    r = []
    with open(map) as f:
        d = map.split("\\")[-2][3:]
        n = map.split("\\")[-1]

        # read type, height, width, map (notes begin of the map)
        f.readline()
        h = int(f.readline().split()[-1])
        w = int(f.readline().split()[-1])
        f.readline()

        # if the map is not square-shaped or it is too big
        if (h != w) or (h * w >= 512 * 512):
            return None, None

        # replaces map to be compatible with the testing script
        v = [replace_all(line) for line in f]
        # path to scenario
        s = os.getcwd().replace("\\", "\\\\") + \
            "\\\\scen" + d + "\\\\" + n + ".scen"
        # parsescenarios
        t = parsescen(s)
        # iterate through each case in testcases
        for c in t:
            m = v
            #start, goal = testcase
            s, g = c
            # split the string, assign start and target and indices
            m = [list(x) for x in v]
            m[s[1]][s[0]] = 'S'
            m[g[1]][g[0]] = 'T'
            # re-create the map back
            m = ''.join([''.join(l) for l in m])
            r.append(m)
    # return maps and name of the map
    return r, n
