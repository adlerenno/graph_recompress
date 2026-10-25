from collections.abc import MutableMapping


class ListDict(MutableMapping):
    def __init__(self, data={}):
        self._mapping = {}
        self.update(data)

    def __getitem__(self, key):
        return self._mapping.__getitem__(key)

    def __delitem__(self, key):
        if key in self._mapping:
            return self._mapping.__delitem__(key)
        else:
            key, value = key
            l: list = self._mapping.__getitem__(key)
            del l[l.index(value)]

    def __setitem__(self, key, value):
        if key not in self._mapping:
            kl = list()
            self._mapping[key] = kl
        else:
            kl = self._mapping[key]
        kl.append(value)

    def __iter__(self):
        return self._mapping.__iter__()

    def __contains__(self, item):
        return self._mapping.__contains__(item)

    def __len__(self):
        return self._mapping.__len__()

    def __repr__(self):
        return self._mapping.__repr__()

    def extends(self, other):
        for key in other.keys():
            for value in other[key]:
                self[key] = value
