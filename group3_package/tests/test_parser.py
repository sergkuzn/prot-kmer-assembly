"""Tests for the PARSER."""

from src import parser


class TestParser:

    def test_parse(self):
        """check if output is list and contains only A,G,C,T"""
        path_x = "../tests/test.fastq"
        out = parser.parse(path=path_x)
        assert (type(out) is list) is True
        allowed = set(["A", "C", "G", "T"])
        assert (set(out[-1]) <= allowed) is True
