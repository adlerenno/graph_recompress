from collections.abc import MutableMapping
from functools import reduce


class CountDict(MutableMapping):
    def __init__(self, data={}):
        self._mapping = {}
        self.update(data)

    def __getitem__(self, key):
        if key in self._mapping:
            return self._mapping.__getitem__(key)
        else:
            return 0

    def __delitem__(self, key):
        return self._mapping.__delitem__(key)

    def __setitem__(self, key, value):
        if value <= 0:
            if key in self._mapping:
                del self[key]
            return False
        else:
            return self._mapping.__setitem__(key, value)

    def __iter__(self):
        return self._mapping.__iter__()

    def __contains__(self, item):
        return self._mapping.__contains__(item)

    def __len__(self):
        return self._mapping.__len__()

    def __repr__(self):
        return self._mapping.__repr__()

    def get_max(self):
        return reduce(lambda x, y: x if self[x] >= self[y] else y, self.keys()) \
            if len(self.keys()) > 0 else None

    def get_min(self):
        return reduce(lambda x, y: x if self[x] <= self[y] else y, self.keys()) \
            if len(self.keys()) > 0 else None


class AutoAddCountDict(MutableMapping):
    def __init__(self):
        self._mapping = {}

    def __getitem__(self, key):
        if key not in self._mapping:
            self._mapping[key] = CountDict()
        return self._mapping.__getitem__(key)

    def __delitem__(self, key):
        return self._mapping.__delitem__(key)

    def __setitem__(self, key, value):
        return self._mapping.__setitem__(key, value)

    def __iter__(self):
        return self._mapping.__iter__()

    def __len__(self):
        return self._mapping.__len__()

    def __repr__(self):
        return self._mapping.__repr__()