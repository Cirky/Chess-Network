import os
import pickle
from pgn_parser import *
from embeddings import *
from classifier import *
from classic_evaluations import *
from logger import *

# s = time.time()
# games, results = parser("data/lichess/lichess_db_standard_rated_2017-02.pgn", elo=2700)
# save_game_data(games, results, "games_2700")
# print("Igre smo sprocesirali v:", time.time() - s, " in imamo jih:", len(games))

game_data_file = "games_2600"

games, results = load_game_data(game_data_file)

last_moves_percentage = 0.01
G, all_results = create_metaposition_network(games, results, advanced=False, color_separated=True,
                                             last_moves_percentage=last_moves_percentage)

embeddings = metaposition_node2vec(G, all_results, color_separated=True, num_walks=150)
X, y = parse_embeddings(embeddings)

clf = logistic_regression()
print(clf.cross_validate(X, y, k=5, output=True))

s = time.time()
X, y = shannon(games, results, last_moves_percentage=last_moves_percentage)
print("Shannon:", time.time() - s)

clf = logistic_regression()
scores = clf.cross_validate(X, y, k=5, output=True)

log = Log()
log.write((log.GAME_DATA, game_data_file),
          (log.LAST_MOVES, last_moves_percentage),
          log.COLOR_SEPARATED,
          (log.WALKS, 150),
          (log.ACCURACY, scores.mean()),
          (log.STD_DEV, scores.std()))
