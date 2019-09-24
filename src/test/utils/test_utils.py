from src.lumigo_log_shipper.utils.utils import split_to_chunks


def test_split_to_chunks_empty_list():
    lst = []
    chunks = split_to_chunks(lst, 2)
    assert chunks == []


def test_split_to_chunks_simple_flow():
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    chunks = split_to_chunks(lst, 2)
    assert chunks == [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]


def test_split_to_chunks_min_value():
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    chunks = split_to_chunks(lst, 0)
    assert chunks == [[1], [2], [3], [4], [5], [6], [7], [8], [9], [10]]


def test_split_to_chunks_not_equal_chunks():
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    chunks = split_to_chunks(lst, 3)
    assert chunks == [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10]]


def test_split_to_chunks_smaller_then_chunk_size():
    lst = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    chunks = split_to_chunks(lst, 11)
    assert chunks == [lst]
