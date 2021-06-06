import snap
import chess
import chess.svg
import chess.pgn
import networkx as nx

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