from constants import *
from graph import make_graph
from heapq import *


class Dijkstra(object):

    """This class is designed for solving general graphs without
    negative weighted edges, not limited to grid maps.
    """

    def __init__(self, graph, source, target):
        """Create a new instance of Dijkstra path finder.

        :Parameters:
            graph : {nodeid1: {nodeid2: dist, ... }, ... }
                The graph is in adjacency list representation.
                The nodeid can be any hashable object.
                Sample graphs are as follows:
                    graph = {(1, 2): {(2, 2): 1, (1, 3): 1},
                             (2, 2): {(1, 2): 1},
                             (1, 3): {(1, 2): 1}}
                or
                    graph = {'A': {'B': 1, 'C': 1},
                             'B': {'A': 1},
                             'C': {'A': 1}}

            source : nodeid
                Source coordinate.

            target : nodeid
                Destination coordinate.
        """
        self.graph = graph
        self.source = source
        self.target = target
        self.path = []

        # record of each node's parent
        self.parent = {}

        # record of each node's estimate distance
        self.dist = dict([(pos, INF) for pos in graph])

        # set of open nodes
        self.nodes = set([pos for pos in graph])

    def step(self, record=None):
        """Starts the computation of shortest path.
        :Parameters:
            record : deque
                if a queue is specified, a record of each operation
                (OPEN, CLOSE, etc) will be pushed into the queue.
        """
        self.dist[self.source] = 0
        while self.dist:
            # get the node with minimum estimated distance
            node = min(self.nodes, key=self.dist.__getitem__)
            self.nodes.remove(node)

            if record is not None:
                record.append(('CLOSE', node))

            # if the node with minimum estimated distance has the
            # distance of infinity, then there is no such path from
            # source to distance.
            if self.dist[node] == INF:
                break

            # if the node is the target, then the path exists.
            if node == self.target:
                self._retrace()
                break

            # inspect the adjacent nodes.
            for adj in self.graph[node]:
                if adj in self.nodes:
                    self._relax(node, adj, record)
                    if record is not None:
                        record.append(('OPEN', adj))
            yield
        yield

    def _relax(self, u, v, record_):
        """Relax an edge.
        :Parameters:
            u : nodeid
                Node u
            v : nodeid
                Node v
        :Return:
            suc : bool
                whether the node v can be accessed with a lower
                cost from u.
        """
        d = self.dist[u] + self.graph[u][v]
        if d < self.dist[v]:
            self.dist[v] = d
            self.parent[v] = u
            if record_ is not None:
                record_.append(('VALUE', ('f', v, d)))
                record_.append(('PARENT', (v, u)))
            return True
        return False

    def _retrace(self):
        """This method will reconstruct the path according to the
        nodes' parents.
        """
        self.path = [self.target]
        while self.path[-1] != self.source:
            self.path.append(self.parent[self.path[-1]])
        self.path.reverse()


class GridDijkstra(Dijkstra):

    """This class is specified to grid maps.

    *Note*: On grid maps with all horizontal and vertical weights
    set to be 10 and all diagonal weights set to be 14, like
    we presumed in this scenario, Dijkstra's algorithm explores
    nodes in exactly the same way as a generic Breadth-First-Search
    algorithm.
    """

    def __init__(self, raw_graph):
        g, s, t = make_graph(raw_graph)
        Dijkstra.__init__(self, g, s, t)
