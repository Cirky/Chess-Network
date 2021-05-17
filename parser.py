import chess
import chess.svg
import chess.pgn
import networkx as nx
import snap
import os
import time
import matplotlib.pyplot as plt
import pygraphviz
import scipy

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


def parser(file, elo=400):
    pgn = open(file)
    games = []
    results = []
    offsets = []
    while True:
        offset = pgn.tell()
        headers = chess.pgn.read_headers(pgn)
        if headers is None:
            break

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



def create_support_network(board, game_num, move_num):
    piece_map = board.piece_map()
    G = snap.TNEANet.New()
    G.AddStrAttrN("color")
    G.AddStrAttrE("type")

    color_dict_nodes = {}
    label_dict_nodes = {}
    type_dict_edges = {}
    for square in piece_map:
        if board.color_at(square): # true = white, false = nig, none = empty
            color = "white"
        else:
            color = "black"
        reach = board.attacks(square)
        if not G.IsNode(square):
            label_dict_nodes[square] = str(square)
            color_dict_nodes[square] = color
            G.AddNode(square)
            G.AddStrAttrDatN(square, color, "color")

        # print()
        # print(square, color)
        # print(reach)
        for reachable_square in reach:
            if board.color_at(reachable_square) is None:
                continue
            elif board.color_at(reachable_square):
                s_color = "white"
            else:
                s_color = "black"
            # print(reachable_square, s_color)
            if not G.IsNode(reachable_square):
                label_dict_nodes[reachable_square] = str(reachable_square)
                color_dict_nodes[reachable_square] = s_color
                G.AddNode(reachable_square)
                G.AddStrAttrDatN(reachable_square, s_color, "color")

            G.AddEdge(square, reachable_square)
            edge = G.GetEI(square, reachable_square)
            if s_color == color:
                type_dict_edges[edge.GetId()] = "defend"
                G.AddStrAttrDatE(edge.GetId(), "defend", "type")
            else:
                type_dict_edges[edge.GetId()] = "attack"
                G.AddStrAttrDatE(edge.GetId(), "attack", "type")

    G.SavePajek("networks/lichess/support_" + str(game_num) + "-" + str(move_num) + ".net", NIdLabelH=label_dict_nodes, NIdColorH=color_dict_nodes, EIdColorH=type_dict_edges)


def create_mobility_network(board, game_num, move_num):
    piece_map = board.piece_map()
    G = snap.TNEANet.New()
    G.AddStrAttrN("color")
    G.AddStrAttrE("type")

    color_dict_nodes = {}
    label_dict_nodes = {}
    type_dict_edges = {}
    for square in piece_map:
        if board.color_at(square): # true = white, false = nig, none = empty
            color = "white"
        else:
            color = "black"
        reach = board.attacks(square)
        if not G.IsNode(square):
            label_dict_nodes[square] = str(square)
            color_dict_nodes[square] = color
            G.AddNode(square)
            G.AddStrAttrDatN(square, color, "color")

        for reachable_square in reach:
            if board.color_at(reachable_square) is None:
                s_color = "none"
            elif board.color_at(reachable_square):
                s_color = "white"
            else:
                s_color = "black"

            if s_color == color:
                break

            if not G.IsNode(reachable_square):
                label_dict_nodes[reachable_square] = str(reachable_square)
                color_dict_nodes[reachable_square] = s_color
                G.AddNode(reachable_square)
                G.AddStrAttrDatN(reachable_square, s_color, "color")

            G.AddEdge(square, reachable_square)
            edge = G.GetEI(square, reachable_square)
            if s_color == color:
                type_dict_edges[edge.GetId()] = "defend"
                G.AddStrAttrDatE(edge.GetId(), "defend", "type")
            else:
                type_dict_edges[edge.GetId()] = "attack"
                G.AddStrAttrDatE(edge.GetId(), "attack", "type")

    G.SavePajek("networks/lichess/mobility_" + str(game_num) + "-" + str(move_num) + ".net", NIdLabelH=label_dict_nodes, NIdColorH=color_dict_nodes, EIdColorH=type_dict_edges)

def create_position_network(board, game_num, move_num, result):
  #  print(chess.SQUARES[3])
    piece_map = board.piece_map()
    G = snap.TNEANet.New()
    G.AddStrAttrN("color")
    G.AddStrAttrE("type")

    color_dict_nodes = {}
    label_dict_nodes = {}
    type_dict_edges = {}

    for square in piece_map:
        if board.color_at(square): # true = white, false = nig, none = empty
            color = "white"
        else:
            color = "black"
        reach = board.attacks(square)
        if not G.IsNode(square):
            label_dict_nodes[square] = str(square)
            color_dict_nodes[square] = color
            G.AddNode(square)
            G.AddStrAttrDatN(square, color, "color")

        for reachable_square in reach:
            if board.color_at(reachable_square) is None:
                s_color = "none"
            elif board.color_at(reachable_square):
                s_color = "white"
            else:
                s_color = "black"

            if not G.IsNode(reachable_square):
                label_dict_nodes[reachable_square] = str(reachable_square)
                color_dict_nodes[reachable_square] = s_color
                G.AddNode(reachable_square)
                G.AddStrAttrDatN(reachable_square, s_color, "color")

            G.AddEdge(square, reachable_square)
            edge = G.GetEI(square, reachable_square)
            if s_color == color:
                type_dict_edges[edge.GetId()] = "defend"
                G.AddStrAttrDatE(edge.GetId(), "defend", "type")
            else:
                type_dict_edges[edge.GetId()] = "attack"
                G.AddStrAttrDatE(edge.GetId(), "attack", "type")

    G.SavePajek("networks/li_new/position_" + str(game_num) + "-" + str(move_num) + ".net", NIdLabelH=label_dict_nodes, NIdColorH=color_dict_nodes, EIdColorH=type_dict_edges)
    f = open("networks/li_new/position_" + str(game_num) + "-" + str(move_num) + ".net", "a")
    f.write("Result = " + result)
    f.close()

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
    for node in G.nodes(data=True):
        if node[1]["color"] == "black":
            node_colors.append("brown")
        if node[1]["color"] == "white":
            node_colors.append("yellow")
        if node[1]["color"] == "none":
            node_colors.append("grey")
        node_size.append(100)
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

    pos = nx.nx_agraph.graphviz_layout(G)

    nx.draw_networkx(G, font_size=6, node_size=node_size, pos=pos, arrowsize=5, node_color=node_colors, edge_color=edge_colors, with_labels=True, labels=labels)
    plt.savefig("example_position_network.png")
    plt.show()


# file = open("data/chess_com_games_precejgej.pgn")
# games = parser(file)
#
# for game in games:
#     board = game.board()
#     for move in game.mainline_moves():
#         board.push(move)
#       #  boardsvg = chess.svg.board(board=board, size=420)
#       #  print(board)
#       #  print()
#     create_support_network(board)
#     create_mobility_network(board)
#     create_position_network(board)
#    # print(board.attacks(chess.F3))
#    # print(board.attacks(chess.D4))
#   #  boardsvg = chess.svg.board(board=board, size=420)
#   #  f = open("board.SVG", "w")
#   #  f.write(boardsvg)
#   #  f.close()
#     break

#read_network("test_support.out")
#read_network("test_mobility.out")
#read_network("test_position.out")

def get_information(file, elo):
    start = time.time()
    games, results = parser(file, elo)
    print("This took: ", time.time() - start)
    print(len(games))
    move_num = 0
    for game in games:
        for move in game.mainline_moves():
            move_num += 1
    print(move_num)


#get_information("data/lichess/lichess_db_standard_rated_2017-02.pgn", 2600)

def read_pgn_file(file, elo):
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
          #  create_support_network(board, game_num, move_num,result)
          #  create_mobility_network(board, game_num, move_num,result)
            create_position_network(board, game_num, move_num, result)
        print(game_num)
        game_num += 1


#read_pgn_file("data/lichess/lichess_db_standard_rated_2017-02.pgn", 2700)
