import pickle
'''
AUTHOR: Cameron Cunningham
DESCRIPTION: tests a naive bayes classifier produced by bayes_train.py. 
INPUTS: none, but requires test.p, logprior.p, loglikelihood.p, and vocab.p
to be in the same folder as bayes_test.py
OUTPUTS: none
'''

test = pickle.load(open("test.p", "rb"))
logprior = pickle.load(open("logprior.p", "rb"))
loglikelihood = pickle.load(open("loglikelihood.p", "rb"))
vocab = pickle.load(open("vocab.p", "rb"))

def classify(doc):
    sums = {}
    for c in logprior:
        sums[c] = logprior[c]
        for word in doc:
            if word in vocab:
                sums[c] += loglikelihood[word][c]
    if sums['true'] < sums['fake']:
        return 'fake'
    elif sums['true'] > sums['fake']:
        return 'true'
    else:
        # if this ever happens I will eat my hat
        return "ERROR: both classes equal"

if __name__ == "__main__":
    true_count = 0
    for doc in test['true']:
        if classify(doc) == 'true':
            true_count += 1
    print(f"accuracy of true docs = {true_count / len(test['true'])}")

    fake_count = 0
    for doc in test['fake']:
        if classify(doc) == 'fake':
            fake_count += 1
    print(f"accuracy of fake docs = {fake_count / len(test['fake'])}")
    print(f"total accuracy: {(true_count + fake_count) / (len(test['fake']) + len(test['true']))}")



