import os
import pickle
from pgn_parser import *
from embeddings import *
from classifier import *
from classic_evaluations import *
from logger import *
import sys
from visualization import *
sys.setrecursionlimit(100000)

# s = time.time()
# games, results = parser("data/lichess/CCRL-4040.pgn", elo=0, time_control=False)
# save_game_data(games, results, "chess-engines")
# print("Igre smo sprocesirali v:", time.time() - s, " in imamo jih:", len(games))

# s = time.time()
# games, results = parser("data/lichess/lichess_db_standard_rated_2019-10.pgn", elo=2500)
# save_game_data(games, results, "games_2500_2019")
# print("Igre smo sprocesirali v:", time.time() - s, " in imamo jih:", len(games))


#games_file = "karpov"
games_file = "chess-engines"
p = 0.001
num_walks = 500
games, results = load_game_data(games_file)
num_of_games = 10000
boards = []

#print(results)

# G, all_results = create_metaposition_network(games, results, last_moves_percentage=0.05)
# embeddings = metaposition_node2vec(G, all_results, num_walks=200)

games = games[:num_of_games]

G, all_results = create_combined_metaposition_network(games, results, color_separated=True, last_moves_percentage=p, boards=boards)
embeddings = metaposition_node2vec(G, all_results, color_separated=True, num_walks=num_walks, dimensions=300)

X, y = parse_embeddings(embeddings)
clf = neural_network()

scores = clf.cross_validate(X, y, k=10, output=True)
#print(clf.cross_validate(X, y, k=5, output=True))


s = time.time()
X, y = shannon(games, results, last_moves_percentage=p)
print("Shannon:", time.time() - s)
print(clf.cross_validate(X, y, k=10, output=True))

# clf.train(X[:8000], y[:8000])
# print(clf.trained_classifier.classes_)
# probabilities = clf.get_probabilities(X[8000:])
#
# for i in range(50):
#     visualize_fen(boards[8000 + i], filename="board_" + str(i))
#     print("Probability " + str(i) + ":", probabilities[i], y[8000 + i])

log = Log(filename="log_maj.txt")
log.write((log.GAME_DATA, games_file),
          ("Number of games", num_of_games),
          (log.LAST_MOVES, p),
          (log.COLOR_SEPARATED, "True"),
          (log.WALKS, num_walks),
          ("Classifier", clf.get_name()),
          (log.ACCURACY, scores.mean()),
          (log.STD_DEV, scores.std()))
