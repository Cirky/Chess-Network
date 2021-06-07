import os
import pickle
from pgn_parser import *
from embeddings import *
from classifier import *

# s = time.time()
# games, results = parser("data/lichess/lichess_db_standard_rated_2017-02.pgn", elo=2700)
# save_game_data(games, results, "games_2700")
# print("Igre smo sprocesirali v:", time.time() - s, " in imamo jih:", len(games))


games, results = load_game_data("games_2700")
G, all_results = create_metaposition_network(games, results)


embeddings = metaposition_node2vec(G, all_results)

# with open(os.path.join("output", "embeddings"), 'rb') as file:
#     embeddings = pickle.load(file)

X, y = parse_embeddings(embeddings)

clf = logistic_regression()
#clf.train(X, y)
#print(clf.predict(X))
#print(clf.get_score(X, y))
print(clf.cross_validate(X, y, k=5, output=True))
