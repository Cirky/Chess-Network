import time

from node2vec import Node2Vec
import pickle
import os

def metaposition_node2vec(G, results, write=False, filename="embeddings"):
    node2vec = Node2Vec(G, dimensions=200, walk_length=2, num_walks=150, workers=1, p=1, q=1)

    start = time.time()
    model = node2vec.fit(window=10, min_count=1, batch_words=4)
    print("Fitting took:", time.time() - start)

    embeddings = {}
    for board_num in range(len(results)):
        embeddings[board_num] = model.wv[str(board_num)]
        embeddings["result_" + str(board_num)] = results[board_num]

    if write:
        with open(os.path.join("output", filename), 'wb') as file:
            pickle.dump(embeddings, file)
    return embeddings
