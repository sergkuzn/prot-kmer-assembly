import itertools
import math
from tqdm import tqdm
from typing import List
import numpy as np
from .heap_utils import create_max_heap
from .scs_utils import find_overlap_length, get_strings_with_id_dict, calc_pairwise_overlaps_parallel_heap, \
    add_row_col_to_end, remove_rows_cols


def scs(strings: List[str]) -> str:
    """
    Shortest common superstring algorithm.
    (Correct solution guaranteed, but takes long time).

    Parameters
    ----------
    strings: list of str
        Input strings (reads).

    Returns
    -------
    shortest_sup: str
        Shortest common superstring.
    """
    strings = list(set(strings))
    shortest_sup = None
    for perm in tqdm(itertools.permutations(strings),
                     desc='Shortest Common Superstring',
                     total=math.factorial(len(strings))):  # perm - current string ordering
        current_sup = perm[0]
        for i in range(len(strings) - 1):
            overlap_len = find_overlap_length(perm[i], perm[i + 1], min_length=1)
            current_sup += perm[i + 1][overlap_len:]
        if shortest_sup is None or len(current_sup) < len(shortest_sup):
            shortest_sup = current_sup
    return shortest_sup


def greedy_scs_dict(strings: List[str]):
    """
    Greedy shortest common superstring algorithm.
    (Correct solution NOT guaranteed, but takes reasonable time).

    Overlaps are stored in a dict.
    """
    strings = list(set(strings))

    strings_dict = get_strings_with_id_dict(strings)  # str_id: str
    overlap_dict = {}  # (str_id1, str_id2): overlap_len
    id_counter = itertools.count(start=len(strings))  # used to get new id for new merged string

    # Initial pairwise overlap calculation
    for (id1, s1), (id2, s2) in tqdm(itertools.permutations(strings_dict.items(), r=2),
                                     desc='Greedy SCS. Initialization.',
                                     total=len(strings) ** 2 - len(strings)):
        overlap_len = find_overlap_length(s1, s2)
        overlap_dict[(id1, id2)] = overlap_len

    # Find two strings with th ebiggest overlap and merge them. Repeat.
    # At each iteration number of strings in strings_dict decreases by 1, so, (len(strings) - 1) iterations.
    for _ in tqdm(range(len(strings) - 1),
                  desc='Greedy SCS. String merging.'):
        # Find max overlap and corresponding string IDs.
        (merge_id1, merge_id2), max_overlap = max(overlap_dict.items(), key=lambda x: x[1])

        # create new string
        new_string = strings_dict[merge_id1] + strings_dict[merge_id2][max_overlap:]
        new_id = next(id_counter)

        # Delete two strings that were merged
        del strings_dict[merge_id1]
        del strings_dict[merge_id2]

        # calculate overlaps between new string and the old ones
        new_overlaps_list = []
        for (id_, s_) in strings_dict.items():
            new_overlaps_list.append(((new_id, id_),
                                      find_overlap_length(new_string, s_, min_length=overlap_dict[merge_id2, id_]))
                                     )
            new_overlaps_list.append(((id_, new_id),
                                      find_overlap_length(s_, new_string, min_length=overlap_dict[id_, merge_id1]))
                                     )

        # add new overlaps to the storage
        for k, v in new_overlaps_list:
            overlap_dict[k] = v

        # Delete overlap history of merged strings
        del overlap_dict[(merge_id1, merge_id2)]
        del overlap_dict[(merge_id2, merge_id1)]
        for id_ in strings_dict.keys():
            del overlap_dict[(id_, merge_id1)]
            del overlap_dict[(merge_id1, id_)]
            del overlap_dict[(id_, merge_id2)]
            del overlap_dict[(merge_id2, id_)]

        # Add new string to the string set
        strings_dict[new_id] = new_string

    assert len(strings_dict) == 1
    return list(strings_dict.values())[0]


def greedy_scs_heap(strings: List[str], num_cpu: int = 1):
    """
    Greedy shortest common superstring algorithm.
    (Correct solution NOT guaranteed, but takes reasonable time).

    Overlaps are stored in a numba max_heap.
    """
    strings = list(set(strings))

    strings_dict = get_strings_with_id_dict(strings)  # str_id: str
    overlap_dict = {}  # (str_id1, str_id2): overlap_len
    overlap_items_list = []  # tuple(str_id1, str_id2, overlap_len)
    id_counter = itertools.count(start=len(strings))  # used to get new id for new merged string

    # Initial pairwise overlap calculation
    if num_cpu == 1:
        for (id1, s1), (id2, s2) in tqdm(itertools.permutations(strings_dict.items(), r=2),
                                         desc='Greedy SCS + heap. Initialization.',
                                         total=len(strings) ** 2 - len(strings)):
            overlap_len = find_overlap_length(s1, s2)
            overlap_dict[(id1, id2)] = overlap_len
            overlap_items_list.append((id1, id2, overlap_len))
    else:
        overlap_items_list = calc_pairwise_overlaps_parallel_heap(strings_dict, num_cpu)
        overlap_dict = {(el[0], el[1]): el[2] for el in overlap_items_list}

    # construct heap
    heap = create_max_heap(overlap_items_list)

    # Find two strings with the biggest overlap and merge them. Repeat.
    # At each iteration number of strings in strings_dict decreases by 1, so, (len(strings) - 1) iterations.
    for _ in tqdm(range(len(strings) - 1),
                  desc='Greedy SCS + heap. String merging.'):
        # Find max overlap and corresponding string IDs.
        (merge_id1, merge_id2, max_overlap) = heap.pop_max()

        # create new string
        new_string = strings_dict[merge_id1] + strings_dict[merge_id2][max_overlap:]
        new_id = next(id_counter)

        # Delete two strings that were merged and their overlaps
        del strings_dict[merge_id1]
        del strings_dict[merge_id2]
        heap.delete((merge_id1, merge_id2)) \
            .delete((merge_id2, merge_id1))
        for id_ in strings_dict.keys():
            heap.delete((id_, merge_id1)) \
                .delete((merge_id1, id_)) \
                .delete((id_, merge_id2)) \
                .delete((merge_id2, id_))

        # calculate overlaps between new string and the old ones
        new_overlaps_list = []
        for (id_, s_) in strings_dict.items():
            new_overlaps_list.append((new_id, id_,
                                      find_overlap_length(new_string, s_, min_length=overlap_dict[merge_id2, id_]))
                                     )
            new_overlaps_list.append((id_, new_id,
                                      find_overlap_length(s_, new_string, min_length=overlap_dict[id_, merge_id1]))
                                     )

        # add new overlaps to the storage
        for item in new_overlaps_list:
            overlap_dict[(item[0], item[1])] = item[2]
            heap.push(item)

        # Add new string to the string set
        strings_dict[new_id] = new_string

    assert len(strings_dict) == 1
    return list(strings_dict.values())[0]


def greedy_scs_matrix(strings: List[str]):
    """
    Greedy shortest common superstring algorithm.
    (Correct solution NOT guaranteed, but takes reasonable time).
    """

    strings = list(set(strings))

    strings_dict = get_strings_with_id_dict(strings)  # str_id: str
    overlap_matrix = np.full((len(strings), len(strings)), fill_value=-1, dtype=int)

    # Initial pairwise overlap calculation
    for (id1, s1), (id2, s2) in tqdm(itertools.permutations(strings_dict.items(), r=2),
                                     desc='Greedy SCS. Initialization.',
                                     total=len(strings) ** 2 - len(strings)):
        overlap_len = find_overlap_length(s1, s2)
        overlap_matrix[id1, id2] = overlap_len

    # Find two strings with biggest overlap and merge them. Repeat.
    # At each iteration number of strings in strings_dict decreases by 1, so, (len(strings) - 1) iterations.

    for _ in tqdm(range(len(strings) - 1),
                  desc='Greesy SCS. String merging.'):
        len_strings = len(strings_dict)
        # Find max overlap and corresponding string IDs.
        merge_id1, merge_id2 = np.unravel_index(overlap_matrix.argmax(), overlap_matrix.shape)
        max_overlap = overlap_matrix[merge_id1, merge_id2]

        new_string = strings_dict[merge_id1] + strings_dict[merge_id2][max_overlap:]

        print(strings_dict[merge_id1], strings_dict[merge_id2], max_overlap)

        # calculate overlaps between new string and the old ones
        new_overlaps_list1 = np.full(len_strings - 1, -1, dtype=int)
        new_overlaps_list2 = np.full(len_strings - 2, -1, dtype=int)

        j = 0
        for (id_, s_) in strings_dict.items():
            if id_ in (merge_id1, merge_id2):
                continue
            new_overlaps_list1[j] = find_overlap_length(new_string, s_, min_length=overlap_matrix[merge_id2, id_])
            new_overlaps_list2[j] = find_overlap_length(s_, new_string, min_length=overlap_matrix[id_, merge_id1])
            j += 1

        # Delete two strings that were merged
        del strings_dict[merge_id1]
        del strings_dict[merge_id2]
        # rename the indexes/IDs
        for j in range(min(merge_id1, merge_id2) + 1, max(merge_id1, merge_id2)):
            strings_dict[j - 1] = strings_dict[j]
        for j in range(max(merge_id1, merge_id2) + 1, len_strings):
            strings_dict[j - 2] = strings_dict[j]
        for k in [len_strings - 1, len_strings - 2]:
            if k in strings_dict:
                del strings_dict[k]

        # Delete overlap history of merged strings
        overlap_matrix = remove_rows_cols(overlap_matrix, [merge_id1, merge_id2])

        # add new overlaps
        overlap_matrix = add_row_col_to_end(overlap_matrix, new_overlaps_list1, new_overlaps_list2)

        # Add new string to the string set
        strings_dict[len(strings_dict)] = new_string

    assert len(strings_dict) == 1
    return list(strings_dict.values())[0]
