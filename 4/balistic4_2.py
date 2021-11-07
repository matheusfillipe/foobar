"""
Uh-oh -- you've been cornered by one of Commander Lambdas elite bunny trainers! Fortunately, you grabbed a beam weapon from an abandoned storeroom while you were running through the station, so you have a chance to fight your way out. But the beam weapon is potentially dangerous to you as well as to the bunny trainers: its beams reflect off walls, meaning you'll have to be very careful where you shoot to avoid bouncing a shot toward yourself!

Luckily, the beams can only travel a certain maximum distance before becoming too weak to cause damage. You also know that if a beam hits a corner, it will bounce back in exactly the same direction. And of course, if the beam hits either you or the bunny trainer, it will stop immediately (albeit painfully). 

Write a function solution(dimensions, your_position, trainer_position, distance) that gives an array of 2 integers of the width and height of the room, an array of 2 integers of your x and y coordinates in the room, an array of 2 integers of the trainer's x and y coordinates in the room, and returns an integer of the number of distinct directions that you can fire to hit the elite trainer, given the maximum distance that the beam can travel.

The room has integer dimensions [1 < x_dim <= 1250, 1 < y_dim <= 1250]. You and the elite trainer are both positioned on the integer lattice at different distinct positions (x, y) inside the room such that [0 < x < x_dim, 0 < y < y_dim]. Finally, the maximum distance that the beam can travel before becoming harmless will be given as an integer 1 < distance <= 10000.

For example, if you and the elite trainer were positioned in a room with dimensions [3, 2], your_position [1, 1], trainer_position [2, 1], and a maximum shot distance of 4, you could shoot in seven different directions to hit the elite trainer (given as vector bearings from your location): [1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3, 2], and [-3, -2]. As specific examples, the shot at bearing [1, 0] is the straight line horizontal shot of distance 1, the shot at bearing [-3, -2] bounces off the left wall and then the bottom wall before hitting the elite trainer with a total shot distance of sqrt(13), and the shot at bearing [1, 2] bounces off just the top wall before hitting the elite trainer with a total shot distance of sqrt(5).


#########

1) do not shoot yourself by Hitting corners
2) Beans stop after hitting a target
* GOAL: solution(dimensions:[1 < x_dim <= 1250, 1 < y_dim <= 1250], your_position: [0 < x < x_dim, 0 < y < y_dim], trainer_position: [0 < x < x_dim, 0 < y < y_dim], distance: int 1 < distance <= 10000) -> Number of directions (count) that you can hit the trainer (distance is bullet reach)
* e.g
 - - - 
|     |
|* X  |
 - - - 
distance = 4
Bearings: [1, 0], [1, 2], [1, -2], [3, 2], [3, -2], [-3, 2], and [-3, -2]

$$$$$$$$$$$$$$$$$$$$$$$$

Dx = 2w
Dy = 2h
all combinations 
x + Dx, y + Dy

"""

import sys
from inspect import currentframe
from time import time


def now():
    return time() * 1000


last_milis = now()


def debug(msg=""):
    global last_milis
    tnow = now()
    cf = currentframe()
    print(">>>> %d %s %f" % (cf.f_back.f_lineno, msg, tnow - last_milis))
    last_milis = now()


def colinear_in_order(p1, p2, p3):
    """Checks if 3 points are colinear and come in the given order."""
    tri_area = (
        p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1])
    )
    if tri_area == 0:
        d = distance2(p1, p3)
        return d > distance2(p1, p2) and d > distance2(p2, p3)


def any_colinear(p1, points, p2):
    for p in points:
        if (
            tuple(p1) != tuple(p)
            and tuple(p1) != tuple(p2)
            and colinear_in_order(p1, p, p2)
        ):
            return True


def bearing(p1, p2):
    d = distance2(p1, p2) ** 0.5
    return ((p2[0] - p1[0]) / d, (p2[1] - p1[1]) / d)


###### SOLUTION STARTS HERE

from math import atan2


def angle(p1, p2):
    """Returns the horizontal angle in radians of the line starting from p1 to
    p2."""
    return atan2(p2[1] - p1[1], p2[0] - p1[0])


def distance2(p1, p2):
    """Returns the squared euclidean distance between two points."""
    return (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2


def generate_mirrored_points(rooms_x, rooms_y, dx, dy, points):
    """Generates the coordinates of points in different rooms."""
    signs = [[1, 1], [-1, 1], [1, -1], [-1, -1]]
    for nx in range(-rooms_x, rooms_x + 1):
        for ny in range(-rooms_y, rooms_y + 1):
            for sx, sy in signs:
                yield [[sx * x + nx * dx, sy * y + ny * dy] for x, y in points]


def hit_angles(dimensions, origin, target, max_distance):
    """Returns a dictionary with float angle values as keys and a list like [x,
    y, distance] as values for all mirrored rooms within the radius of
    max_distance."""
    w, h = dimensions
    dx, dy = 2 * w, 2 * h
    rooms_x = max_distance // w
    rooms_y = max_distance // h
    my_reflections, target_reflections = {}, {}

    def add_point(point, _dict):
        """Adds point to _dict if it is the closest point on that direction."""
        d = distance2(origin, point)
        a = angle(origin, point)
        if d > max_distance ** 2:
            return
        if d == 0 or a in _dict and _dict[a][-1] < d:
            return
        _dict[a] = point + [d]

    for m_origin, m_target in generate_mirrored_points(
        rooms_x, rooms_y, dx, dy, [origin, target]
    ):
        add_point(m_origin, my_reflections)
        add_point(m_target, target_reflections)

    return target_reflections, my_reflections


def solution(dimensions, me, target, max_distance):
    # Compute directions and distances for all targets and my reflections
    target_reflections, my_reflections = hit_angles(
        dimensions, me, target, max_distance
    )

    # Count all directions filtering those behind my own reflections
    return sum(
        (
            1
            for t_angle in target_reflections
            if not (
                t_angle in my_reflections
                and my_reflections[t_angle][-1] < target_reflections[t_angle][-1]
            )
        )
    )


def main():
    debug()
    assert solution([3, 2], [1, 1], [2, 1], 1) == 1
    debug()
    assert solution([3, 2], [1, 1], [2, 1], 4) == 7
    debug()
    assert solution([300, 275], [150, 150], [185, 100], 10) == 0
    debug()
    assert solution([300, 275], [150, 150], [185, 100], 500) == 9
    debug()
    assert solution([500, 250], [150, 150], [185, 100], 2000) == 99
    debug()
    assert solution([1250, 1250], [1000, 1000], [500, 400], 10000) == 196
    debug()
    assert solution((15, 6), (7, 5), (13, 1), 1404) == 60595
    debug()

    import cProfile
    cProfile.run("solution((15, 6), (7, 5), (13, 1), 1404)")


if __name__ == "__main__":
    main()
