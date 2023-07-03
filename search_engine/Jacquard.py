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
doc_size = res[3]


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


address = "../../IR_data_news_12k.json"
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
    return summation / vector_sizes[i]


while True:
    inp = input("enter your search query:")
    print(inp)
    unprocessed = inp.split(" ")
    arr = unprocessed
    doc_frq = []
    for i in range(20000):
        doc_frq.append(0)
    # find each words node in postings lists
    word_nodes = []
    for i in range(len(arr)):
        if arr[i] in plist.tokens:
            word_nodes.append(plist.posting_list[plist.tokens.index(lemmatizer.lemmatize(arr[i]))])
        else:
            print("we couldn't find word " + arr[i] + " in our docs!!!")

    # find not include nodes in postings lists

    if len(word_nodes) > 0:
        linked_list = word_nodes[0]

    for i in word_nodes:
        cur = i.first_doc
        added_docs = []
        while not cur.doc_id == -1:
            if cur.doc_id not in added_docs:
                added_docs.append(cur.doc_id)
                doc_frq[cur.doc_id] += 1
            cur = cur.next
    counter = 0
    results = []
    for i in range(20000):
        results.append(0)
    for i in range(doc_counter):
        results[i] = doc_frq[i] / (doc_size[i] + len(word_nodes) - doc_frq[i])
    results_copy = results[:]
    results_copy = sorted(results_copy, reverse=True)[:5]
    # print(results.index(best))
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
                        print_array(j, content[x - 5:x + 5], topic)
                cur = cur.next
