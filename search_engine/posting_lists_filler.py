import ast
import linked_list_classes
import time


def persian_sort_key(t):
    return [ord(c) for c in list(t[0])]


def postings_lists_builder():
    f = open("../tokenizer/tokens.txt", "r")
    lines = f.readlines()
    posting_lists = linked_list_classes.PostingLists()
    all_tokens = []
    doc_counter = 0
    for line in lines:
        if doc_counter % 1000 == 0:
            print("pending doc number " + str(doc_counter))
        doc_counter += 1
        all_tokens += ast.literal_eval(line)
        # all_tokens = sorted(all_tokens, key=persian_sort_key)
    print("sort pending...")
    all_tokens = sorted(all_tokens, key=persian_sort_key)
    counter = 0
    tokens_length = str(len(all_tokens))
    start_time = time.time()
    last_counter = 0
    speed = 0
    for token in all_tokens:
        if counter % 250000 == 0:
            print("creating postings list step " + str(counter) + "/" + tokens_length, speed, "token per second")
        counter += 1
        if time.time() - start_time > 2:
            speed = (counter - last_counter) // (time.time() - start_time)
            start_time = time.time()
            last_counter = counter
        splitted = token[1].split("-")
        posting_lists.add_doc(token[0], splitted[0], splitted[1])
    # x = posting_lists.tokens.index("محمد")
    # print(posting_lists.freq[x])
    # print(posting_lists.tokens[0])
    vector_sizes = []
    doc_size = []
    for i in range(20000):
        vector_sizes.append(0)
        doc_size.append(0)
    print("Calculating Tf-Idf...")
    counter = 0
    for i in posting_lists.posting_list:
        cur = i.first_doc
        # print(i.word)
        while not cur.doc_id == -1:
            doc_size[cur.doc_id] += 1
            tfidf_result = cur.set_tf_idf(doc_counter, i.frq)
            # print(tfidf_result)
            vector_sizes[cur.doc_id] += (tfidf_result*tfidf_result)
            cur = cur.next
            if counter % 250000 == 0:
                print(counter, "tokens calculated...")
            counter += 1
    print('all', counter, 'tokens are done')
    print("docs:", len(posting_lists.tokens))
    with open('plists', 'a') as f:
        for i in posting_lists.posting_list:
            cur = i.first_doc
            # print(i)
            while not cur.doc_id == -1:
                f.write(i.word + str(cur.positions) + '\n')
                cur = cur.next
    return [posting_lists, doc_counter + 1, vector_sizes, doc_size]
