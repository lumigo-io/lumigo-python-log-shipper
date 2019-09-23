from typing import List


def split_to_chunks(list_to_split: list, chunk_size: int) -> List[list]:
    def chunk(l, n):
        for i in range(0, len(l), n):
            yield l[i : i + n]  # noqa

    number_of_chunks = max(chunk_size, 1)
    result = list(chunk(list_to_split, number_of_chunks))
    return result
