import pickle
from collections import defaultdict
import matplotlib.pyplot as plt
from logger import *

dataset = delog("player_games_net_ml.txt", path="../logs")

algs = [([], [], []) for _ in range(6)]
names = ["logistic regression", "SVM", "naive bayes", "random forest", "decision tree", "neural network"]
for data in dataset:
    if int(data[Log.WALKS]) != 300:
        continue
    ml = data[Log.ML_ALG]
    index = names.index(ml)
    res_tuple = algs[index]
    res_tuple[0].append(float(data[Log.LAST_MOVES]))
    res_tuple[1].append(float(data[Log.ACCURACY]))
    res_tuple[2].append(float(data[Log.STD_DEV]))

xlabels = ["last move", 0.05, 0.10, 0.20, 0.30]

plt.figure(figsize=(6, 5))
plt.rcParams.update({'font.size': 11})
plt.xlabel("Moves from end (%)")
plt.ylabel("Accuracy")
plt.errorbar(algs[0][0], algs[0][1], algs[0][2], linestyle="--", marker='^', markersize="6", label="Logistic regression", linewidth=0.8)
plt.errorbar(algs[1][0], algs[1][1], algs[1][2], linestyle="--", marker='v', markersize="6", label="Support vector machines", linewidth=0.8)
plt.errorbar(algs[2][0], algs[2][1], algs[2][2], linestyle="--", marker='o', markersize="6", label="Naive Bayes", linewidth=0.8)
plt.errorbar(algs[3][0], algs[3][1], algs[4][2], linestyle="--", marker='D', markersize="6", label="Random forest", linewidth=0.8)
plt.errorbar(algs[4][0], algs[4][1], algs[4][2], linestyle="--", marker='*', markersize="6", label="Decision tree", linewidth=0.8)
plt.errorbar(algs[5][0], algs[5][1], algs[5][2], linestyle="--", marker='s', markersize="6", label="Neural Networks", linewidth=0.8)
plt.xticks(algs[0][0], labels=xlabels)
plt.ylim([0.6, 0.92])
plt.legend()
plt.savefig("../output/graphs/human_games_ml.png")
plt.show()