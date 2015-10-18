from constants import *
from graph import is_walkable, InvalidMap
from heapq import *
from math import hypot


class _Node(object):

    """This class works as the container of the nodes' info.
    Refer to the class AStar's documents for the meanings
    of g, h and f.
    """
    __slots__ = ['parent', 'status', 'f', 'g', 'h']

    def __init__(self):
        self.status = None
        self.parent = None
        self.g = None
        self.h = None
        self.f = None


class _QNode(object):

    """This class is used for storing the coordinates of the
    opened nodes in the open list. It provides a comparison
    method used by the priority queue.
    """
    __slots__ = ['pos', '_nodes']

    def __init__(self, pos, nodes):
        """Creates a new instance of QNode.
        :Parameters:
            pos : (x, y)
                the coordinate of this node.
            nodes: [str]
                a reference to AStar.nodes.
        """
        self.pos = pos
        self._nodes = nodes

    def __lt__(self, other):
        """Used by heapq for maintaining the priority queue.
        """
        x, y = self.pos
        ox, oy = other.pos
        if self._nodes[y][x].f == self._nodes[oy][ox].f:
            return self._nodes[y][x].h < self._nodes[oy][ox].h
        else:
            return self._nodes[y][x].f < self._nodes[oy][ox].f


class AStar(object):

    """Each node has three main properties:
        F, G and H
          where
            F = G + H
            G = the cost from source to this node
            H = estimated cost from this node to the destination.
    When we explore a node, we put all its adjacent nodes into a open
    list. At each loop, we take one node from the open list for next
    inspection. The node with smaller F will have higher priority.
    There are serveral ways to calculate the value of H:
        let x = horizontal distance between this node and destination
            y = vertical distance between this node and destination
        1. Manhattan: h = x + y
        2. Euclidean: h = hypot(x, y)
        3. Chebyshev: h = max(x, y)
        and so on.
        (Of course you can define your own heuristic methods.)
    also, you can give H a weight, i.e.
        F = G + W * H
    The higher the W value is, The more important the heuristic will
    be in this algorithm.
    """

    def __init__(self, raw_graph, heuristic=MANHATTAN):
        """Create a new instance of A* path finder.

        :Parameters:
            raw_graph : str
                A multi-line string representing the graph.
                example:
                s = '''
                    S000
                    1110
                    T000
                    '''
            heuristic :
                Currently three types of heuristic are supported,
                namely MANHATTAN, EUCLIDEAN and CHEBYSHEV
        """
        self.graph = raw_graph.split()
        self.size = len(self.graph)

        # determine heuristic function
        self.h_list = {MANHATTAN: self._manhattan,
                       EUCLIDEAN: self._euclidean,
                       CHEBYSHEV: self._chebyshev}
        if heuristic not in self.h_list:
            self.heuristic = MANHATTAN
        else:
            self.heuristic = heuristic
        self.h_func = self.h_list[self.heuristic]

        self.source = None
        self.target = None
        self.path = []

        # 2D array of nodes
        self.nodes = [[_Node()
                       for x in range(self.size)]
                      for y in range(self.size)]

        # get source and target coordinates
        for y in range(self.size):
            for x in range(self.size):
                if self.graph[y][x] == SOURCE:
                    self.source = (x, y)
                elif self.graph[y][x] == TARGET:
                    self.target = (x, y)

        # guarantee that both source and target is present on the graph
        if not all((self.source, self.target)):
            raise InvalidMap("No source or target given")

        # a priority queue holding the coordinates waiting
        # for inspection
        self.open_list = []

    def step(self, record=None):
        """Starts the computation of the shortest path.
        *Note* :
            This function works as a generator, a yield statement
            is appended at the bottom of each loop to make this
            function capable of being executed step by step.

            If you does not want the step feature, simply delete
            the yield statements.

        :Parameters:
            record : deque or list
                if a queue is specified, a record of each operation
                (OPEN, CLOSE, etc) will be pushed into the queue.
        """
        # add the source node into the open list
        sx, sy = self.source
        self.nodes[sy][sx].g = 0
        self.nodes[sy][sx].f = 0
        self.open_list.append(_QNode(self.source, self.nodes))
        self.nodes[sy][sx].status = OPENED

        # while the open list is not empty
        while self.open_list:

            # get the node with lowest F from the heap
            x, y = heappop(self.open_list).pos
            self.nodes[y][x].status = CLOSED
            if record is not None:
                record.append(('CLOSE', (x, y)))

            # if the node is the target, reconstruct the path
            # and break the loop
            if (x, y) == self.target:
                self._retrace()
                break

            # inspect the horizontal and vertical adjacent nodes
            for i in range(len(XOFFSET)):

                # next x and y
                nx = x + XOFFSET[i]
                ny = y + YOFFSET[i]

                # if the next coordinate is walkable, inspect it.
                if is_walkable(nx, ny, self.size, self.graph):
                    self._inspect_node((nx, ny), (x, y), False, record)

                    # further investigate the diagonal nodes
                    nx1 = x + DAXOFFSET[i]
                    ny1 = y + DAYOFFSET[i]
                    nx2 = x + DBXOFFSET[i]
                    ny2 = y + DBYOFFSET[i]
                    npos = ((nx1, ny1), (nx2, ny2))
                    for nx, ny in npos:
                        if is_walkable(nx, ny, self.size, self.graph):
                            self._inspect_node((nx, ny), (x, y),
                                               True, record)
            yield

    def _retrace(self):
        """After the search completes, this method will be called to
        reconstruct the path according to the nodes' parents.
        """
        self.path = [self.target]
        while self.path[-1] != self.source:
            x, y = self.path[-1]
            self.path.append(self.nodes[y][x].parent)
        self.path.reverse()

    def _inspect_node(self, node_pos, parent_pos, diagonal, record):
        """Push the node into the open list if this node is not
        in the open list. Otherwise, if the node can be accessed
        with a lower cost from the given parent position, update
        its parent and cost, then heapify the open list.
        """
        x, y = node_pos
        px, py = parent_pos

        if self.nodes[y][x].status != CLOSED:
            if self.nodes[y][x].status != OPENED:
                self.nodes[y][x].status = OPENED
                if record is not None:
                    record.append(('OPEN', (x, y)))
                self._try_update((x, y), (px, py), diagonal, record)
                heappush(self.open_list,
                         _QNode((x, y), self.nodes))
            else:
                if self._try_update((x, y), (px, py), diagonal,
                                    record):
                    heapify(self.open_list)

    def _try_update(self, node_pos, parent_pos, diagonal, record):
        """Try to update the node's info with the given parent.
        If this node can be accessed with the given parent with lower
        G cost, this node's parent, G and F values will be updated.
        :Return:
            updated : bool
                whether this node's info has been updated.
        """
        x, y = node_pos
        px, py = parent_pos
        dd = DDIST if diagonal else DIST  # whether is diagonal
        ng = self.nodes[py][px].g + dd  # next G value
        node = self.nodes[y][x]

        if node.g is None or ng < node.g:
            # if this node has not been opened or
            # it can be accessed with lower cost
            node.parent = (px, py)
            node.g = ng
            node.h = self._calc_h((x, y))
            node.f = node.g + node.h

            if record is not None:
                record.append(('VALUE', ('g', (x, y), node.g)))
                record.append(('VALUE', ('h', (x, y), node.h)))
                record.append(('VALUE', ('f', (x, y), node.f)))
                record.append(('PARENT', ((x, y), (px, py))))
            return True
        return False

    def _calc_h(self, pos):
        """Caculate the H value of the node.
        """
        dx = abs(pos[0] - self.target[0])
        dy = abs(pos[1] - self.target[1])
        return self.h_func(dx, dy)

    def _manhattan(self, dx, dy):
        return (dx + dy) * SCALE

    def _euclidean(self, dx, dy):
        return int(hypot(dx, dy) * SCALE)

    def _chebyshev(self, dx, dy):
        return max(dx, dy) * SCALE
