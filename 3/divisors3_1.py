"""A "lucky triple" is a tuple (x, y, z) where x divides y and y divides z,
such as (1, 2, 4). With that information, you can figure out which list
contains the number of access codes that matches the number of locks on the
door when you're ready to go in (for example, if there's 5 passcodes, you'd
need to find a list with 5 "lucky triple" access codes).

Write a function solution(l) that takes a list of positive integers l and counts the number of "lucky triples" of (li, lj, lk) where the list indices meet the requirement i < j < k.  The length of l is between 2 and 2000 inclusive.  The elements of l are between 1 and 999999 inclusive.  The solution fits within a signed 32-bit integer. Some of the lists are purposely generated without any access codes to throw off spies, so if no triples are found, return 0.

For example, [1, 2, 3, 4, 5, 6] has the triples: [1, 2, 4], [1, 2, 6], [1, 3, 6], making the solution 3 total.

##############################

lucky triple => [x, y, z] where y/x is int and z/y is int e.g. [1, 2, 4].
goal: given a list l with len > 2 count number of lucky triples on it.


$$$$$$$$$$

Combinations:
    ** 2

    **[] 3
    *[]*
    []**


choose 2 in chain[1:] if first % second == 0

1 2 4 8
1 2 4
1 2 8
2 4 8
1 4 8

##############################
"""


def divisors_tree(numbers, numerator):
    tree = {}
    for i, denominator in enumerate(numbers):
        if numerator % denominator == 0:
            if numerator in tree:
                tree[numerator].append(divisors_tree(numbers[(i + 1) :], denominator))
            else:
                tree[numerator] = [divisors_tree(numbers[(i + 1) :], denominator)]
    return tree if tree else {numerator: []}


###### SOLUTION STARTS HERE


def lucky_tripple_count(numbers, numerator, recursion_level=0, root=False):
    if recursion_level == 2:
        return 1
    count = 0
    for i, denominator in enumerate(numbers):
        if numerator % denominator == 0:
            count += lucky_tripple_count(
                numbers[(i + 1) :], denominator, recursion_level + 1
            )
    return count


def solution(l):
    l.sort()
    count = 0
    for i, numerator in enumerate(l[::-1]):
        test_numbers = l[-(i + 2) :: -1]
        if len(test_numbers) < 2:
            break
        count += lucky_tripple_count(test_numbers, numerator, root=True)
    return count


def solution(l):
    divisors_indexes = [
        [
            i + j + 1
            for j, numerator in enumerate(l[i + 1 :])
            if numerator % denominator == 0
        ]
        for i, denominator in enumerate(l)
    ]

    return sum(
        [
            sum([len(divisors_indexes[idx]) for idx in idx_list])
            for idx_list in divisors_indexes
        ]
    )


if __name__ == "__main__":
    assert solution([1, 2, 3, 4, 5, 6]) == 3
    assert solution([1, 1, 1]) == 1
    assert solution([2, 4, 8]) == 1
    assert solution([1, 2]) == 0
