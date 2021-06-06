import os
import pickle
from pgn_parser import *
from embeddings import *
from classifier import *

games, results = parser("data/lichess/lichess_db_standard_rated_2017-02.pgn")
G, all_results = create_metaposition_network(games, results)
embeddings = metaposition_node2vec(G, all_results)

# with open(os.path.join("output", "embeddings"), 'rb') as file:
#     embeddings = pickle.load(file)

X, y = parse_embeddings(embeddings)

clf = logistic_regression()
clf.train(X, y)
print(clf.predict(X))
print(clf.get_score(X, y))
# cross_validation(clf, X, y, k=2, output=True)
