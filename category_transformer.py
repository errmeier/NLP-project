import torch
import sys
import argparse

from transformer import *
from neural_classifier import *

def read_mono(filename):
    """Read sentences from the file named by 'filename.' """
    data = []
    for line in open(filename):
        words = ['<BOS>'] + line.split() + ['<EOS>']
        data.append(words)
    return data

if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=str, help='test data to translate')
    parser.add_argument('-o', '--outfile', type=str, help='write translations to file')
    args = parser.parse_args()

    c = torch.load('cat.model')
    m = [torch.load('0.model'), torch.load('1.model'), torch.load('2.model')]
     
    with open(args.outfile, 'w') as outfile:
        for words in read_mono(args.infile):
            cat = int(c.predict(words))
            translation = m[cat].translate(words)
            print(' '.join(translation), file=outfile)
