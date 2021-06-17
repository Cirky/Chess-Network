import os
import pickle
from collections import Counter

from pgn_parser import *
from embeddings import *
from classifier import *
from classic_evaluations import *
from logger import *

game_data_file = "games_2700_2019"
last_moves_percentage_list = [0.001, 0.05, 0.1, 0.2, 0.3]
max_games = 5000
k = 5
walk_length = 2
log = Log(filename="player_games_shannon.txt", path="../logs")

def evaluate_shannon(games, results):
    for last_moves_percentage in last_moves_percentage_list:
        print("Last moves %:", last_moves_percentage)
        X, y = shannon(games, results, last_moves_percentage=last_moves_percentage)
        print("Num of positions:", len(X))

        start = time.time()
        clf = logistic_regression()
        scores = clf.cross_validate(X, y, k=k, output=True)
        elapsed = time.time() - start
        print(clf.get_name(), "Cross Validation took:", elapsed)

        log.write((log.GAME_DATA, game_data_file),
                  (log.LAST_MOVES, last_moves_percentage),
                  (log.ALGORITHM, "Shannon"),
                  (log.ML_ALG, clf.get_name()),
                  (log.POSITIONS, len(X)),
                  (log.MAX_GAMES, max_games),
                  (log.K, k),
                  (log.ACCURACY, scores.mean()),
                  (log.STD_DEV, scores.std()))
        print()


games, results = load_game_data(game_data_file, path="../output", max_games=max_games)
evaluate_shannon(games, results)

#
# s = time.time()
# X, y = shannon(games, results, last_moves_percentage=last_moves_percentage)
# print("Shannon:", time.time() - s)
#
# clf = logistic_regression()
# clf.cross_validate(X, y, k=5, output=True)
