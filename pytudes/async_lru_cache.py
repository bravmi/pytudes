import asyncio
import collections
import typing
import functools
from unittest import mock

P = typing.ParamSpec("P")
T = typing.TypeVar("T")


class AsyncLRUCache:
    def __init__(self, maxsize: int) -> None:
        self._maxsize = maxsize
        self._cache: typing.OrderedDict[int, typing.Any] = collections.OrderedDict()

    def __call__(
        self, func: typing.Callable[P, typing.Awaitable[T]]
    ) -> typing.Callable[P, typing.Awaitable[T]]:
        @functools.wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            key = hash((args, tuple(kwargs.items())))
            if key not in self._cache:
                value = await func(*args, **kwargs)
                self._update_cache(key, value)
            return self._cache[key]

        return wrapper

    def _update_cache(self, key: int, value: typing.Any) -> None:
        self._cache[key] = value
        self._cache.move_to_end(key, last=False)
        if len(self._cache) > self._maxsize:
            self._cache.popitem()


async def test_async_lru_cache():
    async def f(n: int) -> int:
        return n

    mocked = mock.AsyncMock(wraps=f)
    f = AsyncLRUCache(maxsize=3)(mocked)

    assert await f(1) == 1
    assert await f(2) == 2
    assert await f(3) == 3
    assert mocked.call_count == 3
    assert await f(1) == 1
    assert await f(4) == 4
    assert mocked.call_count == 4
    assert await f(2) == 2
    assert await f(3) == 3
    assert mocked.call_count == 4


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
