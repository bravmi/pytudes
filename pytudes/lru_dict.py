import collections
import typing


class LRUDict(collections.OrderedDict):
    def __init__(self, maxsize: int) -> None:
        super().__init__()
        self._maxsize = maxsize

    def __setitem__(self, key: int, value: typing.Any) -> None:
        super().__setitem__(key, value)
        if len(self) > self._maxsize:
            self.popitem(last=False)


def test_lru_dict():
    cache = LRUDict(maxsize=3)
    cache[1] = 1
    cache[2] = 2
    cache[3] = 3
    assert cache.keys() == {1, 2, 3}
    cache[4] = 4
    assert cache.keys() == {2, 3, 4}
    cache[5] = 5
    assert cache.keys() == {3, 4, 5}
