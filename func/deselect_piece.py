from globals import canvas, rendered_moves, heldPieceData
from func.unrender_moves import unrender_moves

def deselect_piece(rendered_moves):
    global heldPieceData

    (holding, holding_piece_name) = heldPieceData
    opposite_color = "b" if holding_piece_name[0] == "w" else "w"

    unrender_moves(rendered_moves) # unrender all moves
    
    return (False, opposite_color)
    