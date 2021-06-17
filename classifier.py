from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.model_selection import cross_val_score
import os
import pickle
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


class Classifier:
    classifier = None
    trained_classifier = None

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

    def get_probabilities(self, X):
        if self.trained_classifier is None:
            raise RuntimeError("No trained classifier")
        return self.trained_classifier.predict_proba(X)

    def cross_validate(self, X, y, k=5, output=False):
        if self.classifier is None:
            raise RuntimeError("No classifier")
        if k > len(X) - 1:
            k = len(X) - 1
        scores = cross_val_score(self.classifier, X, y, cv=k)
        if output:
            print("%0.5f accuracy with a standard deviation of %0.5f" % (scores.mean(), scores.std()))
        return scores


class logistic_regression(Classifier):
    # classifier = None
    # trained_classifier = None

    def __init__(self, solver="saga", random_state=0, max_iter=10000):
        self.classifier = LogisticRegression(random_state=random_state, solver=solver, max_iter=max_iter)
        # self.classifier = make_pipeline(StandardScaler(), LogisticRegression(random_state=random_state, solver=solver, max_iter=max_iter))

    def get_name(self):
        return "logistic regression"


class svm(Classifier):
    classifier = None
    trained_classifier = None

    def __init__(self, max_iter=10000):
        self.classifier = make_pipeline(StandardScaler(), SVC(gamma='auto', max_iter=max_iter))

    def get_name(self):
        return "SVM"

class sgd(Classifier):
    classifier = None
    trained_classifier = None

    def __init__(self, loss="hinge"):
        self.classifier = SGDClassifier(loss=loss, penalty="l2", max_iter=10000)

    def get_name(self):
        return "SGD"

class bayes(Classifier):
    classifier = None
    trained_classifier = None

    def __init__(self):
        self.classifier = GaussianNB()

    def get_name(self):
        return "naive bayes"

class random_forest(Classifier):
    classifier = None
    trained_classifier = None

    def __init__(self, max_depth=None):
        self.classifier = RandomForestClassifier(max_depth=max_depth, random_state=0)

    def get_name(self):
        return "random forest"

class decision_trees(Classifier):
    classifier = None
    trained_classifier = None

    def __init__(self, max_depth=None):
        self.classifier = DecisionTreeClassifier(max_depth=max_depth, random_state=0)

    def get_name(self):
        return "decision tree"

class neural_network(Classifier):
    classifier = None
    trained_classifier = None

    def __init__(self, max_iter=10000):
        self.classifier = MLPClassifier(random_state=1, max_iter=max_iter)

    def get_name(self):
        return "neural network"

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
