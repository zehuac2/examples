from typing import Generic, TypeVar, List, Callable, Tuple, Optional

T = TypeVar('T')
TPriority = TypeVar('TPriority')

class PriorityQueue(Generic[T, TPriority]):
    def __init__(
        self,
        priority_comparer: Optional[Callable[[TPriority, TPriority], int]] = None,
        element_comparer: Optional[Callable[[T, T], int]] = None
    ):
        self._priority_comparer = priority_comparer or (lambda a, b: (a > b) - (a < b))
        self._element_comparer = element_comparer or (lambda a, b: (a > b) - (a < b))
        self._entries: List[Tuple[TPriority, T]] = []  # 0-based index

    @property
    def count(self) -> int:
        return len(self._entries)

    @property
    def _root(self) -> int:
        return 0

    def add(self, element: T, priority: TPriority) -> None:
        self._entries.append((priority, element))
        self._heapify_up(len(self._entries) - 1)

    def peek(self) -> Tuple[TPriority, T]:
        return self._entries[self._root]

    def pop(self) -> Tuple[TPriority, T]:
        output = self._entries[self._root]
        self._swap(self._root, len(self._entries) - 1)
        self._entries.pop()
        self._heapify_down(self._root)
        return output

    def update(self, element: T, old_priority: TPriority, new_priority: TPriority) -> None:
        for i in range(self._root, len(self._entries)):
            if self._element_comparer(self._entries[i][1], element) == 0:
                self._entries[i] = (new_priority, self._entries[i][1])
                if self._priority_comparer(new_priority, old_priority) <= 0:
                    self._heapify_up(i)
                else:
                    self._heapify_down(i)
                return

    def _get_left_child(self, index: int) -> int:
        return 2 * index + 1

    def _get_right_child(self, index: int) -> int:
        return 2 * index + 2

    def _get_parent(self, index: int) -> int:
        return (index - 1) // 2 if index > 0 else 0

    def _get_priority(self, index: int) -> TPriority:
        return self._entries[index][0]

    def _has_children(self, index: int) -> bool:
        left = self._get_left_child(index)
        return left < len(self._entries)

    def _max_priority_child(self, index: int) -> int:
        left = self._get_left_child(index)
        right = self._get_right_child(index)
        if right < len(self._entries):
            if self._priority_comparer(self._get_priority(left), self._get_priority(right)) <= 0:
                return left
            return right
        elif left < len(self._entries):
            return left
        return -1

    def _swap(self, a: int, b: int) -> None:
        self._entries[a], self._entries[b] = self._entries[b], self._entries[a]

    def _heapify_up(self, index: int) -> None:
        if index == self._root:
            return
        parent = self._get_parent(index)
        if self._priority_comparer(self._get_priority(index), self._get_priority(parent)) < 0:
            self._swap(index, parent)
            self._heapify_up(parent)

    def _heapify_down(self, index: int) -> None:
        child = self._max_priority_child(index)
        if child != -1 and self._priority_comparer(self._get_priority(index), self._get_priority(child)) > 0:
            self._swap(child, index)
            self._heapify_down(child)
