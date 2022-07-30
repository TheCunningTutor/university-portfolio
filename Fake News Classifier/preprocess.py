import pandas
import pickle
import nltk
''' data from www.kaggle.com/clmentbisaillon/fake-and-real-news-dataset
AUTHOR: Cameron Cunningham
DESCRIPTION: Parses corpora of true and fake documents, additionally creating
a vocabulary, a training corpus, and a testing corpus. 
INPUTS: none
OUTPUTS: writes three files: train.p, test.p, and vocab.p
'''
print("setting up objects...")

true_data = pandas.read_csv('True.csv')
false_data = pandas.read_csv('Fake.csv')

corpus_train = {'true': [], 'fake': []}
corpus_test = {'true': [], 'fake': []}
# vocab[word][class] = # of occurances of 'word' in 'class'
vocab = {}

print("processing 'true' news documents...")
count = 0
for line in true_data['text']:
    tokens = nltk.word_tokenize(line)
    for token in tokens:
        if token not in vocab:
            vocab[token] = {'true': 0, 'fake': 0}
        vocab[token]['true'] += 1
    if count <= 200:
        corpus_test['true'].append(tokens)
    else:
        corpus_train['true'].append(tokens)
    count += 1
print(f"processed {count} 'true' documents")

print("processing 'fake' news documents...")
count = 0
for line in false_data['text']:
    tokens = nltk.word_tokenize(line)
    for token in tokens:
        if token not in vocab:
            vocab[token] = {'true': 0, 'fake': 0}
        vocab[token]['fake'] += 1
    if count <= 200:
        corpus_test['fake'].append(tokens)
    else:
        corpus_train['fake'].append(tokens)
    count += 1
print(f"processed {count} 'fake' documents")
    
pickle.dump(corpus_train, open("train.p", "wb"))
pickle.dump(corpus_test, open("test.p", "wb"))
pickle.dump(vocab, open("vocab.p", "wb"))
