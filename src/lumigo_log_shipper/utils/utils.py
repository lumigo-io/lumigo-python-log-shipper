from typing import List


def split_to_chunks(list_to_split: list, chunk_size: int) -> List[list]:
    def chunk(l, n):
        for i in range(0, len(l), n):
            yield l[i : i + n]  # noqa

    chunk_size = max(chunk_size, 1)
    result = list(chunk(list_to_split, chunk_size))
    return result
