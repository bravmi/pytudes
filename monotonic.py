"""
Taken from:
https://nedbatchelder.com/blog/202108/pythonic_monotonic.html
"""

from typing import Iterable, Iterator


def mono_runs_simpler(seq: Iterable) -> Iterator[list[float]]:
    seqit: Iterator[float] = iter(seq)
    run: list[float] = []
    try:
        run = [next(seqit)]
    except StopIteration:
        yield []
        return
    up: bool | None = None

    for v in seqit:
        if up is not None:
            good: bool = (v >= run[-1]) if up else (v < run[-1])
        else:
            up = v >= run[-1]
            good = True

        if good:
            run.append(v)
        else:
            yield run if up else run[::-1]
            run = [v]
            up = None
    if run:
        yield run if up else run[::-1]


def tests_ngeorgescu():
    assert list(mono_runs_simpler([1, 2, 3, 2, 1, 8, 4, 5, 6, 7])) == [
        [1, 2, 3],
        [1, 2],
        [4, 8],
        [5, 6, 7],
    ]

    assert list(mono_runs_simpler([1, 2, 3, 1, 2, 3, 1, 2, 3])) == [
        [1, 2, 3],
        [1, 2, 3],
        [1, 2, 3],
    ]


def tests_mine():
    assert list(mono_runs_simpler([1, 2, 2, 3, 3, 3, 2, 2, 1])) == [
        [1, 2, 2, 3, 3, 3],
        [2, 2],
        [1],
    ]


def tests_travis():
    assert list(mono_runs_simpler([1, 2, 3, 2, 1, 4, 5, 6, 7, 1, 2])) == [
        [1, 2, 3],
        [1, 2],
        [4, 5, 6, 7],
        [1, 2],
    ]

    assert list(mono_runs_simpler([1, 2, 2, 1, 4, 5, 1, 7, 1, 2])) == [
        [1, 2, 2],
        [1, 4, 5],
        [1, 7],
        [1, 2],
    ]

    assert list(mono_runs_simpler([5, 4, 3, 2, 1])) == [[1, 2, 3, 4, 5]]
    assert list(mono_runs_simpler([])) == [[]]


def tests_cj():
    assert list(mono_runs_simpler([1])) == [[1]]
    assert list(mono_runs_simpler([1, 2])) == [[1, 2]]
    assert list(mono_runs_simpler([1, 1])) == [[1, 1]]
    assert list(mono_runs_simpler([2, 1])) == [[1, 2]]
    assert list(mono_runs_simpler([1, 2, 3, 2, 1])) == [[1, 2, 3], [1, 2]]
    assert list(mono_runs_simpler([3, 2, 1, 2, 3])) == [[1, 2, 3], [2, 3]]

    assert list(mono_runs_simpler([1, 1, 2, 2, 1, 1, 2, 2, 1, 1])) == [
        [1, 1, 2, 2],
        [1, 1, 2, 2],
        [1, 1],
    ]


if __name__ == '__main__':
    tests_mine()
