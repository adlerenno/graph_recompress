from evaluate.timetest.average import average_timing


class Bitvector:
    """
    Saves a 'list' True or False values.
    length: size.
    rank: how many Trues are before the given position.
    """

    def __init__(self, size: int):
        self._bits = [False] * size

    def __setitem__(self, key: int, value: bool):
        self._bits[key] = value

    def __getitem__(self, key: int) -> bool:
        return self._bits[key]

    def __str__(self):
        return ''.join(map(lambda x: str(1) if x else str(0), self._bits))

    __repr__ = __str__

    def all_false(self) -> bool:
        """Sets all bool values to False."""
        for i in range(len(self._bits)):
            self._bits[i] = False

    def are_all_true(self) -> bool:
        """Checks whether all bits are set to True."""
        return all(self._bits)

    def get_max_rank(self) -> int:
        """Returns the number of Trues within the bits. Equal to rank(len(_bits))."""
        return sum(self._bits)

    @average_timing
    def rank(self, index: int) -> int:
        """Answers: How many Trues are there are before the index."""
        r = 0
        for i in range(index):
            if self[i]:
                r += 1
        return r
