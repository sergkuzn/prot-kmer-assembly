from src import heap_utils


class TestHeapUtils:
    def test_create_max_heap(self):
        items = [(1, 2, 2), (2, 3, 4), (3, 4, 3), (4, 2, 1)]

        heap_utils.create_max_heap(items)

    def test_pop_max(self):
        items = [(1, 2, 2), (2, 3, 4), (3, 4, 3), (4, 2, 1)]

        heap = heap_utils.create_max_heap(items)
        assert heap.pop_max() == (2, 3, 4)

    def test_delete(self):
        items = [(1, 2, 2), (2, 3, 4), (3, 4, 3), (4, 2, 1)]

        heap = heap_utils.create_max_heap(items)
        heap.delete((2, 3))
        assert heap.pop_max() == (3, 4, 3)

    def test_push(self):
        items = [(1, 2, 2), (2, 3, 4), (3, 4, 3), (4, 2, 1)]

        heap = heap_utils.create_max_heap(items)
        heap.push((5, 6, 7))
        assert heap.pop_max() == (5, 6, 7)
