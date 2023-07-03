from __future__ import unicode_literals
import file_reader
import tokenizer
from hazm import *

address = "../../IR_data_news_5k.json"
json_file = file_reader.read_file(address)
f = open("./stop_words.txt", 'r')
stop_words = f.readlines()
f.close()
f = open("./punctuations.txt", 'r')
punctuations = f.readlines()
f.close()
normalizer = Normalizer()
stemmer = Stemmer()
lemmatizer = Lemmatizer()
arr = []
for i in range(1000):
    arr.append(0)
stop_words = []
for i in json_file:
    print("pending file number " + i)
    tokens, stop_words, arr2 = tokenizer.normalizing_sentences(json_file[i]['content'], i, normalizer, stemmer, lemmatizer)
    for p in range(len(arr2)):
        arr[p] += arr2[p]
    with open('tokens.txt', 'a') as f:
        f.write(str(tokens) + '\n')
results_copy = arr[:]
results_copy = sorted(results_copy, reverse=True)
for i in range(len(results_copy)):
    print(stop_words[arr.index(results_copy[i])], results_copy[i])
