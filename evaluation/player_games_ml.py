import os
import pickle
from collections import Counter

from pgn_parser import *
from embeddings import *
from classifier import *
from classic_evaluations import *
from logger import *

game_data_file = "games_2700_2019"
num_walks_list = [100, 200, 300]
# last_moves_percentage_list = [0.001, 0.05, 0.1, 0.2, 0.3]
last_moves_percentage_list = [0.3]
max_games = 5000
num_walks = 300
last_moves_percentage = 0.05
k = 5
walk_length = 2
log = Log(filename="player_games_net_ml.txt", path="../logs")


def evaluate_ml(games, results, algorithm, color_separated):
    for last_moves_percentage in last_moves_percentage_list:
        print("Algorithm:", algorithm, "| Color separated:", color_separated)
        print("Last moves %:", last_moves_percentage)
        G, all_results = algorithm(games, results, color_separated=color_separated,
                                   last_moves_percentage=last_moves_percentage)

        embeddings = metaposition_node2vec(G, all_results, color_separated=color_separated, num_walks=num_walks,
                                           walk_length=walk_length, quiet=False)

        X, y = parse_embeddings(embeddings)
        print("Num of positions:", len(X))

        start = time.time()
        clf = logistic_regression()
        scores = clf.cross_validate(X, y, k=k, output=True)
        elapsed = time.time() - start
        print(clf.get_name(), "Cross Validation took:", elapsed)

        log.write((log.GAME_DATA, game_data_file),
                  (log.LAST_MOVES, last_moves_percentage),
                  (log.ML_ALG, clf.get_name()),
                  log.COLOR_SEPARATED,
                  (log.WALKS, num_walks),
                  (log.POSITIONS, len(X)),
                  (log.WALK_LENGTH, walk_length),
                  (log.MAX_GAMES, max_games),
                  (log.K, k),
                  (log.TIME, elapsed),
                  (log.ACCURACY, scores.mean()),
                  (log.STD_DEV, scores.std()))

        start = time.time()
        clf = svm()
        scores = clf.cross_validate(X, y, k=k, output=True)
        elapsed = time.time() - start
        print(clf.get_name(), "Cross Validation took:", elapsed)

        log.write((log.GAME_DATA, game_data_file),
                  (log.LAST_MOVES, last_moves_percentage),
                  (log.ML_ALG, clf.get_name()),
                  log.COLOR_SEPARATED,
                  (log.WALKS, num_walks),
                  (log.POSITIONS, len(X)),
                  (log.WALK_LENGTH, walk_length),
                  (log.MAX_GAMES, max_games),
                  (log.K, k),
                  (log.TIME, elapsed),
                  (log.ACCURACY, scores.mean()),
                  (log.STD_DEV, scores.std()))

        start = time.time()
        clf = bayes()
        scores = clf.cross_validate(X, y, k=k, output=True)
        elapsed = time.time() - start
        print(clf.get_name(), "Cross Validation took:", elapsed)

        log.write((log.GAME_DATA, game_data_file),
                  (log.LAST_MOVES, last_moves_percentage),
                  (log.ML_ALG, clf.get_name()),
                  log.COLOR_SEPARATED,
                  (log.WALKS, num_walks),
                  (log.POSITIONS, len(X)),
                  (log.WALK_LENGTH, walk_length),
                  (log.MAX_GAMES, max_games),
                  (log.K, k),
                  (log.TIME, elapsed),
                  (log.ACCURACY, scores.mean()),
                  (log.STD_DEV, scores.std()))

        start = time.time()
        clf = random_forest()
        scores = clf.cross_validate(X, y, k=k, output=True)
        elapsed = time.time() - start
        print(clf.get_name(), "Cross Validation took:", elapsed)

        log.write((log.GAME_DATA, game_data_file),
                  (log.LAST_MOVES, last_moves_percentage),
                  (log.ML_ALG, clf.get_name()),
                  log.COLOR_SEPARATED,
                  (log.WALKS, num_walks),
                  (log.POSITIONS, len(X)),
                  (log.WALK_LENGTH, walk_length),
                  (log.MAX_GAMES, max_games),
                  (log.K, k),
                  (log.TIME, elapsed),
                  (log.ACCURACY, scores.mean()),
                  (log.STD_DEV, scores.std()))

        start = time.time()
        clf = decision_trees()
        scores = clf.cross_validate(X, y, k=k, output=True)
        elapsed = time.time() - start
        print(clf.get_name(), "Cross Validation took:", elapsed)

        log.write((log.GAME_DATA, game_data_file),
                  (log.LAST_MOVES, last_moves_percentage),
                  (log.ML_ALG, clf.get_name()),
                  log.COLOR_SEPARATED,
                  (log.WALKS, num_walks),
                  (log.POSITIONS, len(X)),
                  (log.WALK_LENGTH, walk_length),
                  (log.MAX_GAMES, max_games),
                  (log.K, k),
                  (log.TIME, elapsed),
                  (log.ACCURACY, scores.mean()),
                  (log.STD_DEV, scores.std()))

        start = time.time()
        clf = neural_network()
        scores = clf.cross_validate(X, y, k=k, output=True)
        elapsed = time.time() - start
        print(clf.get_name(), "Cross Validation took:", elapsed)

        log.write((log.GAME_DATA, game_data_file),
                  (log.LAST_MOVES, last_moves_percentage),
                  (log.ML_ALG, clf.get_name()),
                  log.COLOR_SEPARATED,
                  (log.WALKS, num_walks),
                  (log.POSITIONS, len(X)),
                  (log.WALK_LENGTH, walk_length),
                  (log.MAX_GAMES, max_games),
                  (log.K, k),
                  (log.TIME, elapsed),
                  (log.ACCURACY, scores.mean()),
                  (log.STD_DEV, scores.std()))

        print()


games, results = load_game_data(game_data_file, path="../output", max_games=max_games)
evaluate_ml(games, results, create_combined_metaposition_network, color_separated=True)

#
# s = time.time()
# X, y = shannon(games, results, last_moves_percentage=last_moves_percentage)
# print("Shannon:", time.time() - s)
#
# clf = logistic_regression()
# clf.cross_validate(X, y, k=5, output=True)
