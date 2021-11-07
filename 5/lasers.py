"""
Dodge the Lasers!
=================

Oh no! You've managed to escape Commander Lambda's collapsing space station in an escape pod with the rescued bunny workers - but Commander Lambda isnt about to let you get away that easily. Lambda sent an elite fighter pilot squadron after you -- and they've opened fire!

Fortunately, you know something important about the ships trying to shoot you down. Back when you were still Lambda's assistant, the Commander asked you to help program the aiming mechanisms for the starfighters. They undergo rigorous testing procedures, but you were still able to slip in a subtle bug. The software works as a time step simulation: if it is tracking a target that is accelerating away at 45 degrees, the software will consider the targets acceleration to be equal to the square root of 2, adding the calculated result to the targets end velocity at each timestep. However, thanks to your bug, instead of storing the result with proper precision, it will be truncated to an integer before adding the new velocity to your current position.  This means that instead of having your correct position, the targeting software will erringly report your position as sum(i=1..n, floor(i*sqrt(2))) - not far enough off to fail Commander Lambdas testing, but enough that it might just save your life.

If you can quickly calculate the target of the starfighters' laser beams to know how far off they'll be, you can trick them into shooting an asteroid, releasing dust, and concealing the rest of your escape.  Write a function solution(str_n) which, given the string representation of an integer n, returns the sum of (floor(1*sqrt(2)) + floor(2*sqrt(2)) + ... + floor(n*sqrt(2))) as a string. That is, for every number i in the range 1 to n, it adds up all of the integer portions of i*sqrt(2).

For example, if str_n was "5", the solution would be calculated as
floor(1*sqrt(2)) +
floor(2*sqrt(2)) +
floor(3*sqrt(2)) +
floor(4*sqrt(2)) +
floor(5*sqrt(2))
= 1+2+4+5+7 = 19
so the function would return "19".

str_n will be a positive integer between 1 and 10^100, inclusive. Since n can be very large (up to 101 digits!), using just sqrt(2) and a loop won't work. Sometimes, it's easier to take a step back and concentrate not on what you have in front of you, but on what you don't.


==================

1) Spaceships are shooting me
2) There is a bug on the software of the spaceshipts shooting me where they will compute my velocity wrong:
    v = sum(i=1..n, floor(i*sqrt(2)))
 *) solution(str_n: str(int) in [1, ... 10^100]) -> str(sum of (floor(1*sqrt(2)) + floor(2*sqrt(2)) + ... + floor(n*sqrt(2))))

sqrt(2) ~= 1.41

$$$$$$$

*) The sequence
If it was a rational number intead of sqrt(2) like '1.5':
N        1   2     3     4    5    6    7     8     9      10
x1.5    1.5  3.0  4.5   6.0  7.5  9.0  10.5  12.0  13.5   15.0
floor    1    3    4     6    7    9    10    12    13     15
SKIPPED    2         5          8          11          14
d = 3

For 1.4:
N        1    2    3     4    5     6    7     8      9      10    11    12
x1.4    1.4  2.8  4.2   5.6  7.0   8.4  9.8   11.2   12.6   14.0  15.4  16.8 
floor    1    2    4     5    7     8    9     11     12     14    15    16
SKIPPED         3           6               10           13                 17
d = 3, 4, 3, 4
1/.4 = 5/2 = 2.5    + 1 = 3.5

For 1.2:
N        1    2    3     4    5     6    7     8      9       10
x1.2    1.2  2.4  3.6   4.8  6.0   7.2  8.4   9.6    10.8    12.0
floor    1    2    3     4    6     7    8     9      10      12        ...17
SKIPPED                     5                             11
d = 6

There is a skip every time (1.5 - 1)*N > 1, in another words every time 0.5 * N % 1 == 0
So in every 2 there is a skip because 1/(1.5 -1) + 1 = 3

The sum would then be a AP (aritimetic progression) ranging from 1 to N, where N is the input on solution, subtracted by the AP sum with 3 ratio. Being q = 1.5 - 1
d = 1/q + 1
S = N * (N + 1) / 2  -  (1/q) * N ??????


So the question is, what is the expression and properties for the skipped numbers sequence


$$$$$$$





"""
from inspect import currentframe
from sys import stdout
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


##################################################


def gentable(N, f, silent=False):
    """N        1    2    3     4    5     6    7     8      9      10    11 12
    x1.4    1.4  2.8  4.2   5.6  7.0   8.4  9.8   11.2   12.6   14.0  15.4 16.8
    floor    1    2    4     5    7     8    9     11     12     14    15 16
    SKIPPED         3           6               10           13 17."""

    def write(*args):
        if silent:
            return
        s = " ".join([str(s) for s in args])
        stdout.write(s)

    def row(label, func, iter=None):
        write(label)
        if iter is None:
            iter = range(1, N + 1)
        for n in iter:
            func(n)
        write("\n")

    res = []

    def floor_r(n):
        r = int(n * f)
        res.append(r)
        return r

    row("N" + " " * 7, lambda n: write(" ", n, " " * 3))
    row("x" + "%.2f" % f + " " * 3, lambda n: write("%.2f" % (n * f) + " " * 3))
    row("floor  ", lambda n: write(" ", floor_r(n), " " * 3))
    skipped = [(str(r) if r not in res else "") for r in range(1, res[-1] + 1)]
    row("SKIPPED   ", lambda n: write(skipped[n], " " * 3), range(1, res[-1]))
    write("d = ", "%.4f" % (1 / (f - 1)))
    write("\n")

    skipped = [int(r) for r in skipped if r.strip()]
    d = sorted(list(set([n - p for p, n in zip(skipped[:-1], skipped[1:])])))
    return d, skipped


def dumb_solution(s):
    n = 2 ** 0.5
    sum = 0
    for i in range(int(s) + 1):
        x = int(i * n)
        sum += x
    return str(sum)


def dumb_solution2(s, acc=0, n=1):
    acc += int(2 ** 0.5 * n)
    if n == int(s):
        return str(acc)
    return dumb_solution2(s, acc, n + 1)


from decimal import Decimal


def asyntotic_extimative(s):
    n = int(s)
    s = int(round(n * (n + 1) * (2 ** 0.5) / 2.0 - n / 2.0))
    return s


#### REAL SOLUTION HERE

SQRT2_DIGITS = 4142135623730950488016887242096980785696718753769480731766797379907324784621070388503875343276415727


def sum_floors(n):
    # After recognizing this is a betty sequence called A001951, there is a way to compute its sum:
    # For n' = floor((sqrt(2) - 1)*n)
    # S(n) = nn' + n(n + 1)/2 - n'(n' + 1)/2 - S(n')
    if n == 0:
        return 0
    n_ = ((SQRT2_DIGITS) * n) // (10 ** 100)
    return n * n_ + n * (n + 1) / 2 - n_ * (n_ + 1) / 2 - sum_floors(n_)


def solution(s):
    return str(int(sum_floors(int(s))))


############################################################

if __name__ == "__main__":
    print(solution(5))
    debug()
    assert solution("5") == "19"
    debug()
    assert solution("77") == "4208"
    debug()
    assert solution("10000000") == "70710680189722"
    debug()
    assert solution("100000000") == "7071067832576153"
    debug()
    print(solution(10**100))
    debug()
