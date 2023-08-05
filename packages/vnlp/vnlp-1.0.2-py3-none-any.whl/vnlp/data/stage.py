import revtok
from vocab import Vocab


class Stage:

    def __call__(self, ann):
        raise NotImplementedError()


class Tokenize(Stage):

    @classmethod
    def tokenize(cls, sent):
        return revtok.tokenize(sent)

    @classmethod
    def detokenize(cls, tokens):
        return revtok.detokenize(tokens)

    def __call__(self, ann):
        ann['tokens'] = self.tokenize(ann['orig'])


class Numericalize(Stage):

    def __init__(self, vocab=None, append_ends=True, train=True, lower=None):
        self.vocab = vocab or Vocab()
        self.append_ends = append_ends
        self.train = train
        assert lower in {'all', 'first', None}
        self.lower = lower

    def __call__(self, ann):
        tokens = []
        for i, t in enumerate(ann['tokens']):
            t = t.strip()
            if self.lower == 'first' and i == 0 and (len(t) == 1 or t.upper() != t):
                t = t.lower()
            elif self.lower == 'all':
                t = t.lower()
            tokens.append(t)
        if self.append_ends:
            tokens = ['<S>'] + tokens + ['</S>']
        ann['num'] = self.vocab.word2index(tokens, train=self.train)
