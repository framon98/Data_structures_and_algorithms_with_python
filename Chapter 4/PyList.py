

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

    #This method is hidden since it starts with two underscores. 
    # It can only be seen to the class to use
    def __makeroom(self):
        """
        Increase siez by 1/4 to make room
        Add one in case for some reason self.size is 0
        """

        newlen = (self.size // 4) + self.size + 1
        newlst = [None] * newlen
        for idxi in range(self.numItems):
            newlst[idxi] = self.items[idxi]

        self.items = newlst
        self.size = newlen

    def append(self, item):
        if self.numItems == self.size:
            self.__makeroom()

        self.items[self.numItems] = item
        self.numItems += 1

    def insert(self, idx, element):
        if self.numItems == self.size:
            self.__makeroom()

        if idx < self.numItems:
            for idxj in range(self.numItems - 1, idx - 1, -1):
                self.items[idxj + 1] = self.items[idxj]
            
            self.items[idx] = element
            self.numItems += 1
        else:
            self.append(element)

    def __delitem__(self, index):
        for idxi in range(index, self.numItems - 1):
            self.items[idxi] = self.items[idxi + 1]

        self.numItems -= 1

    def __eq__(self, other):
        if type(other) != type(self):
            return False

        if self.numItems != other.numItems:
            return False
        
        for idxi in range(self.numItems):
            if self.items[idxi] != other.items[idxi]:
                return False

        return True
    
    def __iter__(self):
        for idxi in range(self.numItems):
            yield self.items[idxi]

    def __len__(self):
        return self.numItems

    def __contains__(self, item):
        for idx in range(self.numItems):
            if self.items[idx] == item:
                return True
            
        return False
    
    def __str__(self):
        s = "["
        for idx in range(self.numItems):
            s = s + repr(self.items[idx])
            if idx < self.numItems -1:
                s = s + ", "

        s = s + "]"
        return s
    
    def __repr__(self):
        s = "PyList(["
        for idx in range(self.numItems):
            s = s + repr(self.items[idx])
            if idx < self.numItems - 1:
                s = s + ", "
        s = s + "])"
        return s