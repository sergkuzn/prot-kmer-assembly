import numpy as np
import numba as nb
from numba import njit
from numba.experimental import jitclass
from typing import List, Tuple

"""
heapify_max, siftup_max, siftdown_max, heappop_max, heappush
functions are taken from https://github.com/python/cpython/blob/main/Lib/heapq.py
and slightly modified
"""


@njit
def heapify_max(x):
    """Transform list into a maxheap, in-place, in O(len(x)) time."""
    n = len(x)
    for i in np.arange(n // 2)[::-1]:
        siftup_max(x, i)


@njit
def siftup_max(heap, pos):
    'Maxheap variant of _siftup'
    endpos = len(heap)
    startpos = pos
    newitem = heap[pos]
    # Bubble up the larger child until hitting a leaf.
    childpos = 2 * pos + 1  # leftmost child position
    while childpos < endpos:
        # Set childpos to index of larger child.
        rightpos = childpos + 1
        if rightpos < endpos and not heap[rightpos][2] < heap[childpos][2]:
            childpos = rightpos
        # Move the larger child up.
        heap[pos] = heap[childpos]
        pos = childpos
        childpos = 2 * pos + 1
    # The leaf at pos is empty now.  Put newitem there, and bubble it up
    # to its final resting place (by sifting its parents down).
    heap[pos] = newitem
    siftdown_max(heap, startpos, pos)


@njit
def siftdown_max(heap, startpos, pos):
    'Maxheap variant of _siftdown'
    newitem = heap[pos]
    # Follow the path to the root, moving parents down until finding a place
    # newitem fits.
    while pos > startpos:
        parentpos = (pos - 1) >> 1
        parent = heap[parentpos]
        if parent[2] < newitem[2]:
            heap[pos] = parent
            pos = parentpos
            continue
        break
    heap[pos] = newitem


@njit
def heappop_max(heap):
    """Maxheap version of a heappop."""
    lastelt = heap.pop()  # raises appropriate IndexError if heap is empty
    if heap:
        returnitem = heap[0]
        heap[0] = lastelt
        siftup_max(heap, 0)
        return returnitem
    return lastelt


@njit
def heappush(heap, item):
    """Push item onto heap, maintaining the heap invariant."""
    heap.append(item)
    siftdown_max(heap, 0, len(heap) - 1)


spec_maxheap = [
    ('heap', nb.types.ListType(nb.types.UniTuple(nb.int64, 3))),
    ('deleted_items', nb.types.DictType(nb.types.UniTuple(nb.types.int64, 2), nb.types.boolean))
]


@jitclass(spec_maxheap)
class MaxHeap:
    """
    Max heap.

    input_list: list of tuples of str
        Each item is a tuple of 3 int: (str_id_1, str_id_2, overlap_length).
        Elements are sorted based onn the overlap_length value.

    deleted_items: Dict
        Empty dict for storing deleted items.

    Description
    -----------
    Lazy deletion implemented: an item to delete is only marked deleted.
    When an element is popped, it is checked, whether it is "deleted", if yes, pop operation
    is further called until a non-deleted element is returned.
    """

    def __init__(self, input_list, deleted_items):
        self.heap = input_list
        heapify_max(self.heap)
        self.deleted_items = deleted_items

    def pop_max(self) -> Tuple[int, int, int]:
        while True:
            el = heappop_max(self.heap)
            if (el[0], el[1]) not in self.deleted_items:
                break
        return el

    def delete(self, item: Tuple[int, int]) -> 'MaxHeap':
        self.deleted_items[item] = True
        return self

    def push(self, item: Tuple[int, int, int]) -> 'MaxHeap':
        heappush(self.heap, item)
        return self


def create_max_heap(item_list: List[Tuple[int, int, int]]) -> MaxHeap:
    """
    Create a max heap.

    Parameters
    ----------
    item_list: list of tuples of str
        Each item is a tuple of 3 int: (str_id_1, str_id_2, overlap_length).

    """
    # to store deleted items
    deleted_items = nb.typed.Dict.empty(
        key_type=nb.types.UniTuple(nb.types.int64, 2),
        value_type=nb.types.boolean)

    numba_item_list = nb.typed.List(item_list)

    return MaxHeap(numba_item_list, deleted_items)
