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
        # TODO: try to use match here?
        if count in [2, 3] and point in board:
            newstate.add(point)
        elif count == 3 and point not in board:
            newstate.add(point)
    return newstate


def advance_counter(board: set[tuple[int, int]]) -> set[tuple[int, int]]:
    """My take, might be wrong ;)"""
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
    glider = set([(0, 0), (1, 0), (2, 0), (0, 1), (1, 2)])
    for _ in range(1000):
        glider = advance(glider)

    glider_counter = set([(0, 0), (1, 0), (2, 0), (0, 1), (1, 2)])
    for _ in range(1000):
        glider_counter = advance_counter(glider_counter)

    assert glider == glider_counter


if __name__ == '__main__':
    glider = set([(0, 0), (1, 0), (2, 0), (0, 1), (1, 2)])
    for _ in range(1000):
        glider = advance_counter(glider)
    print(glider)
