import chess.svg
import chess.pgn
import matplotlib.pyplot as plt

from networks import *

def read(file, path):
    G = nx.MultiDiGraph(name=file)
    result = ""
    with open(os.path.join(path, file), 'r') as file:
        nodes = {}
        for line in file:
            if line.startswith('*Vertices'):
                continue
            elif line.startswith('*Edges') or line.startswith('*Arcs'):
                break
            else:
                node = line.strip().split(' ')
            #    print(node)
                nodes[node[0]] = node[2].strip('"')
                G.add_node(node[2].strip('"'), id=int(node[0]), color=node[4])
        for line in file:
            if line.startswith("Result"):
                rez = line.strip().split(' ')
                result = rez[2]
                break
            edge = line.strip().split(' ')
            G.add_edge(nodes[edge[0]], nodes[edge[1]], type=edge[4])
    return G, result


def parser(file, elo=400, draws=False):
    pgn = open(file)
    games = []
    results = []
    offsets = []
    while True:
        offset = pgn.tell()
        headers = chess.pgn.read_headers(pgn)
        if headers is None:
            break

        if not draws:
            if headers.get("Result") == "1/2-1/2":
                continue

        elo_white = headers.get("WhiteElo")
        elo_black = headers.get("BlackElo")

        if not elo_white.isnumeric():
            elo_white = 0
        if not elo_black.isnumeric():
            elo_black = 0

        time_control = headers.get("TimeControl")

        if not time_control[0:4].isnumeric():
            if not time_control[0:3].isnumeric():
                continue

            if int(time_control[0:3]) < 180:
                continue

        if int(elo_black) >= elo or int(elo_white) >= elo:
            offsets.append(offset)
            result = headers.get("Result")
            if result == "1-0":
                results.append("white")
            elif result == "0-1":
                results.append("black")
            else:
                results.append("draw")

    for offset in offsets:
        pgn.seek(offset)
        games.append(chess.pgn.read_game(pgn))

    return games, results


def read_network(file):
    G, result = read(file, "./networks/")
    # for node in G.nodes(data=True):
    #     print(node)
    # for edge in G.edges(data=True):
    #     print(edge)

    # sub = []
    # for node in G.nodes(data=True):
    #     if node[1]["color"] == "white":
    #         sub.append(node[0])
    # G = G.subgraph(sub)


    node_colors = []
    edge_colors = []
    labels = {}
    node_size = []
    pos = {}
    for node in G.nodes(data=True):
        if node[1]["color"] == "black":
            node_colors.append("brown")
        if node[1]["color"] == "white":
            node_colors.append("yellow")
        if node[1]["color"] == "none":
            node_colors.append("grey")
        node_size.append(100)
        pos[node[0]] = (int(node[0]) % 8, int(int(node[0]) / 8))
        labels[node[0]] = chess.square_name(int(node[0]))

    for edge in G.edges(data=True):
        if edge[2]["type"] == "attack":
         #   print(G.nodes[edge[1]])
            n = G.nodes[edge[1]]
            if n["color"] == "none":
                edge_colors.append("blue")
            else:
                edge_colors.append("red")

        if edge[2]["type"] == "defend":
            edge_colors.append("green")

   # print(pos)
   # pos = nx.nx_agraph.graphviz_layout(G)

    nx.draw_networkx(G, font_size=6, node_size=node_size, pos=pos, arrowsize=5, node_color=node_colors, edge_color=edge_colors, with_labels=True, labels=labels)
    plt.savefig("example_position_network.png")
    plt.show()

def read_pgn_file(file, elo, support_network=False, mobility_network=False, position_network=True):
    start = time.time()
    games, results = parser(file, elo)
    print("This took: ", time.time() - start)
    print(len(games))
    game_num = 0
    for game in games:
        board = game.board()
        result = results[game_num]
        for move in game.mainline_moves():
            board.push(move)
            move_num = board.ply()
            if support_network:
                create_support_network(board, game_num, move_num, result, "li_new")
            if mobility_network:
                create_mobility_network(board, game_num, move_num, result, "li_new")
            if position_network:
                create_position_network(board, game_num, move_num, result, "li_new")
        print(game_num)
        game_num += 1

def test():
    G, result = read("dummy/position_1-0.net", "./networks/")
    G.add_node(420)
    for node in G.nodes():
        if node == 420:
            continue
        G.add_edge(420, node)

    node2vec = Node2Vec(G, dimensions=64, walk_length=30, num_walks=200, workers=1)
    model = node2vec.fit(window=10, min_count=1, batch_words=4)
    print(model.wv.most_similar('420'))


def save_game_data(games, results, filename):
    with open(os.path.join("output", filename), 'wb') as file:
        pickle.dump({"games": games, "results": results}, file)


def load_game_data(filename):
    with open(os.path.join("output", filename), 'rb') as file:
        data = pickle.load(file)
    return data["games"], data["results"]
