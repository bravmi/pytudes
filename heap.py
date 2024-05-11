import heapq
from typing import Any, Callable


class Heap:
    def __init__(
        self,
        items: list | None = None,
        key: Callable[[Any], Any] | None = None,
    ) -> None:
        self.items = items or []
        heapq.heapify(self.items)
        self.key = key

    def push(self, value) -> None:
        if self.key:
            item = self.key(value), value
        heapq.heappush(self.items, item)

    def pop(self) -> Any:
        if self.key:
            _, value = heapq.heappop(self.items)
            return value
        return heapq.heappop(self.items)

    def __bool__(self) -> bool:
        return bool(self.items)


if __name__ == '__main__':
    min_heap = Heap()
    max_heap = Heap(key=lambda x: -x)
