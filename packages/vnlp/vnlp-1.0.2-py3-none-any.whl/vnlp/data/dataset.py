import os
import logging
import torch


class BaseDataset:

    def __init__(self, splits=None):
        self.splits = splits or {}

    def debug(self, size=5):
        if size:
            for name, split in self.splits.items():
                self.splits[name] = split.__class__(split[:size])

    def __repr__(self):
        order = sorted(list(self.splits.keys()))
        return '{}({})'.format(self.__class__.__name__, ', '.join(['{}: {}'.format(s, repr(self.splits[s])) for s in order]))

    def save(self, fname):
        torch.save(self, fname)

    @classmethod
    def load(cls, fname):
        return torch.load(fname)

    @classmethod
    def download(cls):
        raise NotImplementedError()

    @classmethod
    def pull(cls, fname, cache=None, debug=0):
        cache = cache or os.path.dirname(fname)
        if not os.path.isfile(fname):
            cls.download(cache).save(fname)
        data = cls.load(fname)
        if debug:
            data.debug(debug)
        return data
