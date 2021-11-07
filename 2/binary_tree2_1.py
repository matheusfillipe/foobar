"""Flux chains require perfect binary trees, so Lambda's design arranged the
ion flux converters to form one. To label them, Lambda performed a post-order
traversal of the tree of converters and labeled each converter with the order
of that converter in the traversal, starting at 1. For example, a tree of 7
converters would look like the following:

   7
 3   6
1 2 4 5
                31
       15                   30
   7       14         22          29
 3   6  10   13    18    21    25    28
1 2 4 5 8 9 11 12 16 17 19 20 23 24 26 27

Write a function solution(h, q) - where h is the height of the perfect tree of converters and q is a list of positive integers representing different flux converters - which returns a list of integers p where each element in p is the label of the converter that sits on top of the respective converter in q, or -1 if there is no such converter.  For example, solution(3, [1, 4, 7]) would return the converters above the converters at indexes 1, 4, and 7 in a perfect binary tree of height 3, which is [3, 6, -1].

The domain of the integer h is 1 <= h <= 30, where h = 1 represents a perfect binary tree containing only the root, h = 2 represents a perfect binary tree with the root and two leaf nodes, h = 3 represents a perfect binary tree with the root, two internal nodes and four leaf nodes (like the example above), and so forth.  The lists q and p contain at least one but no more than 10000 distinct integers, all of which will be between 1 and 2^h-1, inclusive.
"""


class Node:
    def __init__(self, value, left=None, right=None):
        """Simple binary node that stores a value."""
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return "%s: {%s %s}" % (self.value, self.left or "", self.right or "")


def tree(h, accumulated=0):
    """Returns the root node a tree or a subtree."""
    value = 2 ** h - 1 + accumulated
    if h > 0:
        return Node(
            value,
            tree(h - 1, accumulated),
            tree(h - 1, 2 ** (h - 1) - 1 + accumulated),
        )


# Will only work if q doesn't have repeated numbers
def solution(h, q):
    res = [-1 for _ in range(len(q))]
    node_list = [tree(h)]

    # Transverse binary tree
    while len(node_list) > 0:
        node = node_list.pop()
        if node.left is None and node.right is None:
            continue
        if node.left:
            node_list.append(node.left)
            if node.left.value in q:
                res[q.index(node.left.value)] = node.value
        if node.right:
            node_list.append(node.right)
            if node.right.value in q:
                res[q.index(node.right.value)] = node.value

    return res


if __name__ == "__main__":
    assert solution(3, [1, 4, 7]) == [3, 6, -1]
    assert solution(3, [7, 3, 5, 1]) == [-1, 7, 6, 3]
    assert solution(5, [19, 14, 28]) == [21, 15, 29]
