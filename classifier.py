from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
import os
import pickle
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC


class logistic_regression:
    classifier = None
    trained_classifier = None

    def __init__(self, solver="saga", random_state=0, max_iter=10000):
        self.classifier = LogisticRegression(random_state=random_state, solver=solver, max_iter=max_iter)
        # self.classifier = make_pipeline(StandardScaler(), LogisticRegression(random_state=random_state, solver=solver, max_iter=max_iter))

    def train(self, X, y):
        if self.classifier is None:
            raise RuntimeError("No classifier")
        self.trained_classifier = self.classifier.fit(X, y)

    def predict(self, X):
        if self.trained_classifier is None:
            raise RuntimeError("No trained classifier")
        return self.trained_classifier.predict(X)

    def get_score(self, X, y):
        if self.trained_classifier is None:
            raise RuntimeError("No trained classifier")
        return self.trained_classifier.score(X, y)

    def cross_validate(self, X, y, k=5, output=False):
        if self.classifier is None:
            raise RuntimeError("No classifier")
        if k > len(X) - 1:
            k = len(X) - 1
        scores = cross_val_score(self.classifier, X, y, cv=k)
        if output:
            print("%0.5f accuracy with a standard deviation of %0.5f" % (scores.mean(), scores.std()))
        return scores

class svm:
    classifier = None
    trained_classifier = None

    def __init__(self):
        self.classifier = make_pipeline(StandardScaler(), SVC(gamma='auto'))

    def train(self, X, y):
        if self.classifier is None:
            raise RuntimeError("No classifier")
        self.trained_classifier = self.classifier.fit(X, y)

    def predict(self, X):
        if self.trained_classifier is None:
            raise RuntimeError("No trained classifier")
        return self.trained_classifier.predict(X)

    def get_score(self, X, y):
        if self.trained_classifier is None:
            raise RuntimeError("No trained classifier")
        return self.trained_classifier.score(X, y)

    def cross_validate(self, X, y, k=5, output=False):
        if self.classifier is None:
            raise RuntimeError("No classifier")
        if k > len(X) - 1:
            k = len(X) - 1
        scores = cross_val_score(self.classifier, X, y, cv=k)
        if output:
            print("%0.5f accuracy with a standard deviation of %0.5f" % (scores.mean(), scores.std()))
        return scores

def parse_embeddings(data):
    X = []
    y = []
    for key, value in data.items():
        if isinstance(key, int):
            X.append(value)
            result = data["result_" + str(key)]
            if result < 0:
                result = 0
            y.append(int(result))
    return X, y