# Comparing the efficiency of different path-finding algorithms to find the shortest path in a square-shaped maze

was the topic of my high-school "research" essay, done as a part of IB Diploma Programme.

I implemented the following path-finding algorithms: (original author Xueqiao Xu, I optimized the code and made it compatible with Python 3.x.
* A* (with all heuristic functions, Manhattan, Euclidean and Chebyshev)
* Bi-directional Breadth First Search (BFS)
* Dijkstra's algorithm.

As a dataset, I used both Nathan Sturtevant's [set of maps](www.movingai.com/benchmarks/) and randomly generated maps with 20% change of a tile being an obstacle. (based on personal communication with David Silver & Dr. Richard Korf, both haing written a paper on Cooperative Pathfinding.)

The code is structured followingly:
##### Pathfinding Logic
`astar.py`
`bidirbfs.py`
`constants.py`
`dijkstra.py`

##### Random Maze Generator
`mazegen.py`

##### Testing code
`ee.py`
`mapparser.py`

A* was the best path-finding algorithm on both testing sets, which is due to its intelligent heuristic, which ensures that the algorithm is going as much towards target as possible.

I got 36 points out of 36, which is A - highest markcount and grade possible. I am willing to provide a copy of my extended essay upon request.
