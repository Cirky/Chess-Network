import os
import pickle
from pgn_parser import *
from embeddings import *
from classifier import *
import sys
# print(sys.getrecursionlimit())
# sys.setrecursionlimit(10000)
# print(sys.getrecursionlimit())
#
from classic_evaluations import *
# s = time.time()
# games, results = parser("data/lichess/lichess_db_standard_rated_2017-02.pgn", elo=2600)
# print("Igre smo sprocesirali v:", time.time() - s, " in imamo jih:", len(games))
# save_game_data(games, results, "games_2600")

games, results = load_game_data("games_2600")
G, all_results = create_metaposition_network(games[:500], results, directed=True, advanced=True)


embeddings = metaposition_node2vec(G, all_results)

# with open(os.path.join("output", "embeddings"), 'rb') as file:
#     embeddings = pickle.load(file)

X, y = parse_embeddings(embeddings)

clf = logistic_regression()
#clf.train(X, y)
#print(clf.predict(X))
#print(clf.get_score(X, y))
print(clf.cross_validate(X, y, k=5, output=True))
