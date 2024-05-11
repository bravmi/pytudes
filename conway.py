"""
Based on Jack Diederich's talk from PyCon 2012
"""

import collections as co
import itertools as it


def neighbors(point):
    x, y = point
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1
    yield x + 1, y + 1
    yield x + 1, y - 1
    yield x - 1, y + 1
    yield x - 1, y - 1


def advance(board: set[tuple[int, int]]) -> set[tuple[int, int]]:
    newstate = set()
    recalc = board | set(it.chain(*map(neighbors, board)))
    for point in recalc:
        count = sum((neigh in board) for neigh in neighbors(point))
        if count in [2, 3] and point in board:
            newstate.add(point)
        elif count == 3 and point not in board:
            newstate.add(point)
    return newstate


def advance2(board: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """my take, might be wrong ;)"""
    newstate = set()
    recalc: co.Counter[tuple[int, int]] = co.Counter()
    recalc.update({point: 0 for point in board})  # to make it explicit
    recalc.update(it.chain(*map(neighbors, board)))
    for point, count in recalc.items():
        if count in [2, 3] and point in board:
            newstate.add(point)
        elif count == 3 and point not in board:
            newstate.add(point)
    return newstate


def test_compare():
    glider1 = set([(0, 0), (1, 0), (2, 0), (0, 1), (1, 2)])
    for _ in range(1000):
        glider1 = advance(glider1)

    glider2 = set([(0, 0), (1, 0), (2, 0), (0, 1), (1, 2)])
    for _ in range(1000):
        glider2 = advance2(glider2)

    assert glider1 == glider2


if __name__ == '__main__':
    glider = set([(0, 0), (1, 0), (2, 0), (0, 1), (1, 2)])
    for _ in range(1000):
        glider = advance2(glider)
    print(glider)
