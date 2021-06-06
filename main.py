import os
import pickle
from classifier import *

X, y = read_and_parse_embeddings("embeddings")

clf = logistic_regression()
clf.train(X, y)
print(clf.predict(X))
print(clf.get_score(X, y))
# cross_validation(clf, X, y, k=2, output=True)
