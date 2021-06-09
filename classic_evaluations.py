import chess
import chess.svg
import chess.pgn


def shannon(games, results, progress=False, last_moves_percentage=1):
    X = []
    y = []
    game_num = 0
    board_node = 0
    for game in games:
        board = game.board()
        if results[game_num] == "white":
            result = 1
        elif results[game_num] == "black":
            result = 0 #-1
        else:
            result = 0

        if progress:
            print("Shannon game", game_num, "/", len(games) - 1)

        last_moves_n = 0
        for _ in game.mainline_moves():
            last_moves_n += 1
        last_moves_n = int(last_moves_n * (1 - last_moves_percentage))

        for move in game.mainline_moves():
            board.push(move)

            if last_moves_n > 0:
                last_moves_n -= 1
                continue

            y.append(result)
            score = 0
            if board.turn == chess.WHITE:
                score += 0.1 * board.legal_moves.count()
                board.turn = chess.BLACK
                score -= 0.1 * board.legal_moves.count()
                board.turn = chess.WHITE
            else:
                score -= 0.1 * board.legal_moves.count()
                board.turn = chess.WHITE
                score += 0.1 * board.legal_moves.count()
                board.turn = chess.BLACK

            white_pawn_files = [0 for _ in range(8)]
            black_pawn_files = [0 for _ in range(8)]
            for square in board.piece_map():
                piece = board.piece_at(square)
                if piece.symbol() == "q":
                    score -= 9
                elif piece.symbol() == "Q":
                    score += 9
                elif piece.symbol() == "r":
                    score -= 5
                elif piece.symbol() == "R":
                    score += 5
                elif piece.symbol() == "b":
                    score -= 3
                elif piece.symbol() == "B":
                    score += 3
                elif piece.symbol() == "n":
                    score -= 3
                elif piece.symbol() == "N":
                    score += 3
                elif piece.symbol() == "p":
                    score -= 1
                    if is_backward_black(square, board):
                        score += 0.5
                    black_pawn_files[chess.square_file(square)] += 1
                elif piece.symbol() == "P":
                    score += 1
                    if is_backward_white(square, board):
                        score -= 0.5
                    white_pawn_files[chess.square_file(square)] += 1

            score -= 0.5 * isolated_pawns(white_pawn_files)
            score += 0.5 * isolated_pawns(black_pawn_files)
            score -= 0.5 * doubled_pawns(white_pawn_files)
            score += 0.5 * doubled_pawns(black_pawn_files)

            X.append([score])
            board_node += 1
        game_num += 1

    return X, y


def doubled_pawns(file_list):
    count = 0
    for i in range(len(file_list)):
        if file_list[i] > 1:
            continue
        count += file_list[i]
    return count


def is_backward_white(square, board):
    square_file = chess.square_file(square)
    square_rank = chess.square_rank(square)
    if square_rank == 7:
        return False

    current_square = chess.square(square_file, square_rank + 1)
    piece = board.piece_at(current_square)
    if piece is not None and (piece.symbol() == "p" or piece.symbol() == "P"):
        return False

    if not board.is_attacked_by(chess.BLACK, current_square):
        return False

    if square_file == 0:
        file_range = [1]
    elif square_file == 7:
        file_range = [-1]
    else:
        file_range = [-1, 1]

    has_pawn_ahead = False
    for file in file_range:
        for rank in range(8):
            current_square = chess.square(square_file + file, rank)
            piece = board.piece_at(current_square)
            if piece is None or piece.symbol() != "P":
                continue
            if rank < square_rank:
                return False
            else:
                has_pawn_ahead = True
    if has_pawn_ahead:
        return True
    return False

def is_backward_black(square, board):
    square_file = chess.square_file(square)
    square_rank = chess.square_rank(square)

    if square_rank == 0:
        return False

    current_square = chess.square(square_file, square_rank - 1)
    piece = board.piece_at(current_square)
    if piece is not None and (piece.symbol() == "p" or piece.symbol() == "P"):
        return False

    if not board.is_attacked_by(chess.WHITE, current_square):
        return False

    if square_file == 0:
        file_range = [1]
    elif square_file == 7:
        file_range = [-1]
    else:
        file_range = [-1, 1]

    has_pawn_ahead = False
    for file in file_range:
        for rank in range(8):
            current_square = chess.square(square_file + file, rank)
            piece = board.piece_at(current_square)
            if piece is None or piece.symbol() != "p":
                continue
            if rank > square_rank:
                return False
            else:
                has_pawn_ahead = True
    if has_pawn_ahead:
        return True
    return False


def isolated_pawns(file_list):
    count = 0
    for i in range(len(file_list)):
        if file_list[i] < 1:
            continue
        if i != 0 and file_list[i - 1] > 0:
            continue
        if i != 7 and file_list[i + 1] > 0:
            continue
        count += 1
    return count
    # if square.square_file == 0:
    #     file_range = [1]
    # elif square.square_file == 7:
    #     file_range = [-1]
    # else:
    #     file_range = [-1, 1]
    # if square.rank_file == 0:
    #     rank_range = [0, 1]
    # elif square.rank_file == 7:
    #     rank_range = [-1, 0]
    # else:
    #     rank_range = [-1, 0, 1]
    #
    # for i in file_range:
    #     for j in rank_range:
    #         current_square = chess.square(square.square_file + i, square.rank_file + j)


def test():
    board = chess.Board("8/1p2p3/4p3/2p2p2/8/4P1P1/2P2P2/8 w - - 0 1")
    print(is_backward_white(chess.SQUARES[chess.square(5, 1)], board))
    print(is_backward_black(chess.SQUARES[chess.square(4, 6)], board))

