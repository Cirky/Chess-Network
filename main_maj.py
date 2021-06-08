import os
import pickle
from pgn_parser import *
from embeddings import *
from classifier import *
from classic_evaluations import *
import sys
sys.setrecursionlimit(100000)

# s = time.time()
# games, results = parser("data/lichess/lichess_db_standard_rated_2019-10.pgn", elo=2600)
# save_game_data(games, results, "games_2600_2019")
# print("Igre smo sprocesirali v:", time.time() - s, " in imamo jih:", len(games))
#
# s = time.time()
# games, results = parser("data/lichess/lichess_db_standard_rated_2019-10.pgn", elo=2700)
# save_game_data(games, results, "games_2700_2019")
# print("Igre smo sprocesirali v:", time.time() - s, " in imamo jih:", len(games))



games, results = load_game_data("games_2600_2019")

# G, all_results = create_metaposition_network(games, results, last_moves_percentage=0.05)
# embeddings = metaposition_node2vec(G, all_results, num_walks=200)

games = games

G, all_results = create_combined_metaposition_network(games, results, color_separated=True, last_moves_percentage=0.05)
embeddings = metaposition_node2vec(G, all_results, color_separated=True, num_walks=200)

X, y = parse_embeddings(embeddings)
clf = logistic_regression()
print(clf.cross_validate(X, y, k=5, output=True))


s = time.time()
X, y = shannon(games, results, last_moves_percentage=0.05)
print("Shannon:", time.time() - s)

clf = logistic_regression()
print(clf.cross_validate(X, y, k=5, output=True))