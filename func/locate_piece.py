from globals import boardData, boardSetup
from func.convert_notation import convert_notation

def locate_piece(piece):
    for x, row in enumerate(boardSetup):
        for y, piece_ in enumerate(row):
            if piece_ == piece:
                return (convert_notation((y, x), True), boardData[x][y])