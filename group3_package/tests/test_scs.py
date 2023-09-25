from src import scs


class TestScs:
    def test_scs(self):
        strings = ['GHIJKL', 'ABCDEF', 'BCDEFG', 'CDEFGH', 'CDEFGH', 'DEFGHI']

        result = scs.scs(strings)
        assert result == 'ABCDEFGHIJKL'

    def test_greedy_scs_dict(self):
        strings = ['GHIJKL', 'ABCDEF', 'BCDEFG', 'CDEFGH', 'CDEFGH', 'DEFGHI']

        result = scs.greedy_scs_dict(strings)
        assert result == 'ABCDEFGHIJKL'

    def test_greedy_scs_heap(self):
        strings = ['GHIJKL', 'ABCDEF', 'BCDEFG', 'CDEFGH', 'CDEFGH', 'DEFGHI']

        result = scs.greedy_scs_heap(strings)
        assert result == 'ABCDEFGHIJKL'

    def test_greedy_scs_heap_parallel(self):
        strings = ['GHIJKL', 'ABCDEF', 'BCDEFG', 'CDEFGH', 'CDEFGH', 'DEFGHI']

        result = scs.greedy_scs_heap(strings, num_cpu=4)
        assert result == 'ABCDEFGHIJKL'

    def test_greedy_scs_matrix(self):
        strings = ['GHIJKL', 'ABCDEF', 'BCDEFG', 'CDEFGH', 'CDEFGH', 'DEFGHI']

        result = scs.greedy_scs_matrix(strings)
        assert result == 'ABCDEFGHIJKL'

    def test_greedy_fails(self):
        strings = ['ABCD', 'CDBC', 'BCDA']
        greedy = scs.greedy_scs_dict(strings)
        not_greedy = scs.scs(strings)
        assert len(greedy) == 9
        assert len(not_greedy) == 8
