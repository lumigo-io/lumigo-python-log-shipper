from src.utils.utils import split_to_chunks


def test_split_to_chunks_simple_flow():
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    chunks = split_to_chunks(lst, 2)
    assert chunks == [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]


def test_split_to_chunks_min_value():
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    chunks = split_to_chunks(lst, 0)
    assert chunks == [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]
