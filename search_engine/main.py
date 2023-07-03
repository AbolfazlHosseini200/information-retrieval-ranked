from hazm import *

lemmatizer = Lemmatizer()
plist = postings_lists_builder()


def phrase_finder(string, plist):
    string = string.replace('"', '')
    arr = string.split(" ")
    word_nodes = []
    for i in range(len(arr)):
        if arr[i] in plist.tokens:
            word_nodes.append(plist.posting_list[plist.tokens.index(lemmatizer.lemmatize(arr[i]))])
        else:
            return None
    intersect_finder = []
    same_docs = []
    for i in range(15000):
        intersect_finder.append(0)
    for i in word_nodes:
        cur = i.first_doc
        while not cur.doc_id == -1:
            intersect_finder[cur.doc_id] += 1
            if intersect_finder[cur.doc_id] == len(word_nodes):
                same_docs.append(cur.doc_id)
            cur = cur.next
    phrase_positions = []
    cur1 = word_nodes[0].first_doc
    cur2 = word_nodes[1].first_doc
    while True:
        if cur1.doc_id == -1 or cur2.doc_id == -1:
            break
        if cur1.doc_id == cur2.doc_id and cur1.doc_id in same_docs:
            for i in cur1.positions:
                if i + 1 in cur2.positions:
                    new_tuple = (cur1.doc_id, i)
                    phrase_positions.append(new_tuple)
            cur1 = cur1.next
            cur2 = cur2.next
        elif cur1.doc_id > cur2.doc_id:
            cur2 = cur2.next
        else:
            cur1 = cur1.next
    for o in range(2, len(word_nodes)):
        cur1 = word_nodes[o].first_doc
        while True:
            if cur1.doc_id == -1:
                break
            if cur1.doc_id in same_docs:
                for k in phrase_positions[:]:
                    if cur1.doc_id == k[0]:
                        if not k[1] + o in cur1.positions:
                            phrase_positions.remove(k)
            cur1 = cur1.next
    return phrase_positions


def phrase_processor(phrases, plist):
    res = []
    for i in phrases:
        temp = phrase_finder(i, plist)
        res.append(temp)
    return res


inp = input("Query:")
unprocessed = inp.split(" ")
queries = []
arr = []
flag = False
double_quotes = []
doc_frq = []
for i in range(15000):
    doc_frq.append(0)
for i in unprocessed:
    if '"' in i and not flag:
        flag = True
        double_quotes.append(i)
        continue
    if not flag:
        queries.append(i)
    else:
        double_quotes[-1] = double_quotes[-1] + " " + i
        if '"' in i:
            flag = False
not_include = []
for i in queries:
    if i.startswith("!"):
        not_include.append(i)
    else:
        arr.append(i)
word_nodes = []
for i in range(len(arr)):
    if arr[i] in plist.tokens:
        word_nodes.append(plist.posting_list[plist.tokens.index(lemmatizer.lemmatize(arr[i]))])

not_include_results = []
for i in range(len(not_include)):
    the_word = not_include[i][1:]
    if the_word in plist.tokens:
        not_include_results.append(plist.posting_list[plist.tokens.index(lemmatizer.lemmatize(the_word))])

phrase_results = phrase_processor(double_quotes, plist)
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
for i in phrase_results:
    docs_added = []
    for j in i:
        if j[0] not in docs_added:
            docs_added.append(j[0])
            doc_frq[j[0]] += 1
for i in not_include_results:
    cur = i.first_doc
    while not cur.doc_id == -1:
        doc_frq[cur.doc_id] = 0
        cur = cur.next
counter = 0

for i in range(len(word_nodes) + len(double_quotes), 0, -1):
    for j in range(len(doc_frq)):
        if doc_frq[j] == i:
            print("doc_id:", j)
