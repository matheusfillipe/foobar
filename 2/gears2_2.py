# https://i.imgur.com/lVaAFYT.jpg
"""The engineers have plenty of gears in all different sizes stocked up, so you
can choose gears of any size, from a radius of 1 on up. Your goal is to build a
system where the last gear rotates at twice the rate (in revolutions per
minute, or rpm) of the first gear, no matter the direction. Each gear (except
the last) touches and turns the gear on the next peg to the right.

Given a list of distinct positive integers named pegs representing the location of each peg along the support beam, write a function solution(pegs) which, if there is a solution, returns a list of two positive integers a and b representing the numerator and denominator of the first gear's radius in its simplest form in order to achieve the goal above, such that radius = a/b. The ratio a/b should be greater than or equal to 1. Not all support configurations will necessarily be capable of creating the proper rotation ratio, so if the task is impossible, the function solution(pegs) should return the list [-1, -1].

For example, if the pegs are placed at [4, 30, 50], then the first gear could have a radius of 12, the second gear could have a radius of 14, and the last one a radius of 6. Thus, the last gear would rotate twice as fast as the first one. In this case, pegs would be [4, 30, 50] and solution(pegs) should return [12, 1].

The list pegs will be given sorted in ascending order and will contain at least 2 and no more than 20 distinct positive integers, all between 1 and 10000 inclusive.

26 20
-6  = 0.5

############

----p1---------p2------------------------p3-------------

pegs list in N+ --> positions along the beam | sorted ascending | 2 <= len(pegs) <= 20 | 1 <= elm <= 1000

goal: last has to rotate twice as fast as first
things: [a, b] with a/b > 1, a,b in N+, r1 = a/b   impossible = [-1, -1]

pegs --> R0 --> a/b
$

V0 = 1
goal: V_{len(pegs)} = 2*V0
Vn = V_{n-1} R_n/R_{n-1}
Vl = R_0/R_l = 2   --> (telescopic multiplication aka obvious) All we need is the last to be half the radius of the first

Rl = R0/2
$

Rn + R_{n-1} = Pn - P_{n-1}

R0 + R1 = P1 - P0 --> R0 = P1 - P0 - R1      with R1 as a parameter
Rl + R_{l-1} = Pl - P_{l-1}
R0/2 + R_{l-1} = Pl - P_{l-1}
R0/2 = Pl - P_{l-1} - R_{l-1}
R0 = (Pl - P_{l-1} - R_{l-1}) * 2           wirh R_{l-1} as parameter

R0 = (Pl - P_{l-1} - R_{l-1}) * 2 = P1 - P0 - R1
$
R's can be rational numbers

db = R0 + R1
de = R-1 + R-2
de = R0/2 + R-2 -->  recursive must fit

db - de = R0/2 + R1 - R-2
R0 + R-1 + 2*(R1+R2+...R-2) = Pl-P0
Rn = Pn - P_{n-1} - R_{n-1}
Rn =    Dn - R_{n-1}
Rn > 1 !!!

if two pegs are spaced by 1 then [-1, -1]
odd numer of pegs --> r_0 -- R-1
if even inversely

1 7
4 2
R1 = D1 - R0
R2 = D2 - R1 = D2 - D1 + R0
R3 = D3 - R2 = D3 - D2 + D1 - R0
Rn = Dn - Dn-1 + Dn-2 - Dn-3 .... R0   --> - if n%2!=0 else +

R0/2 = Dn - Dn-1 + Dn-2 - Dn-3 .... R0   --> - if n%2!=0 else +


###########
"""


MINIMUM_GEAR_RADIUS = 1


def solution(pegs):
    # All we need is the radius of the last gear to be half the radius of the first
    # If Dn is the distance between the peg n and n-1 and Rn the gear radius at peg n,
    # with a bit of math manipulations we have: Rn = Dn - Dn-1 + Dn-2 - Dn-3 .... R0
    # Thus: R0/2 + (+R0 if n%2 == 0 else -R0) = Dn - Dn-1 + Dn-2.... D1a    where n here is len(pegs)

    distances = [pegs[n + 1] - pegs[n] for n in range(len(pegs) - 1)]
    is_even = len(pegs) % 2 == 0

    sign = 1
    sum_of_differences = 0
    for d in distances[::-1]:
        sum_of_differences += sign * d
        sign *= -1

    r0 = sum_of_differences / (1.5 if is_even else -0.5)

    # We must still confirm the radius for all gears to validate the result
    rn = r0
    for d in [2 * r0] + distances:
        rn = d - rn
        if rn < MINIMUM_GEAR_RADIUS:
            return [-1, -1]

    # The only possible denominator is 3 in the case len(pegs) is an even number (sum_of_differences
    # is a positive number and will be multiplied by 2/3)
    if is_even:
        return [int(r0), 1] if r0.is_integer() else [sum_of_differences * 2, 3]
    else:
        return [int(r0), 1]


if __name__ == "__main__":
    assert solution([4, 30, 50]) == [12, 1]
    assert solution([4, 17, 50]) == [-1, 1]
    assert solution([4, 17, 50]) == [-1, -1]
