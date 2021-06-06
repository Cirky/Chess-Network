import snap
import chess
import chess.svg
import chess.pgn
import networkx as nx
import pickle
import time
import os
from node2vec import Node2Vec

def create_metaposition_network(games, results, progress=False):
    # start = time.time()
    # games, results = parser(file, elo)
    # print("This took: ", time.time() - start)
    # print(len(games))

    G = create_placement_network()

    all_results = []
    game_num = 0
    board_node = 0
    for game in games:
        board = game.board()
        if progress:
            print("Games Added:", str(game_num), "/", str(len(games)))
        if results[game_num] == "white":
            result = 1
        elif results[game_num] == "black":
            result = -1
        else:
            result = 0

        for move in game.mainline_moves():
            all_results.append(result)
            board.push(move)
            G.add_node(board_node)
            for square in board.piece_map():
                piece = board.piece_at(square).symbol()
                if piece == "k":
                    G.add_edge(board_node, "B_K" + chess.square_name(square))
                elif piece == "K":
                    G.add_edge(board_node, "W_K" + chess.square_name(square))
                elif piece == "q":
                    G.add_edge(board_node, "B_Q" + chess.square_name(square))
                elif piece == "Q":
                    G.add_edge(board_node, "W_Q" + chess.square_name(square))
                elif piece == "r":
                    G.add_edge(board_node, "B_R" + chess.square_name(square))
                elif piece == "R":
                    G.add_edge(board_node, "W_R" + chess.square_name(square))
                elif piece == "b":
                    G.add_edge(board_node, "B_B" + chess.square_name(square))
                elif piece == "B":
                    G.add_edge(board_node, "W_B" + chess.square_name(square))
                elif piece == "n":
                    G.add_edge(board_node, "B_N" + chess.square_name(square))
                elif piece == "N":
                    G.add_edge(board_node, "W_N" + chess.square_name(square))
                elif piece == "p":
                    G.add_edge(board_node, "B_P" + chess.square_name(square))
                elif piece == "P":
                    G.add_edge(board_node, "W_P" + chess.square_name(square))
            board_node = +1
        game_num += 1

    return G, all_results

def create_placement_network():
    G = nx.DiGraph()
    for char in ["a", "b", "c", "d", "e", "f", "g", "h"]:
        for number in [1, 2, 3, 4, 5, 6, 7, 8]:
            G.add_node("W_K" + char + str(number))
            G.add_node("W_Q" + char + str(number))
            G.add_node("W_R" + char + str(number))
            G.add_node("W_B" + char + str(number))
            G.add_node("W_N" + char + str(number))
            G.add_node("B_K" + char + str(number))
            G.add_node("B_Q" + char + str(number))
            G.add_node("B_R" + char + str(number))
            G.add_node("B_B" + char + str(number))
            G.add_node("B_N" + char + str(number))
            if number not in [1, 8]:
                G.add_node("W_P" + char + str(number))
                G.add_node("B_P" + char + str(number))

    return G

def create_support_network(board, game_num, move_num, result):
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
    f = open("networks/lichess/support_" + str(game_num) + "-" + str(move_num) + ".net", "a")
    f.write("Result = " + result)
    f.close()
    return G

def create_mobility_network(board, game_num, move_num, result):
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

        # dont count sideways pawn attacks if there are no pieces there
        if board.piece_at(square).piece_type == chess.PAWN:
            reach_c = reach.copy()
            for reachable_square in reach:
                if board.color_at(reachable_square) is None:
                    reach_c.remove(reachable_square)
            reach = reach_c

        # pawn movement
        if board.piece_at(square).piece_type == chess.PAWN:
            sqr = chess.square_name(square)
            for move in board.legal_moves:
                if chess.square_name(move.from_square) == sqr:  # and move.to_square not in reach:
                    reach.add(move.to_square)

            board.turn = not board.turn  # legalne poteze dobi samu stran na potezi, zatu obrnem kdu je na vrsti
            for move in board.legal_moves:
                if chess.square_name(move.from_square) == sqr:  # and move.to_square not in reach:
                    reach.add(move.to_square)
            board.turn = not board.turn

        for reachable_square in reach:
            if board.color_at(reachable_square) is None:
                s_color = "none"
                # dont count sideways pawn attacks if there are no pieces there
                if board.piece_at(square).piece_type == chess.PAWN:
                    continue
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
    f = open("networks/lichess/mobility_" + str(game_num) + "-" + str(move_num) + ".net", "a")
    f.write("Result = " + result)
    f.close()
    return G


def create_position_network(board, game_num, move_num, result, file):
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

        # dont count sideways pawn attacks if there are no pieces there
        if board.piece_at(square).piece_type == chess.PAWN:
            reach_c = reach.copy()
            for reachable_square in reach:
                if board.color_at(reachable_square) is None:
                    reach_c.remove(reachable_square)
            reach = reach_c

        # pawn movement
        if board.piece_at(square).piece_type == chess.PAWN:
            sqr = chess.square_name(square)
            for move in board.legal_moves:
                if chess.square_name(move.from_square) == sqr: # and move.to_square not in reach:
                    reach.add(move.to_square)

            board.turn = not board.turn # legalne poteze dobi samu stran na potezi, zatu obrnem kdu je na vrsti
            for move in board.legal_moves:
                if chess.square_name(move.from_square) == sqr: # and move.to_square not in reach:
                    reach.add(move.to_square)
            board.turn = not board.turn

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

    G.SavePajek("networks/"+file+"/position_" + str(game_num) + "-" + str(move_num) + ".net", NIdLabelH=label_dict_nodes, NIdColorH=color_dict_nodes, EIdColorH=type_dict_edges)
    f = open("networks/"+file+"/position_" + str(game_num) + "-" + str(move_num) + ".net", "a")
    f.write("Result = " + result)
    f.close()
    return G


def create_dummy():

    G = create_placement_network()

    fen1 = "8/6k1/5pp1/3Q4/6K1/8/8/8 w - - 0 1" # 1-0
    fen2 = "8/8/3p1k2/4b3/2Q5/3KP3/8/8 w - - 0 1" # 1-0
    fen3 = "8/Q7/3p1k2/4b1pp/8/3K4/8/1R6 w - - 0 1" # 1-0
    fen4 = "8/4k3/8/2q5/8/5N2/4P1K1/8 w - - 0 1" # 0-1

    board1 = chess.Board(fen1)
    board2 = chess.Board(fen2)
    board3 = chess.Board(fen3)
    board4 = chess.Board(fen4)

    boards = [board1, board2, board3, board4]
    results = [1, 1, 1, -1]

    board_node = 0
    for board in boards:
        G.add_node(board_node)
        for square in board.piece_map():
            piece = board.piece_at(square).symbol()
            if piece == "k":
                G.add_edge(board_node, "B_K" + chess.square_name(square))
            elif piece == "K":
                G.add_edge(board_node, "W_K" + chess.square_name(square))
            elif piece == "q":
                G.add_edge(board_node, "B_Q" + chess.square_name(square))
            elif piece == "Q":
                G.add_edge(board_node, "W_Q" + chess.square_name(square))
            elif piece == "r":
                G.add_edge(board_node, "B_R" + chess.square_name(square))
            elif piece == "R":
                G.add_edge(board_node, "W_R" + chess.square_name(square))
            elif piece == "b":
                G.add_edge(board_node, "B_B" + chess.square_name(square))
            elif piece == "B":
                G.add_edge(board_node, "W_B" + chess.square_name(square))
            elif piece == "n":
                G.add_edge(board_node, "B_N" + chess.square_name(square))
            elif piece == "N":
                G.add_edge(board_node, "W_N" + chess.square_name(square))
            elif piece == "p":
                G.add_edge(board_node, "B_P" + chess.square_name(square))
            elif piece == "P":
                G.add_edge(board_node, "W_P" + chess.square_name(square))

        board_node += 1

    node2vec = Node2Vec(G, dimensions=64, walk_length=1, num_walks=200, workers=1, p=1, q=1, seed=69)

    start = time.time()
    model = node2vec.fit(window=10, min_count=1, batch_words=4)
    print("this took:", time.time() - start)

    embeddings = {}
    for board_num in range(board_node):
        embeddings[board_num] = model.wv[str(board_num)]
        embeddings["result_" + str(board_num)] = results[board_num]

    with open(os.path.join("output/", "embeddings"), 'wb') as file:
        pickle.dump(embeddings, file)

    with open(os.path.join("output/", "embeddings"), 'rb') as file:
        r = pickle.load(file)
    print(r)