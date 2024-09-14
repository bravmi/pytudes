import asyncio
import collections
import typing
import functools
from unittest import mock

import pytest


def async_lru_cache[
    T, **P
](maxsize: int) -> typing.Callable[
    [typing.Callable[P, typing.Awaitable[T]]], typing.Callable[P, typing.Awaitable[T]]
]:
    def decorator(
        func: typing.Callable[P, typing.Awaitable[T]]
    ) -> typing.Callable[P, typing.Awaitable[T]]:
        cache: typing.OrderedDict[int, typing.Any] = collections.OrderedDict()

        def update_cache(key: int, value: typing.Any) -> None:
            cache[key] = value
            cache.move_to_end(key, last=False)
            if len(cache) > maxsize:
                cache.popitem()

        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            key = hash((args, tuple(kwargs.items())))
            if key not in cache:
                value = await func(*args, **kwargs)
                update_cache(key, value)
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
        cache: typing.OrderedDict[int, typing.Any] = collections.OrderedDict()

        def update_cache(key: int, value: typing.Any) -> None:
            cache[key] = value
            cache.move_to_end(key, last=False)
            if len(cache) > self._maxsize:
                cache.popitem()

        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            key = hash((args, tuple(kwargs.items())))
            if key not in cache:
                value = await func(*args, **kwargs)
                update_cache(key, value)
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
