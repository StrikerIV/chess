from globals import *

from func.locate_piece import locate_piece
from func.convert_notation import convert_notation
from func.move_piece import move_piece

def capture_piece(piece_data, tile): # piece takes on tile (assume the move is valid)
    print(piece_data[0], "is taking on", tile)
    
    (piece_tile, taking_id) = piece_data
    (taken_x, taken_y) = convert_notation(tile)

    # delete the piece on the tile, then move the piece
    taken_id = boardData[taken_y][taken_x]
    
    canvas.delete(taken_id)

    
    return move_piece(piece_data, tile)

    