import collections
import typing
import functools
from unittest import mock
import pytest

P = typing.ParamSpec("P")
T = typing.TypeVar("T")
FuncT = typing.Callable[P, T]


def lru_cache(
    func: FuncT | None = None,
    *,
    maxsize: int,
) -> typing.Callable[[FuncT], FuncT]:
    if func is None:
        return functools.partial(lru_cache, maxsize=maxsize)

    cache: typing.OrderedDict[int, typing.Any] = collections.OrderedDict()

    def update_cache(key: int, value: typing.Any) -> None:
        cache[key] = value
        cache.move_to_end(key, last=False)
        if len(cache) > maxsize:
            cache.popitem()

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        key = hash((args, tuple(kwargs.items())))
        if key not in cache:
            value = func(*args, **kwargs)
            update_cache(key, value)
        return cache[key]

    return wrapper


class LRUCache:
    def __init__(self, maxsize: int) -> None:
        self._maxsize = maxsize
        self._cache: typing.OrderedDict[int, typing.Any] = collections.OrderedDict()

    def __call__(self, func: FuncT) -> FuncT:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            key = hash((args, tuple(kwargs.items())))
            if key not in self._cache:
                value = func(*args, **kwargs)
                self._update_cache(key, value)
            return self._cache[key]

        return wrapper

    def _update_cache(self, key: int, value: typing.Any) -> None:
        self._cache[key] = value
        self._cache.move_to_end(key, last=False)
        if len(self._cache) > self._maxsize:
            self._cache.popitem()


@pytest.mark.parametrize("cache", [lru_cache, LRUCache])
def test_lru_cache(cache):
    def f(n: int) -> int:
        return n

    mocked = mock.Mock(wraps=f)
    f = cache(maxsize=3)(mocked)

    assert f(1) == 1
    assert f(2) == 2
    assert f(3) == 3
    assert mocked.call_count == 3
    assert f(1) == 1
    assert f(4) == 4
    assert mocked.call_count == 4
    assert f(2) == 2
    assert f(3) == 3
    assert mocked.call_count == 4


@lru_cache(maxsize=3)
def f(n: int) -> int:
    print("f is called")
    return n


if __name__ == "__main__":
    print(f(1))
    print(f(2))
    print(f(3))
    print(f(1))
    print(f(4))
    print(f(2))
    print(f(3))
