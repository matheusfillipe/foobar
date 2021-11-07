"""You will set up simultaneous thumb wrestling matches. In each match, two
trainers will pair off to thumb wrestle. The trainer with fewer bananas will
bet all their bananas, and the other trainer will match the bet. The winner
will receive all of the bet bananas. You don't pair off trainers with the same
number of bananas (you will see why, shortly). You know enough trainer
psychology to know that the one who has more bananas always gets over-confident
and loses. Once a match begins, the pair of trainers will continue to thumb
wrestle and exchange bananas, until both of them have the same number of
bananas. Once that happens, both of them will lose interest and go back to
supervising the bunny workers, and you don't want THAT to happen!

For example, if the two trainers that were paired started with 3 and 5 bananas, after the first round of thumb wrestling they will have 6 and 2 (the one with 3 bananas wins and gets 3 bananas from the loser). After the second round, they will have 4 and 4 (the one with 6 bananas loses 2 bananas). At that point they stop and get back to training bunnies.

How is all this useful to distract the bunny trainers? Notice that if the trainers had started with 1 and 4 bananas, then they keep thumb wrestling! 1, 4 -> 2, 3 -> 4, 1 -> 3, 2 -> 1, 4 and so on.

Now your plan is clear. You must pair up the trainers in such a way that the maximum number of trainers go into an infinite thumb wrestling loop!

Write a function solution(banana_list) which, given a list of positive integers depicting the amount of bananas the each trainer starts with, returns the fewest possible number of bunny trainers that will be left to watch the workers. Element i of the list will be the number of bananas that trainer i (counting from 0) starts with.

The number of trainers will be at least 1 and not more than 100, and the number of bananas each trainer starts with will be a positive integer no more than 1073741823 (i.e. 2^30 -1). Some of them stockpile a LOT of bananas.


#######

pair them in the way the maximum is stuck on infinite loops

task: pair them in infinite loops
return: total - number of trainers stuck in infinite loops
goal: Number of games that will end * 2

1 - 1 ---> end --> 2 gone

1 - 7 -> 2 - 6 -> 4 - 4 x

1 - 3 -> 2 - 2 x

3 - 7 -> 6, 4 -> 2, 8 -> 4, 6 -> 8, 2 !!!!

match(a, b) for a < b :--> 2a, b - a


itertools --> all possible pairs ---> max ---> recursive func using match above --> identify loop


$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$

a + b = constant
a, b -> 2a, b - a = b, a => b = 2a

loops happen from b = (2*n) * a   for any interger n > 0



A B C D  --> AB CD, AC BD, AD BC
A B C D E F --> AB CD EF, AC DB EF, AD BC EF, AE



# Numbers you cant couple (a, b)
#


a = 1 --> 2*n + 1 starting with n==0  or 2**n - 1 starting with n = 1
a = 2 --> 2**n - 2
a = 3 --> 2**n - 3 no ---
1 3 5 9 13 21 29 45 61 93 125 189 253 381 509 765
 2 2 4 4  8  8  16 16 32 32 .... 2**n
  0 2 0 4  0  8  0  16 0 32 0 ... 2**n
   2 -2 4 -4 8 -8 16 -16 ... 2**n -2**n
    -4 6 -8 12 -16 24 -32 ...
b_n = 1/2 (2^(n/2 + 3/2) + (-1)^(n + 1) 2^(n/2 + 3/2) + 3 2^(n/2) + 3 (-1)^n 2^(n/2) - 6) (for all terms given)

a = 4 --> lambda z: (5 + 6 * z - 6 * z^2)/(1 - z - 2 z^2 + 2 * z^3)

* If the a number is a potency of 2 then all endable games b with it are on the form b = 2**n - a
1, 2, 4, 8, 16 ...
* If the number is not a potency of 2, b = 2**n - a is endable but there are more endable games

can't couple a, b if
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
    print(">>>>%d %s %f" % (cf.f_back.f_lineno, msg, tnow - last_milis))
    last_milis = now()


def f_game_ends(a, b, last=None, silent=False):
    if last is None:
        last = []
    nums = [a, b]
    nums.sort()
    a, b = nums
    if not silent:
        sys.stdout.write("{a}, {b} -> ".format(a=a, b=b))
    if a == b or 0 in nums:
        if not silent:
            print("end")
        return True
    b -= a
    a *= 2
    if [a, b] in last:
        if not silent:
            print("loop")
        return False
    last.append([a, b])
    return f_game_ends(a, b, last, silent)


# # TODO problem on 42, 2   35, 5
# # TODO optmize
# def game_ends2(*nums):
#     a, b = sorted(nums)
#     return (b // a) % 2 != 0


# def test(n1, n2=None, samples=1000):
#     from random import randint

#     if n2 is None:
#         n2 = n1
#     r = [[randint(1, n1), randint(1, n2)] for _ in range(samples)]
#     for n in r:
#         if game_ends(n[0], n[1], silent=True) != game_ends2(n[0], n[1]):
#             print(f"Failed on {n[0]} {n[1]}")
#             game_ends(n[0], n[1])
#             print(f"\n" + ("-" * 80))


from itertools import permutations
from pprint import pprint

"""
abcd   abcd bcbd adbc
"""


def pair_permutations(p_list):
    yield p_list
    for x in pair_permutations(p_list + 1):
        yield x


def test(s=1, n=100):
    c = int(log2(2 * s))
    for i in range(s, n):
        if f_game_ends(s, i, silent=True):
            sys.stdout.write("{i}  ".format(i=i))
            c += 1
    print()


def pair_permutations(p_list):
    if len(p_list) == 0:
        return []
    p = []
    for i, item in enumerate(p_list[1:]):
        for rest in pair_permutations([n for j, n in enumerate(p_list[1:]) if j != i]):
            p.append([p_list[0], item] + rest)
    return [p_list] if not p else p


from copy import copy
from math import log

# def log2(x: int) -> float:
#     """Returns the log on base 2 of x.

#     :param x: Number
#     :type x: int
#     :rtype: float
#     """
#     return log(x) / log(2)


########################################
###### SOLUTION STARTS HERE

def game_ends(a, b):
    """Determines if a game will eventually end, returning True if it does end,
    or False if it will fall on an infinite loop.

    :param a: Number of bananas of player 1
    :type a: int
    :param b: Number of bananas of player 2
    :type b: int
    :rtype: bool
    """

    def _game_ends(a, b, res):
        a, b = sorted([a, b])
        # Small optimization. If the sum of the numbers is a potency of 2
        # the game will end
        if a == b or bin(a + b).count("1") == 1:
            return True
        b -= a
        a *= 2
        # Another small optimization is if the numbers are multiple by an even number
        # the game is endless
        if (b // a) % 2 == 0 or [a, b] in res:
            return False
        res.append([a, b])
        return _game_ends(a, b, res)

    return _game_ends(a, b, [])


def solution(banana_list):
    # Store all possible endless games that can happen in banana_list as a network
    endless_games = {i: [] for i in range(len(banana_list))}
    for i, a in enumerate(banana_list):
        for j, b in enumerate(banana_list[(i + 1) :]):
            if not game_ends(a, b):
                j = i + j + 1
                endless_games[i].append(j)
                endless_games[j].append(i)

    # Eliminate the ones with smaller pair possibilities first, matching them with others
    # with the smaller pair possibilities
    sorted_idx = sorted(endless_games, key=lambda i: len(endless_games[i]))
    removed_idx = []
    for i in sorted_idx:
        if i not in removed_idx:
            removal_candidates = [j for j in endless_games[i] if j not in removed_idx]
            if not removal_candidates:
                continue
            j = min(
                removal_candidates,
                key=lambda i: len([j for j in endless_games[i] if j not in removed_idx]),
            )
            removed_idx.append(i)
            removed_idx.append(j)

    return len(banana_list) - len(removed_idx)


if __name__ == "__main__":
    debug()
    c = 0
    for i in range(1, 101):
        for j in range(i, 101):
            game_ends(i, j)
            c += 1
    debug("Did {c} game ends -- ".format(c=c))
    assert solution([1, 1]) == 2
    debug()
    assert solution([1, 1, 1]) == 3
    debug()
    assert solution([1, 1, 3, 5]) == 2
    debug()
    assert solution([1, 2, 4, 8, 16]) == 1
    debug()
    assert solution([1, 7, 3, 21, 13, 19]) == 0
    debug()
    assert solution([1, 1, 3, 5, 3, 7, 3, 7]) == 2
    debug()
    assert solution([1, 1, 3, 5, 3, 7, 3, 7, 3, 7, 99, 1]) == 2
    debug()
    assert solution([1, 1, 3, 5, 3, 7, 3, 7, 3, 7, 99, 1, 2, 2]) == 0
    debug()
    assert solution(list(range(1, 100))) == 1
    debug()
