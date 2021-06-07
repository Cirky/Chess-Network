import time

from node2vec import Node2Vec
import pickle
import os
import numpy as np


def metaposition_node2vec(G, results, write=False, filename="embeddings", dimensions=300, walk_length=2, num_walks=150, color_separated=False):
    node2vec = Node2Vec(G, dimensions=dimensions, walk_length=walk_length, num_walks=num_walks, workers=1, p=1, q=1,
                        seed=69)

    start = time.time()
    model = node2vec.fit()
    print("Fitting took:", time.time() - start)

    embeddings = {}
    for board_num in range(len(results)):
        if not color_separated:
            embeddings[board_num] = model.wv[str(board_num)]
        else:
            embeddings[board_num] = np.concatenate((model.wv[str(board_num) + "W"], model.wv[str(board_num) + "B"]))
        embeddings["result_" + str(board_num)] = results[board_num]

    if write:
        with open(os.path.join("output", filename), 'wb') as file:
            pickle.dump(embeddings, file)
    return embeddings

