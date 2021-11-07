"""Unfortunately (again), you can't just remove all obstacles between the bunnies and the escape pods - at most you can remove one wall per escape pod path, both to maintain structural integrity of the station and to avoid arousing Commander Lambda's suspicions. 

You have maps of parts of the space station, each starting at a work area exit and ending at the door to an escape pod. The map is represented as a matrix of 0s and 1s, where 0s are passable space and 1s are impassable walls. The door out of the station is at the top left (0,0) and the door into an escape pod is at the bottom right (w-1,h-1). 

Write a function solution(map) that generates the length of the shortest path from the station door to the escape pod, where you are allowed to remove one wall as part of your remodeling plans. The path length is the total number of nodes you pass through, counting both the entrance and exit nodes. The starting and ending positions are always passable (0). The map will always be solvable, though you may or may not need to remove a wall. The height and width of the map can be from 2 to 20. Moves can only be made in cardinal directions; no diagonal moves are allowed.

################################################################################

these are always 0:
    start -- 0, 0
    end -- w-1, h-1

map:
    1 -- wall
    0 -- passage
    w, h from 2 to 20

solution := map --> count of shortest path inclusive given that one wall can be removed 
moves are always (+1, 0), (0, +1) (-1, 0) (0, -1) for map[i][j] 

* you may or may not remove a wall to find the shortest path
* it may be needed to remove a wall for map to be solvable

[
    [0, 1, 1, 0],
    [0, 0, 0, 1],
    [1, 1, 0, 0],
    [1, 1, 1, 0]
]
7

[
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0],
]
11

- How to find the shortest path?
- How do i know if i need to remove a wall or not?
- What is the best way to represent this graph?

* It is not worth to remove 1 if it doesn't shorten anything

1) dumb solution: Random design
Run a path finding algorithm (BSF, disjstra, A*) counting the number of steps. For each 1 in the map remove it and releat the path finding. Return the smaller count (min)

"""

T = [[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]]
T1 = [
    [0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0],
]
T2 = [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0],
]
T3 = [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0],
]
T4 = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 0],
    [1, 1, 1, 1, 0, 0, 1, 1],
    [0, 1, 0, 0, 0, 1, 1, 1],
    [0, 1, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1],
    [0, 1, 1, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

TT = [
    [0, 1, 1, 1, 0],
    [0, 1, 1, 0, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
]

T8 = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 1, 0],
    [1, 1, 1, 1, 1, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 1, 1],
    [1, 1, 0, 1, 1, 0, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

T5 = [
    [0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1],
    [0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]

T6 = [
    [0, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0],
    [0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1],
    [0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [0, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1],
    [0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
]


from copy import deepcopy
from inspect import currentframe
from pprint import pprint
from time import time


def now():
    return time() * 1000


last_milis = now()


def debug():
    global last_milis
    tnow = now()
    cf = currentframe()
    print(">>>>%d %f" % (cf.f_back.f_lineno, tnow - last_milis))
    last_milis = now()


def manhattan_distance(p1, p2):
    """Manhattan distance heuristic."""
    # return 0
    return abs(p2[0] - p1[0] + p2[1] - p1[1])


def print_path(grid, came_from, current, attempt_step_count):
    m = deepcopy(grid)
    x = deepcopy(grid)
    n = 8
    m[current[0]][current[1]] = n
    while current != (0, 0):
        current = came_from[current]
        m[current[0]][current[1]] = n
        x[current[0]][current[1]] = attempt_step_count[current]
    pprint(m)
    pprint(x)


def transverse_count(came_from, end):
    count = 0
    current = end
    while current != (0, 0):
        current = came_from[current]
        count += 1
    return count


################################################################################


VALID_MOVES = [(0, -1), (-1, 0), (1, 0), (0, 1)]


def get_neighbors(grid, spot, return_shortcuts=False):
    """Returns a list of spots that are neighbors of spot.

    Spots are a tuple like (row, column) where row and column are
    indexes of the grid matrix.
    """
    neighbors = []
    for move in VALID_MOVES:
        row = spot[0] + move[0]
        column = spot[1] + move[1]
        if 0 <= row < len(grid) and 0 <= column < len(grid[0]):
            if not grid[row][column]:
                neighbors.append((row, column))
            # Only consider removing a wall if it will connect two passages
            elif return_shortcuts and len(get_neighbors(grid, (row, column))) >= 2:
                neighbors.append((row, column))

    return neighbors


def last_wall(grid, came_from, spot):
    while spot != (0, 0):
        if grid[spot[0]][spot[1]]:
            return spot
        spot = came_from[spot]


def find_shortest_path(grid):
    """Slightly modified implementation of dijkstra's path finding.

    Will Return the step count for the shortest path on the grid.
    """
    n_cols = len(grid[0])
    n_rows = len(grid)
    start = (0, 0)
    end = (n_rows - 1, n_cols - 1)
    shortcut = False
    unexplored = [start]
    step_count_dict = {
        (r, c): float("inf") for r in range(n_rows) for c in range(n_cols)
    }
    came_from = {}
    wall_blacklist = []
    wall_sequence = []
    step_count_dict[start] = 1

    # This has better performance than .append followed by sort
    # The idea is to keep the queue of spots with the smaller step count on the end of the unexplored list
    def sorted_put(neighbor):
        for i, spot in enumerate(unexplored):
            if attempt_step_count >= step_count_dict[spot]:
                unexplored.insert(i, neighbor)
                break
        else:
            unexplored.append(neighbor)

    while len(unexplored) != 0:
        current = unexplored.pop()
        shortcut = last_wall(grid, came_from, current)
        if current == end:
            # print_path(grid, came_from, current)
            return transverse_count(came_from, end) + 1
            # return step_count_dict[current]

        attempt_step_count = step_count_dict[current] + 1
        neighbors = get_neighbors(grid, current, not shortcut)
        # print(f"{neighbors=}")
        for neighbor in neighbors:
            if neighbor in wall_blacklist:
                continue
            # TODO after the  blacklisting on the if below the values are set and this comparison always fails
            # No new nieghbots are accepted
            # Even if it was not on the current_path transverse, it might have already been explored
            # print(f"{attempt_step_count} < {step_count_dict[neighbor]}")
            if attempt_step_count < step_count_dict[neighbor]:
                # print(f"Adding {neighbor=}")
                if shortcut:
                    wall_sequence.append(neighbor)
                # if grid[neighbor[0]][neighbor[1]]:
                # print(f"Took shortcut for {current} at [{neighbor[0]}][{neighbor[1]}]")
                came_from[neighbor] = current
                step_count_dict[neighbor] = attempt_step_count
                sorted_put(neighbor)

        if len(unexplored) == 0 and shortcut:
            # print(f"!!!!!!! blacklist {shortcut}")
            wall_blacklist.append(shortcut)
            back_to = came_from[shortcut]
            unexplored.append(back_to)
            for spot in wall_sequence:
                step_count_dict[spot] = float("inf")
                spot = came_from[spot]
            wall_sequence = []
            # print(f"back to {unexplored[-1]}")

    # TODO return None instead
    # print_path(grid, came_from, current, step_count_dict)
    return came_from


def solution(map):
    if len(map) <= 4 and len(map[0]) <= 4:
        return len(map) + len(map[0]) - 1
    return find_shortest_path(map)


############################################################
###### SOLUTION STARTS HERE

VALID_MOVES = [(0, -1), (-1, 0), (1, 0), (0, 1)]


def count_steps(grid, start):
    """Counts inclusively the shortest path number of steps get get at reach
    cell of grid.

    :param grid: The matrix repesentation of the grid of spaces and and walls
    :param start: Tuple (x, y) representing the start position to count from
    :returns: A matrix of ints with the same size as grid
    """
    unexplored = [start]
    board = [[float("inf") for i in range(len(grid[0]))] for i in range(len(grid))]
    board[start[0]][start[1]] = 1

    def neighbors(x, y):
        for move in VALID_MOVES:
            row = x + move[0]
            column = y + move[1]
            if 0 <= row < len(grid) and 0 <= column < len(grid[0]):
                yield (row, column)

    # Basically dijkstra
    while unexplored:
        x, y = unexplored.pop(0)
        for nx, ny in neighbors(x, y):
            n_steps = board[x][y] + 1
            if board[nx][ny] > n_steps:
                # Count the wall but dot not visit its neighbors
                board[nx][ny] = n_steps
                if grid[nx][ny] == 1:
                    continue
                unexplored.append((nx, ny))

    return board


def solution(m):
    height = len(m)
    width = len(m[0])
    shortest = width + height - 1

    # If both dimensions are at maximum 4 the shortest path will be the manhattan distance
    if width <= 4 and height <= 4:
        return shortest

    paths = count_steps(m, (0, 0))
    reverse_paths = count_steps(m, (height - 1, width - 1))

    return min(
        [
            # Wherever both paths meet with the minimum ammount of steps
            paths[i][j] + reverse_paths[i][j] - 1
            for j in range(width)
            for i in range(height)
        ]
    )


if __name__ == "__main__":
    debug()
    assert solution([[0, 1, 1, 0], [0, 0, 0, 1], [1, 1, 0, 0], [1, 1, 1, 0]]) == 7
    debug()
    assert (
        solution(
            [
                [0, 0, 0, 0, 0, 0],
                [1, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0],
            ]
        )
        == 11
    )
    debug()
    assert (
        solution(
            [
                [0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0],
            ]
        )
    ) == 11
    debug()
    assert (
        solution(
            [
                [0, 0, 0, 0, 0, 0],
                [0, 1, 1, 1, 1, 0],
                [1, 1, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 1],
                [0, 1, 1, 1, 1, 1],
                [0, 0, 0, 0, 0, 0],
            ]
        )
    ) == 11
    debug()
    assert (solution(T4)) == 19
    debug()
    assert (solution(T6)) == 38
    debug()
    assert (solution(T5)) == 52
    debug()
