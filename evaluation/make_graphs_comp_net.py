import pickle
from collections import defaultdict
import matplotlib.pyplot as plt
from logger import *

dataset = delog("computer_games_net_eval.txt", path="../logs")
alg1_X = []
alg1_Y = []
alg1_E = []
alg2_X = []
alg2_Y = []
alg2_E = []
alg3_X = []
alg3_Y = []
alg3_E = []
for data in dataset:
    if int(data[Log.WALKS]) != 200:
        continue
    if Log.COLOR_SEPARATED not in data or data[Log.COLOR_SEPARATED] == str(False):
        alg1_X.append(float(data[Log.LAST_MOVES]))
        alg1_Y.append(float(data[Log.ACCURACY]))
        alg1_E.append(float(data[Log.STD_DEV]))
    elif Log.COMBINED in data and data[Log.COMBINED] != str(False):
        alg3_X.append(float(data[Log.LAST_MOVES]))
        alg3_Y.append(float(data[Log.ACCURACY]))
        alg3_E.append(float(data[Log.STD_DEV]))
    else:
        alg2_X.append(float(data[Log.LAST_MOVES]))
        alg2_Y.append(float(data[Log.ACCURACY]))
        alg2_E.append(float(data[Log.STD_DEV]))

print(len(alg1_X), len(alg1_Y), len(alg1_E))

xlabels = ["last move", 0.05, 0.10, 0.20, 0.30]

plt.figure(figsize=(6, 5))
plt.rcParams.update({'font.size': 11})
plt.xlabel("Moves from end (%)")
plt.ylabel("Accuracy")
plt.errorbar(alg1_X, alg1_Y, alg1_E, linestyle="--", marker='^', markersize="6", label="Metaposition network", linewidth=0.8)
plt.errorbar(alg2_X, alg2_Y, alg2_E, linestyle="--", marker='o', markersize="6", label="Color separated network", linewidth=0.8)
plt.errorbar(alg3_X, alg3_Y, alg3_E, linestyle="--", marker='D', markersize="6", label="Color separated advanced network", linewidth=0.8)
plt.xticks(alg1_X, labels=xlabels)
plt.ylim([0.6, 0.92])
plt.legend()
plt.savefig("../output/graphs/computer_games_net.png")
plt.show()