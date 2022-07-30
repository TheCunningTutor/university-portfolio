import pickle
import nltk
from nltk.corpus import stopwords
from math import log
'''
AUTHOR: Cameron Cunningham
DESCRIPTION: trains a naive bayes classifier to classify documents as fake
or real news
INPUTS: none, but requires train.p, and vocab to be in the same folder as
bayes_train.py
OUTPUTS: writes two files: loglikelihood.p and logprior.p
'''

print("loading data...")
train = pickle.load(open("train.p", "rb"))
vocab = pickle.load(open("vocab.p", "rb"))
docs = len(train['true']) + len(train['fake'])
loglikelihood = {}
logprior = {}

for c in train:
    print(f"training for class {c}...")
    logprior[c] = log(len(train[c])/docs)
    class_sum = 0
    for word in vocab:
        class_sum += vocab[word][c] + 1
    for word in vocab:
        if word not in loglikelihood:
            loglikelihood[word] = {'true': 0, 'fake': 0}
        count = vocab[word][c]
        loglikelihood[word][c] = log((count + 1) / (class_sum))

pickle.dump(loglikelihood, open("loglikelihood.p", "wb"))
pickle.dump(logprior, open("logprior.p", "wb"))

