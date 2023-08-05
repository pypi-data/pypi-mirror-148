from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter


def get_default_parser():
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument('module', help='name of module')
    parser.add_argument('--name', help='name of experiment', default='default')
    parser.add_argument('--module_root', help='where to select modules from', default='modules')
    parser.add_argument('--data_root', help='where to store dataset', default='data')
    parser.add_argument('--exp_root', help='where to store experiments', default='exp')
    parser.add_argument('--batch', help='examples per batch', type=int, default=64)
    parser.add_argument('--epoch', help='number of epochs to run', type=int, default=50)
    parser.add_argument('--demb', help='word embedding size', type=int, default=400)
    parser.add_argument('--debug', help='only load this many examples for debug. 0 means off.', type=int, default=0)
    parser.add_argument('--gpus', help='gpus to use', nargs='*', default=[])
    return parser
