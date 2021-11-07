"""It appears that, while random, the probability of each structure
transforming is fixed. That is, each time the ore is in 1 state, it has the
same probabilities of entering the next state (which might be the same state).
You have recorded the observed transitions in a matrix. The others in the lab
have hypothesized more exotic forms that the ore can become, but you haven't
seen all of them.

Write a function solution(m) that takes an array of array of nonnegative ints representing how many times that state has gone to the next state and return an array of ints for each terminal state giving the exact probabilities of each terminal state, represented as the numerator for each state, then the denominator for all of them at the end and in simplest form. The matrix is at most 10 by 10. It is guaranteed that no matter which state the ore is in, there is a path from that state to a terminal state. That is, the processing will always eventually end in a stable state. The ore starts in state 0. The denominator will fit within a signed 32-bit integer during the calculation, as long as the fraction is simplified regularly.

For example, consider the matrix m:
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
So, we can consider different paths to terminal states, such as:
s0 -> s1 -> s3
s0 -> s1 -> s0 -> s1 -> s0 -> s1 -> s4
s0 -> s1 -> s0 -> s5
Tracing the probabilities of each, we find that
s2 has probability 0
s3 has probability 3/14
s4 has probability 1/7
s5 has probability 9/14
So, putting that together, and making a common denominator, gives an answer in the form of
[s2.numerator, s3.numerator, s4.numerator, s5.numerator, denominator] which is
[0, 3, 2, 9, 14].

########################################
$$$$$$$$$$$

[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
s0 {s2: 1/2, s5: 1/2}
s1 {s0: 4/9, s3/3/9, s4: 2/9}

ps5 = 1/2 + 1/2(4/9*ps5)   0.6428571428571428 0.6428571428571429
ps4 = 0 + 1/2*(2/9+4/9*ps4) --> 2ps4 = 2/9 + 4/9*ps4 --> ps4 = 2/9 / (2-4/9) = 2/9 / (14/9) = 1/7
ps3 = 0 + 1/2(3/9+4/9*ps3) --> ps3 = 3/18 + 4/18 ps3 --> ps3 (14/18) = 3/18 --> ps3 = 3/14
ps2 = 0

Mij --> normalized probabilities matrix
Pab = Mab + sum[i unless i==a](MaiPib)
Goal: P0_{terminals}
[
        [0, 2, 1, 0, 0],
        [0, 0, 0, 3, 4],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
]

ps2 = 1/3
ps3 = 2/3*(3/7) = 2/7
ps4 = 2/3 * 4/7 = 8/21

[7, 6, 8, 21]

Mij --> normalized probabilities matrix
Pab = Mab + sum[i unless i==a](MaiPib)

########################################

m -> [[ints, ints], ...] for ints >= 0 --> markov matrix
solution(m) --> [numerators, .., common_denominator]

[0, 3, 2, 9, 14].
[
  [0,1,0,0,0,1],  # s0, the initial state, goes to s1 and s5 with equal probability
  [4,0,0,3,2,0],  # s1 can become s0, s3, or s4, but with different probabilities
  [0,0,0,0,0,0],  # s2 is terminal, and unreachable (never observed in practice)
  [0,0,0,0,0,0],  # s3 is terminal
  [0,0,0,0,0,0],  # s4 is terminal
  [0,0,0,0,0,0],  # s5 is terminal
]
s0 {s2: 1/2, s5: 1/2}
s1 {s0: 4/9, s3: 3/9, s4: 2/9}

SPG(q) = q/(1-q)

ps2 = 0
ps3 = 0 + 1/2*3/9 + 1/2*SPG(4/9*1/2)*3/9= 3/14
ps4 = 0 + 1/2*2/9 + 1/2*spg(4/9*1/2)*2/9= 1/7
ps5 = 1/2 + spg(4/9*1/2)*1/2= 9/14

* 2 types of loops -> A-X-A-D and A-X-A-X-D

ps0n = M0n + sum[i in range(1, len(M))] {M0i*Min + M0i*SPG(Mi0*M0i)*Min + SPG(M0i*Mi0)*Min .... }
Pab = Mab + sum[i!=a] {Mai*Mib + SPG(Mai*Mia)*Mab + Mai*SPG(Mia*Mai)*Mib + Mai*Pib}
 chance of going directly from 0 + sum of (change of going through this one)
"""


from fractions import Fraction

import numpy as np

# from fractions import Fraction, gcd

T = [
    [0, 1, 0, 0, 0, 1],
    [4, 0, 0, 3, 2, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]

T1 = [
    [0, 2, 1, 0, 0, 0],
    [2, 0, 0, 3, 4, 4],
    [1, 2, 2, 0, 3, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]
T2 = [
    [1, 2, 0, 0, 0, 0],
    [0, 0, 3, 2, 0, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]
T3 = [
    [1, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1],
    [0, 0, 3, 2, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
]
T4 = [
    [1, 2, 3, 0, 0, 0],
    [0, 2, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [3, 0, 3, 2, 0, 0],
    [1, 1, 0, 0, 0, 0],
]
T5 = [
    [0, 0, 0, 0, 0, 0],
    [1, 2, 3, 0, 1, 0],
    [0, 2, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [1, 1, 0, 0, 0, 0],
]


# TODO python3 only REMOVE
from math import lcm as _lcm

# def lcm(numbers):
#     """Least common multiplier."""
#     r = 1
#     for n in numbers:
#         r *= n // gcd(r, n)
#     return r


def lcm(numbers):
    return _lcm(*numbers)


def prod(*args):
    """Computes the product of multiple numbers."""
    p = 1
    for n in args:
        p *= n
    return p


def gp_sum(q):
    """Sum of infinite geometric progression with ratio q starting valid for 0.

    =< q < 1.
    """
    return q / (1 - q)


def loop_prob(m, a, b, indexes=[]):
    """Probability of a loop starting on *a*, ending on *b* and passing
    through.

    *indexes*
    """
    return sum(
        [
            gp_sum(m[a][i] * m[i][a]) * m[a][b]
            + m[a][i] * gp_sum(m[i][a] * m[a][i]) * m[i][b]
            for i in indexes
            if i not in [a, b]
        ]
    )


def proba2b(m, a, b, indexes=[]):
    """Probability of getting to index *b* parting from *a*.

    Also passing by *indexes* if given
    """
    # There is no reason to do the fancy linear algebra with eigenvectors and eigeinvalues!!!
    # We are doing the sum of the direct probabilities from the normalized matrix plus
    # the sum of probabilities for the loops considering the probability of them as the sum of an
    # Infinite geometric progressions

    indexes += [a]
    p = m[a][b]
    for i, row in enumerate(m):
        if i in indexes:
            continue
        p += (
            m[a][i] * m[i][b]
            + loop_prob(m, a, b, [i])
            # + m[a][i] * proba2b(m, i, b, indexes)
        )

    return p

    # return m[a][b] + sum(
    #     [
    #         m[a][i] * m[i][b]
    #         + loop_prob(m, a, b, [i])
    # #         + m[a][i]*proba2b(m, i, b, indexes)
    #         for i, row in enumerate(m)
    #         if i not in indexes
    #     ]
    # )


def solution(m):
    # Considering that all terminals (lines with only 0's) are all in the bottom of the matrix
    normalized = [[Fraction(n, sum(line)) for n in line] for line in m if sum(line) > 0]
    probs = [proba2b(normalized, 0, i) for i in range(len(normalized), len(m))]
    _lcm = lcm([frac.denominator for frac in probs])
    return [(frac * _lcm).numerator for frac in probs] + [_lcm]


###### SOLUTION STARTS HERE
import numpy as np

MAX_DENOMINATOR = 2 ** 32


def solution(m):
    # The goal is to find the probability of end up in a terminal state starting from the initial state
    # The absorbing probabilities for a markov chain is given by the matrix dot multiplication
    # B = NxR where N = inv(I-Q) and R is formed by the columns of m that represent the connections
    # between transient states to absorbing/terminal states.
    normalized = []
    transient_indexes = []
    terminal_indexes = []
    for i, row in enumerate(m):
        s = sum(row)
        if s != 0:
            normalized.append([float(n) / s for n in row])
            transient_indexes.append(i)
        elif len(normalized) == 0:  # The initial state is a terminal state!
            return [1] + [0] * (sum([1 for row in m if sum(row) == 0]) - 1) + [1]
        else:
            terminal_indexes.append(i)

    # It may happen that there are terminal states followed by transient states, so we adjust the columns
    normalized = np.array(normalized)[:, transient_indexes + terminal_indexes]

    n_transients = len(transient_indexes)
    R = np.array([row[n_transients:] for i, row in enumerate(normalized)])
    N = np.linalg.inv(
        [
            [(-p if j != i else 1 - p) for j, p in enumerate(row[:n_transients])]
            for i, row in enumerate(normalized[:n_transients])
        ]
    )

    frac_probs = [
        Fraction.from_float(n).limit_denominator(max_denominator=MAX_DENOMINATOR)
        # We only need the first row of the dot product so no reason to do the entire dot product
        for n in np.dot(N[0], R)
    ]

    _lcm = lcm([n.denominator for n in frac_probs])
    return [(Fraction(n) * _lcm).numerator for n in frac_probs] + [_lcm]


nsol = solution
if __name__ == "__main__":
    assert (
        solution(
            [
                [0, 2, 1, 0, 0],
                [0, 0, 0, 3, 4],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
            ]
        )
        == [7, 6, 8, 21]
    )
    assert (
        solution(
            [
                [0, 1, 0, 0, 0, 1],
                [4, 0, 0, 3, 2, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0],
            ]
        )
        == [0, 3, 2, 9, 14]
    )
