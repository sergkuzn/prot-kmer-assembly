from typing import List, Dict, Tuple
import multiprocessing as mp
import numpy as np


def find_overlap_length(a: str, b: str, min_length: int = 1) -> int:
    """
    Returns the length of the overlap between two strings:
    end of a overlaps with start of b.

    Parameters
    ----------
    a, b : str
        Two input strings.

    min_length: int, default=1
        Minimum length of the overlap (smaller overlaps will not be considered).

    Returns
    -------
    overlap_length: int
        Maximum overlap length. If no overlap detected, returns 0.
    """
    start = 0
    while True:
        start = a.find(b[:min_length], start)
        if start == -1:  # nothing found
            return 0
        if b.startswith(a[start:]):
            return len(a) - start
        start += 1


def get_strings_with_id_dict(strings: List[str]) -> Dict[int, str]:
    """
    Create id for each string.

    Returns
    -------
    strings_dict: dict (int: str)
        Key: string id, value: string.
    """
    return {i: s for i, s in enumerate(strings)}


def do_overlaps(strings_start_end: Tuple[list, int, int]) -> List[Tuple[int, int, int]]:
    """
    Calculate overlaps between strings.

    First string is selected so that its index is between start and end,
    the second string will be each from the string list.

    """
    strings, start, end = strings_start_end
    overlap_sublist = []
    for i in range(start, end):
        (id1, s1) = strings[i]
        for (id2, s2) in strings:
            if id1 != id2:
                overlap_len = find_overlap_length(s1, s2)
                overlap_sublist.append((id1, id2, overlap_len))
    return overlap_sublist


def calc_pairwise_overlaps_parallel_heap(strings_dict: Dict[int, str], num_cpu: int) -> List[Tuple[int, int, int]]:
    """
    Initial pairwise overlap calculation
    (most suitable for heap implementation)

    Parameters
    ----------
    strings_dict: dict of (int: str)
        Key: string id, value: string.

    num_cpu: int
    """
    id_strings_list = list(strings_dict.items())

    if num_cpu == -1:
        num_cpu = mp.cpu_count()

    # divide interval [0, len(strings)] into num_cpu parts
    # f.e. len=10, num_cpu=3: [0, 3, 6, 10]
    index_list = [0]
    for j in range(num_cpu):
        m = int(len(id_strings_list) * (j + 1) / num_cpu)
        index_list.append(m)

    def iterator(index_list):
        """
        returns id_strings_list, start and end indexes
        """
        for i in range(len(index_list) - 1):
            yield id_strings_list, index_list[i], index_list[i + 1]

    # Initial pairwise overlap calculation
    with mp.Pool(num_cpu) as pool:
        result = pool.map(do_overlaps, iterator(index_list))  # list of lists

    # Unite the results from different processes
    overlap_list = []
    for sublist in result:
        overlap_list += sublist
    return overlap_list


def remove_rows_cols(matrix, indexes):
    matrix = np.delete(matrix, indexes, axis=0)
    matrix = np.delete(matrix, indexes, axis=1)
    return matrix


def add_row_col_to_end(matrix, row, col):
    # add column
    matrix = np.concatenate([matrix, col[:, np.newaxis]], axis=1)
    # add row
    matrix = np.concatenate([matrix, row[np.newaxis, :]], axis=0)
    return matrix
