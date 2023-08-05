import torch
import os
import re
import logging
import pprint
import json
import numpy as np
from argparse import Namespace
from torch import nn
from torch.nn import functional as F
from collections import defaultdict
from importlib import import_module
from ..utils.logging import get_logger
from ..exp.tracker import Tracker
from ..exp.grapher import Grapher


class Model:
    """
    args has:
    - gpu
    - exp_root
    - module
    - name
    - epoch
    - early_stop
    """

    def __init__(self, args, module):
        self.args = args
        self.device = torch.device('cpu')
        self.to(args.gpus)
        self.module = module

    def to(self, gpus):
        if gpus:
            self.device = torch.device('cuda:{}'.format(gpus[0]))
            if len(gpus) == 1:
                self.module = self.module.to(self.device)
            else:
                self.module = nn.DataParallel(self.module, device_ids=device)

    @property
    def module_instance(self):
        return self.module.module if isinstance(self.module, nn.DataParallel) else self.module

    @property
    def dout(self):
        return os.path.join(self.args.exp_root, self.args.module, self.args.name)

    @classmethod
    def from_module(cls, module, args, *vargs, module_root='modules', **kwargs):
        M = import_module('{}.{}'.format(module_root, module)).Module
        return cls(args, M(args, *vargs, **kwargs))

    def run_train(self, train, dev, optimizer=None, tracker=None, plot_module=False, logging_level=logging.INFO, verbose=True):
        if not os.path.isdir(self.dout):
            os.makedirs(self.dout)
        logger = get_logger('trainer', fout=os.path.join(self.dout, 'train.log'), level=logging_level)
        logger.info('Starting train with args:\n{}'.format(pprint.pformat(self.args)))
        tracker = tracker or Tracker()
        grapher = Grapher(self.dout)

        tracker.save_data(vars(self.args), 'config.json')

        if optimizer is None:
            optimizer = torch.optim.Adam(self.module.parameters())
        iteration = tracker.iteration
        for epoch in range(tracker.epoch, self.args.epoch):
            logger.info('Starting epoch {}'.format(epoch))
            loss = 0
            self.module.train()
            for batch in train.batch(self.args.batch, shuffle=True, verbose=verbose):
                optimizer.zero_grad()
                feat = self.module_instance.featurize(batch, device=self.device)
                if not grapher.plotted_module and plot_module:
                    grapher.plot_module(self.module_instance, feat)
                out = self.module(*feat)
                batch_loss = self.module_instance.compute_loss(out, batch)
                batch_loss.backward()
                optimizer.step()
                loss += batch_loss.item()
                iteration += len(batch)
            train_preds = self.run_pred(train)
            dev_preds = self.run_pred(dev)
            train_metrics = train.compute_metrics(train_preds)
            train_metrics['loss'] = loss
            metrics = {
                'iteration': iteration,
                'epoch': epoch,
                'train': train_metrics,
                'dev': dev.compute_metrics(dev_preds),
            }

            self.module_instance.graph(grapher, metrics, iteration)

            if tracker.is_best(metrics, self.args.early_stop, iteration=iteration, epoch=epoch):
                logging.info('Found new best! Saving to {}'.format(self.dout))
                tracker.save_checkpoint(self.dout, metrics, self.args.early_stop, self.module_instance, optimizer, self.args, link_best=True)
                tracker.clean_old_checkpoints(self.dout, self.args.early_stop)
                tracker.save_data(train_preds, os.path.join(self.dout, 'train.preds.json'))
                tracker.save_data(dev_preds, os.path.join(self.dout, 'dev.preds.json'))
                metrics['best'] = metrics['dev']
            logger.info('\n' + pprint.pformat(metrics))
            tracker.save(os.path.join(self.dout, 'tracker.json'))
        state = tracker.load_best_checkpoint(self.dout, self.args.early_stop)
        self.module_instance.load_state_dict(state['module'])
        optimizer.load_state_dict(state['optimizer'])

    def run_pred(self, dev, verbose=False):
        self.module.eval()
        preds = []
        for batch in dev.batch(self.args.batch, shuffle=False, verbose=verbose):
            out = self.module(*self.module_instance.featurize(batch, device=self.device))
            preds += self.module_instance.extract_preds(out, batch)
        return preds
