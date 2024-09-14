import typing
import functools
from unittest import mock
import pytest


def cached[T, **P](func: typing.Callable[P, T]) -> typing.Callable[P, T]:
    cache: dict[int, typing.Any] = {}

    @functools.wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
        key = hash((args, tuple(kwargs.items())))
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]

    return wrapper


class Cached[T, **P]:
    def __init__(self, func: typing.Callable[P, T]) -> None:
        self._cache: dict[int, typing.Any] = {}
        self._func = func
        functools.update_wrapper(self, func)

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> T:
        key = hash((args, tuple(kwargs.items())))
        if key not in self._cache:
            self._cache[key] = self._func(*args, **kwargs)
        return self._cache[key]


@pytest.mark.parametrize("cached", [cached, Cached])
def test_lru_cached(cached):
    def f(n: int) -> int:
        return n

    mocked = mock.Mock(wraps=f)
    f = cached(mocked)

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


@Cached
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
