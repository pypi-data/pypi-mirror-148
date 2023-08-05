import torch
from torch import nn
from torch.nn import functional as F
from vnlp.nn.functional import mask_invalid_scores


def expand_sentinel(sentinel, seq):
    batch_size, _, dfeat = seq.size()
    return sentinel.unsqueeze(0).unsqueeze(0).expand(batch_size, 1, dfeat)


class Pointer(nn.Module):
    """
    dot product pointer.
    """

    def forward(self, seq, lens, cond):
        scores = seq.bmm(cond.unsqueeze(2)).squeeze(2)
        return mask_invalid_scores(scores, lens)


class Attention(Pointer):
    """
    attend over the sequences `seq` using the condition `cond`.
    """

    def __init__(self, dhid):
        super().__init__()
        self.sentinel = nn.Parameter(torch.Tensor(dhid))
        nn.init.uniform_(self.sentinel, -0.1, 0.1)

    @classmethod
    def mix(cls, seq, raw_scores):
        scores = F.softmax(raw_scores, dim=1)
        return scores.unsqueeze(2).expand_as(seq).mul(seq).sum(1)

    def forward(self, seq, lens, cond):
        seq = torch.cat([expand_sentinel(self.sentinel, seq), seq], dim=1)
        raw_scores = super().forward(seq, lens+1, cond)
        return self.mix(seq, raw_scores)


class SelfAttention(nn.Module):
    """
    scores each element of the sequence with a linear layer and uses the normalized scores to compute a context over the sequence.
    """

    def __init__(self, dhid, scorer=None):
        super().__init__()
        self.scorer = scorer or nn.Linear(dhid, 1)
        self.sentinel = nn.Parameter(torch.Tensor(dhid))
        nn.init.uniform_(self.sentinel, -0.1, 0.1)

    def forward(self, inp, lens):
        inp = torch.cat([expand_sentinel(self.sentinel, inp), inp], dim=1)
        batch_size, seq_len, d_feat = inp.size()
        scores = self.scorer(inp.contiguous().view(-1, d_feat)).view(batch_size, seq_len)
        raw_scores = mask_invalid_scores(scores, lens+1)
        scores = F.softmax(raw_scores, dim=1)
        context = scores.unsqueeze(2).expand_as(inp).mul(inp).sum(1)
        return context


class Coattention(nn.Module):
    """
    one layer of coattention.
    """

    def __init__(self, dhid):
        super().__init__()
        self.trans = nn.Linear(dhid, dhid)
        self.q_sentinel = nn.Parameter(torch.Tensor(dhid))
        self.d_sentinel = nn.Parameter(torch.Tensor(dhid))
        nn.init.uniform_(self.q_sentinel, -0.1, 0.1)
        nn.init.uniform_(self.d_sentinel, -0.1, 0.1)

    def forward(self, q, q_len, d, d_len):
        batch_size, _, dfeat = q.size()
        q = torch.cat([expand_sentinel(self.q_sentinel, q), q], dim=1)
        d = torch.cat([expand_sentinel(self.d_sentinel, d), d], dim=1)
        q = self.trans(q)
        a = q.bmm(d.transpose(1, 2))
        aq = F.softmax(mask_invalid_scores(a, q_len+1), dim=1)
        ad = F.softmax(mask_invalid_scores(a.transpose(1, 2), d_len+1), dim=1)
        sd = q.transpose(1, 2).bmm(aq)
        sq = d.transpose(1, 2).bmm(ad)
        cd = sq.bmm(aq)
        cd, sq, sd = cd.transpose(1, 2), sq.transpose(1, 2), sd.transpose(1, 2)
        return cd[:, 1:], sq[:, 1:], sd[:, 1:]
