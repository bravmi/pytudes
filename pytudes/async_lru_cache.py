import asyncio
import collections
import typing
import functools

P = typing.ParamSpec("P")
T = typing.TypeVar("T")
AsyncFuncT = typing.Callable[P, typing.Awaitable[T]]


def async_lru_cache(
    func: AsyncFuncT | None = None,
    *,
    maxsize: int,
) -> typing.Callable[[AsyncFuncT], AsyncFuncT]:
    if func is None:
        return functools.partial(async_lru_cache, maxsize=maxsize)

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


class AsyncLRUCache:
    def __init__(self, maxsize: int) -> None:
        self._maxsize = maxsize
        self._cache: typing.OrderedDict[int, typing.Any] = collections.OrderedDict()

    def __call__(self, func: AsyncFuncT) -> AsyncFuncT:
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


@async_lru_cache(maxsize=3)
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
    print(f.__annotations__)
    asyncio.run(main())
