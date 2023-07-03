import math

import posting_lists_filler as plist_builder
import linked_list_classes as ll
import json

from hazm import *

lemmatizer = Lemmatizer()
stemmer = Stemmer()

linked_list = ll.LinkedList()
res = plist_builder.postings_lists_builder()
plist = res[0]
doc_counter = res[1]
vector_sizes = res[2]


# In[10]:
def read_file(url):
    f = open(url)
    data = json.load(f)
    return data


def print_array(doc_id, arr, topic):
    print("doc id:", doc_id, 'title:', topic)
    for i in arr:
        print(i, end=" ")
    print()


address = "../../IR_data_news_5k.json"
json_file = read_file(address)
# normalizer = Normalizer()
print("welcome to abol's search engine (Second Edition):")


def cos_similarity(word_nodes, i):
    summation = 0
    for j in word_nodes:
        cur = j.first_doc
        while not cur.doc_id == -1:
            if cur.doc_id == i:
                summation += cur.tf_idf
                break
            else:
                cur = cur.next
    return summation / (math.sqrt(vector_sizes[i])+1)


while True:
    inp = input("enter your search query:")
    print(inp)
    unprocessed = inp.split(" ")
    arr = []
    for i in unprocessed:
        arr.append(lemmatizer.lemmatize(i))
    word_nodes = []
    for i in range(len(arr)):
        if arr[i] in plist.tokens:
            word_nodes.append(plist.posting_list[plist.tokens.index(arr[i])])
        else:
            print("we couldn't find word " + arr[i] + " in our docs!!!")
    results = []
    for i in range(20000):
        results.append(cos_similarity(word_nodes, i))
    results_copy = results[:]
    results_copy = sorted(results_copy, reverse=True)[:10]
    # print(results.index(best))
    printed = []
    for i in results_copy:
        j = results.index(i)
        content = word_tokenize(json_file[str(j)]['content'])
        topic = json_file[str(j)]['title']
        for k in word_nodes:
            cur = k.first_doc
            while True:
                if cur.doc_id == -1:
                    break
                if cur.doc_id == j:
                    for x in cur.positions:
                        if j not in printed:
                            print_array(j, content[x - 5:x + 5], topic)
                            printed.append(j)
                cur = cur.next