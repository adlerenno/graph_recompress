class PathEntry:
    def __init__(self, position, label):
        self.position = position
        self.label = label

    def __eq__(self, other):
        return self.position == other.position and self.label == other.label

    def __lt__(self, other):
        return self.position < other.position

    def __le__(self, other):
        return self.position <= other.position

    def __gt__(self, other):
        return self.position > other.position

    def __ge__(self, other):
        return self.position >= other.position

    def __str__(self):
        return f'({self.position}, {self.label})'

    __repr__ = __str__


class Path:
    def __init__(self, position: int, label, rest_path=None):
        if rest_path is None:
            self._path = (PathEntry(position, label),)
        else:
            rest_path: Path = rest_path
            self._path = (PathEntry(position, label),) + rest_path._path

    def __le__(self, other):
        return self._path <= other._path

    def __lt__(self, other):
        return self._path < other._path

    def __eq__(self, other):
        if type(other) is not Path:
            return False
        return self._path == other._path

    def __ge__(self, other):
        return self._path >= other._path

    def __gt__(self, other):
        return self._path > other._path

    def __len__(self):
        return len(self._path)

    def __iter__(self):
        """Returns an iterable over all but the last entry."""
        return self._path.__iter__()

    def __getitem__(self, item):
        return self._path[item]

    def add_before(self, position: int, label):
        return Path(position, label, self)

    def __str__(self):
        return self._path.__str__()

    __repr__ = __str__


def build_path(symbols, labels):
    """Only used by test-cases"""
    p = Path(symbols[-1], labels[-1])
    symbols = symbols[:-1]
    labels = labels[:-1]
    for index in range(len(symbols)-1, -1, -1):
        p = p.add_before(symbols[index], labels[index])
    return p
