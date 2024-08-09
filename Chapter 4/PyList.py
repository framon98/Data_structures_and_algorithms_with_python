

class PyList:
    def __init__(self, contents=[], size=10):
        """
        contents: allows to create a list with variables initial contents
        initial_size: allows the progrmmer to pick a size for the internal size of the list.
        """
        self.items = [None] * size
        self.numItems = 0
        self.size = size

        for element in contents:
            self.append(element)

    def __getitem__(self, index):
        if index >= 0 and index < self.numItems:
            return self.items(index)

        raise IndexError("PyList index out of range")

    def __setitem__(self, index, val):
        if index >= 0 and index < self.numItems:
            self.items[index] = val
            return

        raise IndexError("PyList assignment index out of range")

    def __add__(self, other):
        result = PyList(size=self.numItems + other.numItems)

        for idxi in range(self.numItems):
            result.append(self.items[idxi])

        for idxi in range(other.numItems):
            result.append(other.items[idxi])

        return result