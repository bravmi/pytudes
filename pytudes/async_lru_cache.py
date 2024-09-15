import asyncio
import typing
import functools
from unittest import mock
from . import lru_dict

import pytest


def async_lru_cache[
    T, **P
](maxsize: int) -> typing.Callable[
    [typing.Callable[P, typing.Awaitable[T]]], typing.Callable[P, typing.Awaitable[T]]
]:
    def decorator(
        func: typing.Callable[P, typing.Awaitable[T]]
    ) -> typing.Callable[P, typing.Awaitable[T]]:
        cache = lru_dict.LRUDict(maxsize)

        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            key = hash((args, tuple(kwargs.items())))
            if key not in cache:
                cache[key] = await func(*args, **kwargs)
            return cache[key]

        return wrapper

    return decorator


class AsyncLRUCache:
    def __init__(self, maxsize: int) -> None:
        self._maxsize = maxsize

    def __call__[
        T, **P
    ](self, func: typing.Callable[P, typing.Awaitable[T]]) -> typing.Callable[
        P, typing.Awaitable[T]
    ]:
        cache = lru_dict.LRUDict(self._maxsize)

        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            key = hash((args, tuple(kwargs.items())))
            if key not in cache:
                cache[key] = await func(*args, **kwargs)
            return cache[key]

        return wrapper


@pytest.mark.parametrize("cache", [async_lru_cache, AsyncLRUCache])
async def test_async_lru_cache(cache):
    async def f(n: int) -> int:
        return n

    mocked = mock.AsyncMock(wraps=f)
    f = cache(maxsize=3)(mocked)

    assert await f(1) == 1
    assert await f(2) == 2
    assert await f(3) == 3
    assert mocked.call_count == 3
    assert await f(4) == 4
    assert await f(1) == 1
    assert mocked.call_count == 5
    assert await f(3) == 3
    assert mocked.call_count == 5
    assert await f(1) == 1
    assert mocked.call_count == 5


@AsyncLRUCache(maxsize=3)
async def f(n: int) -> int:
    print("f is called")
    return n


async def main():
    print(await f(1))
    print(await f(2))
    print(await f(3))
    print(await f(1))
    print(await f(4))
    print(await f(2))
    print(await f(3))


if __name__ == "__main__":
    asyncio.run(main())
