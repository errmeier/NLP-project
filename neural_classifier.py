import torch
import argparse
import sys
import collections
import random
import copy

from layers import *

# If installed, this prints progress bars
try:
    from tqdm import tqdm
except ImportError:
    def tqdm(iterable):
        return iterable

class Vocab(collections.abc.MutableSet):
    """Set-like data structure that can change words into numbers and back."""
    def __init__(self):
        words = {'<BOS>', '<EOS>', '<UNK>'}
        self.num_to_word = list(words)    
        self.word_to_num = {word:num for num, word in enumerate(self.num_to_word)}
    def add(self, word):
        if word in self: return
        num = len(self.num_to_word)
        self.num_to_word.append(word)
        self.word_to_num[word] = num
    def discard(self, word):
        raise NotImplementedError()
    def __contains__(self, word):
        return word in self.word_to_num
    def __len__(self):
        return len(self.num_to_word)
    def __iter__(self):
        return iter(self.num_to_word)

    def numberize(self, word):
        """Convert a word into a number."""
        if word in self.word_to_num:
            return self.word_to_num[word]
        else: 
            return self.word_to_num['<UNK>']

    def denumberize(self, num):
        """Convert a number into a word."""
        return self.num_to_word[num]

def read_parallel(text_file, label_file):
    """Read data from the files text_file and label_file.'

    text_file should contain lines of text separated by newlines
    label_file should contain the corresponding labels for each line
    """
    texts = open(text_file)
    labels = open(label_file)

    data = []
    for line in zip(texts.readlines(), labels.readlines()):
        words = ['<BOS>'] + line[0].strip().split() + ['<EOS>']
        label = int(line[1].strip())
        data.append((words, label))
    return data

class NeuralClassifier(torch.nn.Module):
    
    def __init__(self, vocab, num_classes, dims):
        super().__init__()
        self.classes = num_classes
        self.vocab = vocab
        self.emb = Embedding(len(self.vocab), dims)
        self.out = SoftmaxLayer(dims, self.classes)
        self.loss = torch.nn.NLLLoss()

        self.dummy = torch.nn.Parameter(torch.empty(0))

    def predict(self, words):
        nums = torch.tensor([self.vocab.numberize(w) for w in words], device=self.dummy.device)
        encs = self.emb(nums)
        doc = torch.sum(encs, 0)
        p = self.out(doc)
        return p.argmax()

    def logprob(self, words, k):
        nums = torch.tensor([self.vocab.numberize(w) for w in words], device=self.dummy.device)
        encs = self.emb(nums)
        doc = torch.sum(encs, 0)
        p = self.out(doc)
        p = p.reshape(1, self.classes)
        return self.loss(p, torch.tensor([k]))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train_text', type=str, help='training data sentences')
    parser.add_argument('--train_label', type=str, help='training data labels')
    parser.add_argument('--dev_text', type=str, help='validation data sentences')
    parser.add_argument('--dev_label', type=str, help='validation data labels')
    parser.add_argument('--test_text', type=str, help='test data sentences')
    parser.add_argument('--test_label', type=str, help='test data labels')
    parser.add_argument('--save', type=str, help='save model to file')
    parser.add_argument('--load', type=str, help='load model from file')
    args = parser.parse_args()
    
    if args.load:
        m = torch.load(args.load)
        testdata = read_parallel(args.test_text, args.test_label)
        correct, total = 0, 0
        for words, k in testdata:
            pred_k = m.predict(words)
            if total < 10:
                print(pred_k, k)
            if pred_k == k:
                correct += 1
            else:
                print(pred_k, k)
            total += 1

        print(f'Accuracy: {correct/total}')
        sys.exit()


    traindata = read_parallel(args.train_text, args.train_label)
    devdata = read_parallel(args.dev_text, args.dev_label)
    vocab = Vocab()
    for words, k in traindata:
        vocab |= words
    m = NeuralClassifier(vocab, 3, 64)
    
    opt = torch.optim.Adam(m.parameters(), lr=0.00005)
    best_dev_loss = None
    for epoch in range(1, 15):
        random.shuffle(traindata)

        train_loss = 0
        for words, k in tqdm(traindata):
            loss = m.logprob(words, k) 
            opt.zero_grad()
            loss.backward()
            opt.step()
            train_loss += loss.item()

        dev_loss = 0
        for words, k in devdata:
            dev_loss += m.logprob(words, k).item()

        if best_dev_loss is None or dev_loss < best_dev_loss:
            best_model = copy.deepcopy(m)
            if args.save:
                torch.save(m, args.save)
            best_dev_loss = dev_loss

        print(f'[{epoch}] train_loss={train_loss} dev_loss={dev_loss}',flush=True)
        epoch += 1

    m = best_model

    testdata = read_parallel(args.test_text, args.test_label)
    correct, total = 0, 0
    for words, k in testdata:
        pred_k = m.predict(words)
        if total < 10:
            print(pred_k, k)
        if pred_k == k:
            correct += 1
        total += 1

    print(f'Accuracy: {correct/total}')
