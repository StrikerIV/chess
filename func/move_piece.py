from globals import *

from func.convert_notation import convert_notation
from func.unrender_moves import unrender_moves

def move_piece(old, new, type=False): # old & new are chess notation, move the piece at old to new, assume the move is valid

    (old_pos, piece_id) = old
    
    old_pos = convert_notation(old_pos, False) # convert the old position to a tuple
    new_pos = convert_notation(new, False) # convert the new position to a tuple

    unrender_moves(rendered_moves) # unrender all moves
    canvas.delete(piece_id) # delete the piece at the old position

    old_x = old_pos[0]
    old_y = old_pos[1]

    new_x = new_pos[0]
    new_y = new_pos[1]

    piece_name = boardSetup[old_y][old_x] # get the piece name
    piece_sprite_name = piece_name.replace(piece_name[-1], "")

    moved_pieces.append(piece_name)

    if type == "enPassant":
        captured_pawn_id = boardData[new_y + 1][new_x]
        captured_pawn_name = boardSetup[new_y + 1][new_x]

        canvas.delete(captured_pawn_id) # delete captured pawn

        boardData[new_y + 1][new_x] = "" # no pawn anymore
        boardSetup[new_y + 1][new_x] = "" # no pawn anymore

        if captured_pawn_name[0] == "w":
            captured_pieces[1].append(captured_pawn_name)
        else:
            captured_pieces[0].append(captured_pawn_name)

    if type == "castle":
        print("castle")    

    new_piece = canvas.create_image((new_x * 100) + 50, ((new_y) * 100) + 50, image=globals()[piece_sprite_name]) # create a new piece at the new position
    
    # update the board data
    boardData[old_y][old_x] = "" # good
    boardData[new_y][new_x] = new_piece

    boardSetup[old_y][old_x] = "" # good
    boardSetup[new_y][new_x] = piece_name

    return (boardData, boardSetup)

def castle(king, rook, flags): # castle the king and rook
    king_pos = convert_notation(king, False)
    rook_pos = convert_notation(rook, False)
