# Custom containers


from UserDict import UserDict


# from http://code.activestate.com/recipes
class odict(UserDict):
    def __init__(self, dict = None):
        self._keys = []
        UserDict.__init__(self, dict)

    def __repr__(self):
        totalString = ""
        for key in self.keys():
            totalString += str(key) + ":" + str(self[key]) + "\n"
        return totalString

    def __delitem__(self, key):
        UserDict.__delitem__(self, key)
        self._keys.remove(key)

    def __setitem__(self, key, item):
        UserDict.__setitem__(self, key, item)
        if key not in self._keys: self._keys.append(key)

    def clear(self):
        UserDict.clear(self)
        self._keys = []

    def copy(self):
        dict = UserDict.copy(self)
        dict._keys = self._keys[:]
        return dict

    def items(self):
        return zip(self._keys, self.values())

    def keys(self):
        return self._keys

    def popitem(self):
        try:
            key = self._keys[-1]
        except IndexError:
            raise KeyError('dictionary is empty')

        val = self[key]
        del self[key]

        return (key, val)

    def setdefault(self, key, failobj = None):
        UserDict.setdefault(self, key, failobj)
        if key not in self._keys: self._keys.append(key)

    def update(self, dict):
        UserDict.update(self, dict)
        for key in dict.keys():
            if key not in self._keys: self._keys.append(key)

    def values(self):
        return map(self.get, self._keys)


class OrderedDictionaryFixedKeyList(odict):
    def __init__(self, keyList):
        odict.__init__(self)
        for key in keyList:
            odict.__setitem__(self, key, None)
        
    def __setitem__(self, key, item):
        if key not in self._keys:
            raise KeyError, "The key %s does not exist and OrderedDictionaryFixedKeyList does not allow adding a key with __setitem__." % key
        else:
            UserDict.__setitem__(self, key, item)
