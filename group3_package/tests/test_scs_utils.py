from src import scs_utils


class TestScsUtils:
    def test_find_overlap_length(self):
        assert scs_utils.find_overlap_length('ABC', 'DEF', 1) == 0
        assert scs_utils.find_overlap_length('ABC', 'CDE', 1) == 1
        assert scs_utils.find_overlap_length('ABC', 'CDE', 2) == 0
        assert scs_utils.find_overlap_length('ABC', 'BCD', 1) == 2
