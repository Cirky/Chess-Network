import snap
import chess
import chess.svg
import chess.pgn
import networkx as nx
import pickle
import time
import os
from node2vec import Node2Vec
import matplotlib.pyplot as plt


def create_metaposition_network(games, results, progress=False, directed=True, advanced=False, color_separated=False,
                                last_moves_percentage=1, boards=None):
    if advanced:
        G = create_advanced_placement_network(directed)
    else:
        G = create_placement_network(directed)

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

        last_moves_n = 0
        for _ in game.mainline_moves():
            last_moves_n += 1
        last_moves_n = int(last_moves_n * (1 - last_moves_percentage))

        for move in game.mainline_moves():
            board.push(move)
            if last_moves_n > 0:
                last_moves_n -= 1
                continue

            if boards is not None:
                boards.append(board.copy())

            all_results.append(result)
            if not color_separated:
                G.add_node(board_node)
            else:
                white_node = str(board_node) + "W"
                black_node = str(board_node) + "B"
                G.add_node(white_node)
                G.add_node(black_node)
            for square in board.piece_map():
                piece = board.piece_at(square).symbol()
                node = board_node
                if color_separated:
                    if board.piece_at(square).color == chess.WHITE:
                        node = white_node
                    else:
                        node = black_node
                G.add_edge(node, piece + chess.square_name(square))
            board_node += 1
        game_num += 1

    return G, all_results


def create_weighted_metaposition_network(games, results, progress=False, color_separated=False, last_moves_percentage=1):
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

        last_moves_n = 0
        for _ in game.mainline_moves():
            last_moves_n += 1
        last_moves_n = int(last_moves_n * (1 - last_moves_percentage))

        for move in game.mainline_moves():
            board.push(move)
            if last_moves_n > 0:
                last_moves_n -= 1
                continue

            all_results.append(result)
            if not color_separated:
                G.add_node(board_node)
            else:
                white_node = str(board_node) + "W"
                black_node = str(board_node) + "B"
                G.add_node(white_node)
                G.add_node(black_node)
            for square in board.piece_map():
                piece = board.piece_at(square).symbol()
                node = board_node
                if color_separated:
                    if board.piece_at(square).color == chess.WHITE:
                        node = white_node
                    else:
                        node = black_node
                if piece == "k":
                    G.add_edge(node, "k" + chess.square_name(square))
                elif piece == "K":
                    G.add_edge(node, "K" + chess.square_name(square))
                elif piece == "q":
                    G.add_edge(node, "q" + chess.square_name(square), weight=9)
                elif piece == "Q":
                    G.add_edge(node, "Q" + chess.square_name(square), weight=9)
                elif piece == "r":
                    G.add_edge(node, "r" + chess.square_name(square), weight=5)
                elif piece == "R":
                    G.add_edge(node, "R" + chess.square_name(square), weight=5)
                elif piece == "b":
                    G.add_edge(node, "b" + chess.square_name(square), weight=3.2)
                elif piece == "B":
                    G.add_edge(node, "B" + chess.square_name(square), weight=3.2)
                elif piece == "n":
                    G.add_edge(node, "n" + chess.square_name(square), weight=2.8)
                elif piece == "N":
                    G.add_edge(node, "N" + chess.square_name(square), weight=2.8)
                elif piece == "p":
                    G.add_edge(node, "p" + chess.square_name(square), weight=1)
                elif piece == "P":
                    G.add_edge(node, "P" + chess.square_name(square), weight=1)
            board_node += 1
        game_num += 1

    return G, all_results


# def create_color_separated_metaposition_network(games, results, progress=False, directed=True, advanced=False, last_moves_percentage=1):
#     # start = time.time()
#     # games, results = parser(file, elo)
#     # print("This took: ", time.time() - start)
#     # print(len(games))
#
#     if advanced:
#         G = create_advanced_placement_network(directed)
#     else:
#         G = create_placement_network(directed)
#
#     all_results = []
#     game_num = 0
#     board_node = 0
#     for game in games:
#         board = game.board()
#         if progress:
#             print("Games Added:", str(game_num), "/", str(len(games)))
#         if results[game_num] == "white":
#             result = 1
#         elif results[game_num] == "black":
#             result = -1
#         else:
#             result = 0
#
#         last_moves_n = 0
#         # last_moves_n = len(game.mainline_moves())
#         for _ in game.mainline_moves():
#             last_moves_n += 1
#         last_moves_n = int(last_moves_n * (1 - last_moves_percentage))
#
#         for move in game.mainline_moves():
#             board.push(move)
#             if last_moves_n > 0:
#                 last_moves_n -= 1
#                 continue
#
#             all_results.append(result)
#             white_node = str(board_node) + "W"
#             black_node = str(board_node) + "B"
#             G.add_node(white_node)
#             G.add_node(black_node)
#             for square in board.piece_map():
#                 piece = board.piece_at(square).symbol()
#                 if piece == "k":
#                     G.add_edge(black_node, "B_K" + chess.square_name(square))
#                 elif piece == "K":
#                     G.add_edge(white_node, "W_K" + chess.square_name(square))
#                 elif piece == "q":
#                     G.add_edge(black_node, "B_Q" + chess.square_name(square))
#                 elif piece == "Q":
#                     G.add_edge(white_node, "W_Q" + chess.square_name(square))
#                 elif piece == "r":
#                     G.add_edge(black_node, "B_R" + chess.square_name(square))
#                 elif piece == "R":
#                     G.add_edge(white_node, "W_R" + chess.square_name(square))
#                 elif piece == "b":
#                     G.add_edge(black_node, "B_B" + chess.square_name(square))
#                 elif piece == "B":
#                     G.add_edge(white_node, "W_B" + chess.square_name(square))
#                 elif piece == "n":
#                     G.add_edge(black_node, "B_N" + chess.square_name(square))
#                 elif piece == "N":
#                     G.add_edge(white_node, "W_N" + chess.square_name(square))
#                 elif piece == "p":
#                     G.add_edge(black_node, "B_P" + chess.square_name(square))
#                 elif piece == "P":
#                     G.add_edge(white_node, "W_P" + chess.square_name(square))
#             board_node += 1
#         game_num += 1
#
#     return G, all_results


def create_attack_metaposition_network(games, results, progress=False, directed=True, advanced=False,
                                       color_separated=False, last_moves_percentage=1):
    G = create_attack_network(directed)
    # G = add_attack_network2(nx.MultiDiGraph())

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

        last_moves_n = 0
        for _ in game.mainline_moves():
            last_moves_n += 1
        last_moves_n = int(last_moves_n * (1 - last_moves_percentage))

        for move in game.mainline_moves():
            board.push(move)
            if last_moves_n > 0:
                last_moves_n -= 1
                continue

            all_results.append(result)
            if not color_separated:
                G.add_node(board_node)
            else:
                white_node = str(board_node) + "W"
                black_node = str(board_node) + "B"
                G.add_node(white_node)
                G.add_node(black_node)

            for square in board.piece_map():
                node = board_node
                if color_separated:
                    if board.piece_at(square).color == chess.WHITE:
                        node = white_node
                    else:
                        node = black_node
                piece = board.piece_at(square)
                color = board.color_at(square)
                for attacked_square in board.attacks(square):
                    if board.color_at(attacked_square) is None or board.color_at(attacked_square) is color:
                        continue
                    attacked_piece = board.piece_at(attacked_square)
                    # square_name = chess.square_name(attacked_square)
                    G.add_edge(node, piece.symbol() + "->" + attacked_piece.symbol())

            board_node += 1
        game_num += 1

    # for e in G.edges():
    #     print(e)
    return G, all_results


def create_combined_metaposition_network(games, results, progress=False, directed=True, advanced=False,
                                         color_separated=False, last_moves_percentage=1):
    G = create_placement_network(directed, multigraph=True)
    G = add_attack_network(G)

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

        last_moves_n = 0
        for _ in game.mainline_moves():
            last_moves_n += 1
        last_moves_n = int(last_moves_n * (1 - last_moves_percentage))

        for move in game.mainline_moves():
            board.push(move)
            if last_moves_n > 0:
                last_moves_n -= 1
                continue

            all_results.append(result)
            if not color_separated:
                G.add_node(board_node)
            else:
                white_node = str(board_node) + "W"
                black_node = str(board_node) + "B"
                G.add_node(white_node)
                G.add_node(black_node)

            for square in board.piece_map():
                node = board_node
                if color_separated:
                    if board.piece_at(square).color == chess.WHITE:
                        node = white_node
                    else:
                        node = black_node
                piece = board.piece_at(square)
                color = board.color_at(square)
                G.add_edge(node, piece.symbol() + chess.square_name(square))  # placement

                for attacked_square in board.attacks(square):
                    if board.color_at(attacked_square) is None:
                        continue
                    if board.color_at(attacked_square) is color: #obrambe
                        defended_piece = board.piece_at(attacked_square)
                        G.add_edge(node, piece.symbol() + "->" + defended_piece.symbol())
                    else: # napadi
                        attacked_piece = board.piece_at(attacked_square)
                    #    square_name = chess.square_name(attacked_square)
                        G.add_edge(node, piece.symbol() + "->" + attacked_piece.symbol())

            board_node += 1
        game_num += 1

    return G, all_results


def create_attack_network(directed=True):
    if directed:
        G = nx.MultiDiGraph()
    else:
        G = nx.MultiGraph()

    for piece in ["K", "Q", "R", "B", "N", "P"]:
        for piece2 in ["k", "q", "r", "b", "n", "p"]:
            if piece == "K" and piece2 == "k":
                continue
            G.add_node(piece + "->" + piece2)

    for piece in ["k", "q", "r", "b", "n", "p"]:
        for piece2 in ["K", "Q", "R", "B", "N", "P"]:
            if piece == "k" and piece2 == "K":
                continue
            G.add_node(piece + "->" + piece2)

    #  for n in G.nodes():
    #      print(n)
    return G


def add_attack_network(G):
    for piece in ["K", "Q", "R", "B", "N", "P"]:
        for piece2 in ["k", "q", "r", "b", "n", "p"]:
            if piece == "K" and piece2 == "k":
                continue
            G.add_node(piece + "->" + piece2)

    for piece in ["k", "q", "r", "b", "n", "p"]:
        for piece2 in ["K", "Q", "R", "B", "N", "P"]:
            if piece == "k" and piece2 == "K":
                continue
            G.add_node(piece + "->" + piece2)
    return G


def add_attack_network2(G):
    for piece in ["K", "Q", "R", "B", "N", "P"]:
        for piece2 in ["k", "q", "r", "b", "n", "p"]:
            if piece == "K" and piece2 == "k":
                continue
            for char in ["a", "b", "c", "d", "e", "f", "g", "h"]:
                for number in [1, 2, 3, 4, 5, 6, 7, 8]:
                    square_name = char + str(number)
                    G.add_node(piece + "->" + piece2 + square_name)

    for piece in ["k", "q", "r", "b", "n", "p"]:
        for piece2 in ["K", "Q", "R", "B", "N", "P"]:
            if piece == "k" and piece2 == "K":
                continue
            for char in ["a", "b", "c", "d", "e", "f", "g", "h"]:
                for number in [1, 2, 3, 4, 5, 6, 7, 8]:
                    square_name = char + str(number)
                    G.add_node(piece + "->" + piece2 + square_name)
    return G


def create_placement_network(directed=True, multigraph=False):
    if multigraph and directed:
        G = nx.MultiDiGraph()
    if not multigraph and directed:
        G = nx.DiGraph()
    if multigraph and not directed:
        G = nx.Graph()
    if not multigraph and not directed:
        G = nx.MultiGraph()

    for char in ["a", "b", "c", "d", "e", "f", "g", "h"]:
        for number in [1, 2, 3, 4, 5, 6, 7, 8]:
            square_name = char + str(number)
            G.add_node("K" + square_name)
            G.add_node("Q" + square_name)
            G.add_node("R" + square_name)
            G.add_node("B" + square_name)
            G.add_node("N" + square_name)
            G.add_node("k" + square_name)
            G.add_node("q" + square_name)
            G.add_node("r" + square_name)
            G.add_node("b" + square_name)
            G.add_node("n" + square_name)
            if number not in [1, 8]:
                G.add_node("P" + square_name)
                G.add_node("p" + square_name)

    return G


def helper_adv(G, piece, square_name, node_name):
    board = chess.Board(None)
    piece = chess.Piece.from_symbol(piece)
    square = chess.parse_square(square_name)
    board.set_piece_at(square, piece)
    attacks = board.attacks(square)

    for sq in attacks:
        square_name = chess.square_name(sq)
        for node in G.nodes():
            if node.endswith(square_name):
                G.add_edge(node, node_name)


def create_advanced_placement_network(directed=True):
    if directed:
        G = nx.DiGraph()
    else:
        G = nx.Graph()
    for char in ["a", "b", "c", "d", "e", "f", "g", "h"]:
        for number in [1, 2, 3, 4, 5, 6, 7, 8]:
            square_name = char + str(number)
            G.add_node("W_K" + square_name)
            G.add_node("W_Q" + square_name)
            G.add_node("W_R" + square_name)
            G.add_node("W_B" + square_name)
            G.add_node("W_N" + square_name)
            G.add_node("B_K" + square_name)
            G.add_node("B_Q" + square_name)
            G.add_node("B_R" + square_name)
            G.add_node("B_B" + square_name)
            G.add_node("B_N" + square_name)
            if number not in [1, 8]:
                G.add_node("W_P" + square_name)
                G.add_node("B_P" + square_name)

    for char in ["a", "b", "c", "d", "e", "f", "g", "h"]:
        for number in [1, 2, 3, 4, 5, 6, 7, 8]:
            square_name = char + str(number)
            helper_adv(G, "K", square_name, "W_K" + square_name)
            helper_adv(G, "Q", square_name, "W_Q" + square_name)
            helper_adv(G, "R", square_name, "W_R" + square_name)
            helper_adv(G, "B", square_name, "W_B" + square_name)
            helper_adv(G, "N", square_name, "W_N" + square_name)
            helper_adv(G, "k", square_name, "B_K" + square_name)
            helper_adv(G, "q", square_name, "B_Q" + square_name)
            helper_adv(G, "r", square_name, "B_R" + square_name)
            helper_adv(G, "b", square_name, "B_B" + square_name)
            helper_adv(G, "n", square_name, "B_N" + square_name)
            if number not in [1, 8]:
                helper_adv(G, "P", square_name, "W_P" + square_name)
                helper_adv(G, "p", square_name, "B_P" + square_name)

    # print(len(G.nodes()), len(G.edges()))
    return G


# create_advanced_placement_network()
def create_position_networks(games, results, progress=False, color_separated=False,
                                last_moves_percentage=1):
    networks = []
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

        last_moves_n = 0
        for _ in game.mainline_moves():
            last_moves_n += 1
        last_moves_n = int(last_moves_n * (1 - last_moves_percentage))

        for move in game.mainline_moves():
            board.push(move)
            if last_moves_n > 0:
                last_moves_n -= 1
                continue

            all_results.append(result)
            G = create_position_network(board, board_node, color_separated)
            networks.append(G)
            board_node += 1
        game_num += 1

    return networks, all_results

def create_position_network(board, board_node, color_separated=False):
    piece_map = board.piece_map()
    G = nx.DiGraph()
    node = str(board_node)
    if not color_separated:
        G.add_node(node)
    else:
        white_node = node + "W"
        black_node = node + "B"
        G.add_node(white_node)
        G.add_node(black_node)

    for square in piece_map:
        reach = board.attacks(square)
        square_name = chess.square_name(square)
        if square not in G:
            G.add_node(square_name)
            if not color_separated:
                G.add_edge(node, square_name)
            else:
                if board.color_at(square) == chess.WHITE:
                    G.add_edge(white_node, square_name)
                else:
                    G.add_edge(black_node, square_name)

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
            if reachable_square not in G:
                square_name = chess.square_name(reachable_square)
                G.add_node(square_name)
                if not color_separated:
                    G.add_edge(node, square_name)
                else:
                    if board.color_at(reachable_square) == chess.WHITE:
                        G.add_edge(white_node, square_name)
                    else:
                        G.add_edge(black_node, square_name)

            G.add_edge(chess.square_name(square), chess.square_name(reachable_square))
            # edge = G.GetEI(square, reachable_square)
            # if s_color == color:
            #     type_dict_edges[edge.GetId()] = "defend"
            #     G.AddStrAttrDatE(edge.GetId(), "defend", "type")
            # else:
            #     type_dict_edges[edge.GetId()] = "attack"
            #     G.AddStrAttrDatE(edge.GetId(), "attack", "type")
    # nx.draw_networkx(G)
    # plt.savefig('net.png')
    # plt.draw()
    return G


############### SNAP.PY

def create_support_network(board, game_num, move_num, result):
    piece_map = board.piece_map()
    G = snap.TNEANet.New()
    G.AddStrAttrN("color")
    G.AddStrAttrE("type")

    color_dict_nodes = {}
    label_dict_nodes = {}
    type_dict_edges = {}
    for square in piece_map:
        if board.color_at(square):  # true = white, false = nig, none = empty
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

    G.SavePajek("networks/lichess/support_" + str(game_num) + "-" + str(move_num) + ".net", NIdLabelH=label_dict_nodes,
                NIdColorH=color_dict_nodes, EIdColorH=type_dict_edges)
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
        if board.color_at(square):  # true = white, false = nig, none = empty
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

    G.SavePajek("networks/lichess/mobility_" + str(game_num) + "-" + str(move_num) + ".net", NIdLabelH=label_dict_nodes,
                NIdColorH=color_dict_nodes, EIdColorH=type_dict_edges)
    f = open("networks/lichess/mobility_" + str(game_num) + "-" + str(move_num) + ".net", "a")
    f.write("Result = " + result)
    f.close()
    return G


# def create_position_network(board, game_num, move_num, result, file):
#     #  print(chess.SQUARES[3])
#     piece_map = board.piece_map()
#     G = snap.TNEANet.New()
#     G.AddStrAttrN("color")
#     G.AddStrAttrE("type")
#
#     color_dict_nodes = {}
#     label_dict_nodes = {}
#     type_dict_edges = {}
#
#     for square in piece_map:
#         if board.color_at(square):  # true = white, false = nig, none = empty
#             color = "white"
#         else:
#             color = "black"
#
#         reach = board.attacks(square)
#         if not G.IsNode(square):
#             label_dict_nodes[square] = str(square)
#             color_dict_nodes[square] = color
#             G.AddNode(square)
#             G.AddStrAttrDatN(square, color, "color")
#
#         # dont count sideways pawn attacks if there are no pieces there
#         if board.piece_at(square).piece_type == chess.PAWN:
#             reach_c = reach.copy()
#             for reachable_square in reach:
#                 if board.color_at(reachable_square) is None:
#                     reach_c.remove(reachable_square)
#             reach = reach_c
#
#         # pawn movement
#         if board.piece_at(square).piece_type == chess.PAWN:
#             sqr = chess.square_name(square)
#             for move in board.legal_moves:
#                 if chess.square_name(move.from_square) == sqr:  # and move.to_square not in reach:
#                     reach.add(move.to_square)
#
#             board.turn = not board.turn  # legalne poteze dobi samu stran na potezi, zatu obrnem kdu je na vrsti
#             for move in board.legal_moves:
#                 if chess.square_name(move.from_square) == sqr:  # and move.to_square not in reach:
#                     reach.add(move.to_square)
#             board.turn = not board.turn
#
#         for reachable_square in reach:
#             if board.color_at(reachable_square) is None:
#                 s_color = "none"
#             elif board.color_at(reachable_square):
#                 s_color = "white"
#             else:
#                 s_color = "black"
#
#             if not G.IsNode(reachable_square):
#                 label_dict_nodes[reachable_square] = str(reachable_square)
#                 color_dict_nodes[reachable_square] = s_color
#                 G.AddNode(reachable_square)
#                 G.AddStrAttrDatN(reachable_square, s_color, "color")
#
#             G.AddEdge(square, reachable_square)
#             edge = G.GetEI(square, reachable_square)
#             if s_color == color:
#                 type_dict_edges[edge.GetId()] = "defend"
#                 G.AddStrAttrDatE(edge.GetId(), "defend", "type")
#             else:
#                 type_dict_edges[edge.GetId()] = "attack"
#                 G.AddStrAttrDatE(edge.GetId(), "attack", "type")
#
#     G.SavePajek("networks/" + file + "/position_" + str(game_num) + "-" + str(move_num) + ".net",
#                 NIdLabelH=label_dict_nodes, NIdColorH=color_dict_nodes, EIdColorH=type_dict_edges)
#     f = open("networks/" + file + "/position_" + str(game_num) + "-" + str(move_num) + ".net", "a")
#     f.write("Result = " + result)
#     f.close()
#     return G
#

def create_dummy():

    G = create_placement_network()

    fen1 = "8/6k1/5pp1/3Q4/6K1/8/8/8 w - - 0 1"  # 1-0
    fen2 = "8/8/3p1k2/4b3/2Q5/3KP3/8/8 w - - 0 1"  # 1-0
    fen3 = "8/Q7/3p1k2/4b1pp/8/3K4/8/1R6 w - - 0 1"  # 1-0
    fen4 = "8/4k3/8/2q5/8/5N2/4P1K1/8 w - - 0 1"  # 0-1

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


def test():
    fen1 = "8/6k1/5pp1/3Q4/6K1/8/8/8 w - - 0 1"  # 1-0
    fen2 = "8/8/3p1k2/4b3/2Q5/3KP3/8/8 w - - 0 1"  # 1-0
    fen3 = "8/Q7/3p1k2/4b1pp/8/3K4/8/1R6 w - - 0 1"  # 1-0
    fen4 = "8/4k3/8/2q5/8/5N2/4P1K1/8 w - - 0 1"  # 0-1

    board1 = chess.Board(fen1)
    board2 = chess.Board(fen2)
    board3 = chess.Board(fen3)
    board4 = chess.Board(fen4)

    boards = [board1, board2, board3, board4]
    results = [1, 1, 1, -1]

    board_node = 0
    create_position_network(board1, board_node, color_separated=True)
