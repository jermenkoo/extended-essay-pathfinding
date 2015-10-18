import cProfile
import pstats
import psutil
import os
import sys

from astar import AStar
from bidirbfs import BiDirBFS
from constants import *
from dijkstra import GridDijkstra
from io import StringIO
from mazegen import mgen
from mapparser import parsemap_WHOLE


# based on the answer of Triptych on StackOverflow:
# http://stackoverflow.com/a/616672/825916
class Logger(object):

    """Class for duplication of stdout both to terminal and file."""

    def __init__(self):
        self.terminal = sys.stdout
        self.log = open("results_h", "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        self.terminal.flush()
        self.log.flush()

# set stdout to Logger() class
sys.stdout = Logger()

At = []
Af = []

Aet = []
Aef = []

Act = []
Acf = []

Bt = []
Bf = []

Dt = []
Df = []


# A*
def A(m, h=0):
    a = AStar(m, h)
    for i in a.step():
        pass
    if not a.path:
        raise Exception("\a[!] A* PATH NOT FOUND!")


# Bi-directional BFS
def B(m):
    bdbfs = BiDirBFS(m)
    for i in bdbfs.step():
        pass
    if not bdbfs.path:
        raise Exception("\a[!] Bi-dirBFS PATH NOT FOUND!")


# Dijkstra
def D(m):
    d = GridDijkstra(m)
    for i in d.step():
        pass
    if not d.path:
        raise Exception("\a[!] Dijkstra PATH NOT FOUND!")

# get the ID assigned to the testing script
p = psutil.Process(os.getpid())
# set the priority to realtime
p.set_nice(psutil.REALTIME_PRIORITY_CLASS)

# walk to current working folder to find all the maps which are there
for root, dirs, files in os.walk(os.getcwd()):
    for file in files:
        if file.endswith(".map") and "map" in root:
            r, n = parsemap_WHOLE(os.path.join(root, file))
            if r is not None:
                print(n)
                for i, j in enumerate(r):
                    case = j
                    p = cProfile
                    #A* - manhattan
                    p.run("A(case)", filename="statsfile")
                    stream = StringIO()
                    stats = pstats.Stats('statsfile', stream=stream)
                    stats.print_stats()
                    s = str(stream.getvalue()).split()

                    Af.append(s[6])
                    At.append(s[10])
                    print("[*]A*M - {}/20 done. F: {} T: {}".format(
                        i + 1, Af[-1], At[-1]))

                    #A* - euclidean
                    p.run("A(case, 1)", filename="statsfile")
                    stream = StringIO()
                    stats = pstats.Stats('statsfile', stream=stream)
                    stats.print_stats()
                    s = str(stream.getvalue()).split()

                    Aef.append(s[6])
                    Aet.append(s[10])
                    print("[*]A*E - {}/20 done. F: {} T: {}".format(
                        i + 1, Aef[-1], Aet[-1]))

                    #A* - chebyshev
                    p.run("A(case, 2)", filename="statsfile")
                    stream = StringIO()
                    stats = pstats.Stats('statsfile', stream=stream)
                    stats.print_stats()
                    s = str(stream.getvalue()).split()

                    Acf.append(s[6])
                    Act.append(s[10])
                    print("[*]A*C - {}/20 done. F: {} T: {}".format(
                        i + 1, Acf[-1], Act[-1]))

                    # Bi-directional BFS
                    p.run("B(case)", filename="statsfile")
                    stream = StringIO()
                    stats = pstats.Stats('statsfile', stream=stream)
                    stats.print_stats()
                    s = str(stream.getvalue()).split()

                    Bf.append(s[6])
                    Bt.append(s[10])
                    print("[*]B - {}/20 done. F: {} T: {}".format(
                        i + 1, Bf[-1], Bt[-1]))

                    # Dijkstra
                    p.run("D(case)", filename="statsfile")
                    stream = StringIO()
                    stats = pstats.Stats('statsfile', stream=stream)
                    stats.print_stats()
                    s = str(stream.getvalue()).split()

                    Df.append(s[6])
                    Dt.append(s[10])
                    print("[*]D - {}/20 done. F: {} T: {}".format(
                        i + 1, Df[-1], Dt[-1]))

print("MAPS")
#A* - manhattan
print("A*")
print("AVG CALLS: {}".format(sum(map(int, Af)) // len(Af)))
print("AVG TIMES: {}".format(sum(map(float, At)) / len(At)))
#A* - euclidean
print("A*E")
print("AVG CALLS: {}".format(sum(map(int, Aef)) // len(Aef)))
print("AVG TIMES: {}".format(sum(map(float, Aet)) / len(Aet)))
#A* - chebyshev
print("A*C")
print("AVG CALLS: {}".format(sum(map(int, Acf)) // len(Acf)))
print("AVG TIMES: {}".format(sum(map(float, Act)) / len(Act)))
# Bi-dirBFS
print("B")
print("AVG CALLS: {}".format(sum(map(int, Bf)) // len(Bf)))
print("AVG TIMES: {}".format(sum(map(float, Bt)) / len(Bt)))
# Dijkstra
print("D")
print("AVG CALLS: {}".format(sum(map(int, Df)) // len(Df)))
print("AVG TIMES: {}".format(sum(map(float, Dt)) / len(Dt)))

# RANDOM MAZES
for size in (32, 64, 128):
    At = []
    Af = []

    Aet = []
    Aef = []

    Act = []
    Acf = []

    Bt = []
    Bf = []

    Dt = []
    Df = []
    for i in range(120):
        # generate a random maze of size *size*
        case = mgen(size)
        p = cProfile
        #A* - manhattan
        p.run("A(case)", filename="statsfile")
        stream = StringIO()
        stats = pstats.Stats('statsfile', stream=stream)
        stats.print_stats()
        s = str(stream.getvalue()).split()

        Af.append(s[6])
        At.append(s[10])
        print("[*]A*M - {}/20 done. F: {} T: {}".format(i + 1, Af[-1], At[-1]))

        #A* - euclidean
        p.run("A(case, 1)", filename="statsfile")
        stream = StringIO()
        stats = pstats.Stats('statsfile', stream=stream)
        stats.print_stats()
        s = str(stream.getvalue()).split()

        Aef.append(s[6])
        Aet.append(s[10])
        print("[*]A*E - {}/20 done. F: {} T: {}".format(
            i + 1, Aef[-1], Aet[-1]))

        #A* - chebyshev
        p.run("A(case, 2)", filename="statsfile")
        stream = StringIO()
        stats = pstats.Stats('statsfile', stream=stream)
        stats.print_stats()
        s = str(stream.getvalue()).split()

        Acf.append(s[6])
        Act.append(s[10])
        print("[*]A*C - {}/20 done. F: {} T: {}".format(
            i + 1, Acf[-1], Act[-1]))

        # Bi-directional BFS
        p.run("B(case)", filename="statsfile")
        stream = StringIO()
        stats = pstats.Stats('statsfile', stream=stream)
        stats.print_stats()
        s = str(stream.getvalue()).split()

        Bf.append(s[6])
        Bt.append(s[10])
        print("[*]B - {}/20 done. F: {} T: {}".format(i + 1, Bf[-1], Bt[-1]))

        # Dijkstra
        p.run("D(case)", filename="statsfile")
        stream = StringIO()
        stats = pstats.Stats('statsfile', stream=stream)
        stats.print_stats()
        s = str(stream.getvalue()).split()

        Df.append(s[6])
        Dt.append(s[10])
        print("[*]D - {}/20 done. F: {} T: {}".format(i + 1, Df[-1], Dt[-1]))

    print("{}x{} MAZE".format(size, size))
    #A* - manhattan
    print("A*")
    print("AVG CALLS: {}".format(sum(map(int, Af)) // len(Af)))
    print("AVG TIMES: {}".format(sum(map(float, At)) / len(At)))
    #A* - euclidean
    print("A*E")
    print("AVG CALLS: {}".format(sum(map(int, Aef)) // len(Aef)))
    print("AVG TIMES: {}".format(sum(map(float, Aet)) / len(Aet)))
    #A* - chebyshev
    print("A*C")
    print("AVG CALLS: {}".format(sum(map(int, Acf)) // len(Acf)))
    print("AVG TIMES: {}".format(sum(map(float, Act)) / len(Act)))
    # Bi-dirBFS
    print("B")
    print("AVG CALLS: {}".format(sum(map(int, Bf)) // len(Bf)))
    print("AVG TIMES: {}".format(sum(map(float, Bt)) / len(Bt)))
    # Dijkstra
    print("D")
    print("AVG CALLS: {}".format(sum(map(int, Df)) // len(Df)))
    print("AVG TIMES: {}".format(sum(map(float, Dt)) / len(Dt)))
