import nltk
from bayes_test import classify
import sys 
'''
AUTHOR: Cameron Cunningham
DESCRIPTION: classifies one document
INPUTS: document to be classified, as a text file
OUTPUTS: none
'''

doc = []
with open(sys.argv[1], "r") as article:
    for line in article:
        for token in nltk.word_tokenize(line):
            doc.append(token)

print(classify(doc))
