import os
import pickle
from collections import Counter

from pgn_parser import *
from embeddings import *
from classifier import *
from classic_evaluations import *
from logger import *
from visualization import *

# s = time.time()
# games, results = parser("data/lichess/lichess_db_standard_rated_2017-02.pgn", elo=2700)
# save_game_data(games, results, "games_2700")
# print("Igre smo sprocesirali v:", time.time() - s, " in imamo jih:", len(games))

game_data_file = "games_2700_2019"
num_walks = 200
last_moves_percentage = 0.05

games, results = load_game_data(game_data_file)
print(len(games), Counter(results))
boards = []
G, all_results = create_metaposition_network(games, results, color_separated=True,
                                             last_moves_percentage=last_moves_percentage)

embeddings = metaposition_node2vec(G, all_results, color_separated=True, num_walks=num_walks)

X, y = parse_embeddings(embeddings)
print(Counter(y))
# print(len(X), len(y))

clf = logistic_regression()
scores = clf.cross_validate(X, y, k=5, output=True)

# clf.train(X[:2000], y[:2000])
# print(clf.trained_classifier.classes_)
# probabilities = clf.get_probabilities(X[2000:])

# for i in range(50):
#     visualize_fen(boards[2000 + i], filename="board_" + str(i))
#     print("Probability " + str(i) + ":", probabilities[i], y[2000 + i])


log = Log(filename="log_uros.txt")
log.write((log.GAME_DATA, game_data_file),
          (log.LAST_MOVES, last_moves_percentage),
          log.COLOR_SEPARATED,
          # log.WEIGHTED,
          # log.POSITION_NETWORKS,
          (log.WALKS, num_walks),
          (log.ACCURACY, scores.mean()),
          (log.STD_DEV, scores.std()))

s = time.time()
X, y = shannon(games, results, last_moves_percentage=last_moves_percentage)
print("Shannon:", time.time() - s)

clf = logistic_regression()
clf.cross_validate(X, y, k=5, output=True)
# clf.train(X, y)
# print(clf.trained_classifier.classes_)
# probabilities = clf.get_probabilities(X)
