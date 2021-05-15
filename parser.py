import chess
import chess.svg
import chess.pgn
import networkx as nx
import snap
import os

def read(file, path):
    G = nx.MultiDiGraph(name=file)
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
            edge = line.strip().split(' ')
           # print(edge)
            G.add_edge(nodes[edge[0]], nodes[edge[1]], type=edge[4])
    return G


def parser(file):
    game = chess.pgn.read_game(file)
    games = []
    while game is not None:
        game = chess.pgn.read_game(file)
        games.append(game)
      #  print(game.board())
    return games


def create_support_network(board):
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

    G.SavePajek("networks/test_support.out", NIdLabelH=label_dict_nodes, NIdColorH=color_dict_nodes, EIdColorH=type_dict_edges)

    return G

def create_mobility_network(board):
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

    G.SavePajek("networks/test_mobility.out", NIdLabelH=label_dict_nodes, NIdColorH=color_dict_nodes, EIdColorH=type_dict_edges)

    return G

def create_position_network(board):
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

    G.SavePajek("networks/test_position.out", NIdLabelH=label_dict_nodes, NIdColorH=color_dict_nodes, EIdColorH=type_dict_edges)

    return G


def open_network(file):
    G = read(file, "./networks/")
    for node in G.nodes(data=True):
        print(node)
    for edge in G.edges(data=True):
        print(edge)




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

open_network("test_support.out")
#open_network("test_mobility.out")
#open_network("test_position.out")
