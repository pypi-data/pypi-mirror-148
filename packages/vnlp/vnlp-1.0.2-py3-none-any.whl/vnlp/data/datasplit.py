import numpy as np
from tqdm import tqdm


class DataSplit(list):

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, len(self))

    def batch(self, batch_size, shuffle=False, verbose=True):
        copy = self[:]
        if shuffle:
            np.random.shuffle(copy)
        iterator = range(0, len(copy), batch_size)
        iterator = tqdm(iterator) if verbose else iterator
        for i in iterator:
            yield copy[i:i+batch_size]


class AnnotatedDataSplit(DataSplit):
    pass
