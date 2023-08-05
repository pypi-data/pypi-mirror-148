class Example(dict):

    def __repr__(self):
        order = sorted(list(self.keys()))
        return '{}({})'.format(self.__class__.__name__, ', '.join(order))
