import os

import chess
import chess.svg


def visualize_fen(board, path="boards", filename="board"):
    svg = chess.svg.board(board, size=350)
    with open(os.path.join(path, filename) + ".svg", 'w') as file:
        file.write(svg)
