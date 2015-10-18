from astar import AStar
from random import random, randint, seed

seed()


def solveable(m):
    def A(m, h=0):
        a = AStar(m, h)
        for i in a.step():
            pass
        return None if not a.path else True
    return A(m)


def mgen(size):
    """Generates a random square-sized maze of size *size*."""
    maze = [["0" for i in range(size)] for i in range(size)]

    for i in range(size):
        for j in range(size):
            # each field has a 20% change of being an obstacle
            if random() <= 0.2:
                maze[i][j] = "1"

    while 1:
        # generate source
        a, b = randint(0, size - 1), randint(0, size - 1)
        # if the current tile is blocked
        while(maze[a][b] == '1'):
            a, b = randint(0, size - 1), randint(0, size - 1)
        maze[a][b] = 'S'

        # generate target
        a, b = randint(0, size - 1), randint(0, size - 1)
        # if the current tile is either blocked or start node
        while(maze[a][b] in ("1", "S")):
            a, b = randint(0, size - 1), randint(0, size - 1)
        maze[a][b] = 'T'

        break

    # put the maze back together
    maze = "".join("".join(maze[i]) + "\n" for i in range(size))

    return maze if solveable(maze) else mgen(size)

print(mgen(32))
