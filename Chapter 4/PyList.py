

class PyList:
    def __init__(self, contents=[], size=10):
        """
        contents: allows to create a list with variables initial contents
        initial_size: allows the progrmmer to pick a size for the internal size of the list.
        """

        for element in contents:
            self.append(element)

    