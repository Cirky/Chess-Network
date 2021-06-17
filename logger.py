import os.path
from datetime import datetime


class Log:
    filename = None
    separator = ";"
    GAME_DATA = "Game Data"
    WALKS = "Walks"
    LAST_MOVES = "Perc. of last moves"
    COLOR_SEPARATED = "Color Separated"
    ACCURACY = "Accuracy"
    STD_DEV = "Std. Dev."
    ADVANCED = "Advanced"
    POSITION_NETWORKS = "Position Networks"
    WEIGHTED = "Weighted"
    MULTIPLE = "Multiple"
    ML_ALG = "ML Alg."
    MAX_GAMES = "Max Games"
    POSITIONS = "N Positions"
    K = "K"
    WALK_LENGTH = "Walk Length"
    TIME = "Time"
    COMBINED = "Combined"

    def __init__(self, path="logs", filename="log.txt"):
        self.filename = os.path.join(path, filename)

    def write(self, *data):
        if self.filename is None:
            print("LOGGER HAS NO FILE")
            return
        try:
            with open(self.filename, "a") as f:
                now = datetime.now()
                dt_string = now.strftime("%Y/%m/%d %H:%M:%S")
                f.write(dt_string)
                f.write(self.separator)
                for entry in data:
                    if isinstance(entry, tuple):
                        f.write(str(entry[0]))
                        f.write(self.separator)
                        f.write(str(entry[1]))
                        f.write(self.separator)
                    else:
                        f.write(str(entry))
                        f.write(self.separator)
                        f.write(self.separator)
                f.write("\n")
        except IOError:
            print("Error opening log")


def delog(filename, path="logs"):
    dataset = []
    with open(os.path.join(path, filename), 'r') as file:
        for line in file:
            data = {}
            dataset.append(data)
            params = line.strip().split(';')[:-1]
            data["date"] = params[0]
            # print(params)
            for i in range(1, len(params), 2):
                data[params[i]] = params[i + 1]
    return dataset
