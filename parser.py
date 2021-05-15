import chess
import chess.svg
import chess.pgn
import networkx as nx
import snap


def parser(file):
    game = chess.pgn.read_game(file)
    games = []
    while game is not None:
        game = chess.pgn.read_game(file)
        games.append(game)
      #  print(game.board())
    return games


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

    G.SavePajek("networks/test.out", color_dict_nodes, label_dict_nodes, type_dict_edges)

    return G


def open_network():
    G = nx.read_pajek("networks/test.out")
    for node in G.nodes(data=True):
        print(node)
    for edge in G.edges(data=True):
        print(edge)

file = open("data/chess_com_games_precejgej.pgn")
games = parser(file)

for game in games:
    board = game.board()
    for move in game.mainline_moves():
        board.push(move)
      #  boardsvg = chess.svg.board(board=board, size=420)
      #  print(board)
      #  print()
    create_position_network(board)
   # print(board.attacks(chess.F3))
   # print(board.attacks(chess.D4))
  #  boardsvg = chess.svg.board(board=board, size=420)
  #  f = open("board.SVG", "w")
  #  f.write(boardsvg)
  #  f.close()
    break

open_network()