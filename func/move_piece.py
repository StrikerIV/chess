from globals import *

from func.convert_notation import convert_notation
from func.unrender_moves import unrender_moves
from func.locate_piece import locate_piece

def move_piece(old, new, move_type=False): # old & new are chess notation, move the piece at old to new, assume the move is valid

    print("moving", old[0], "to", new)
    (old_pos, piece_id) = old
    
    old_pos = convert_notation(old_pos, False) # convert the old position to a tuple
    new_pos = convert_notation(new, False) # convert the new position to a tuple

    unrender_moves(rendered_moves) # unrender all moves
    canvas.delete(piece_id) # delete the piece at the old position

    old_x = old_pos[0]
    old_y = old_pos[1]

    new_x = new_pos[0]
    new_y = new_pos[1]

    print(boardSetup, "setup")
    piece_name = boardSetup[old_y][old_x] # get the piece name
    piece_sprite_name = piece_name.replace(piece_name[-1], "")

    moved_pieces.append(piece_name)

    if move_type == "enPassant":
        captured_pawn_id = boardData[new_y + 1][new_x]
        captured_pawn_name = boardSetup[new_y + 1][new_x]

        canvas.delete(captured_pawn_id) # delete captured pawn

        boardData[new_y + 1][new_x] = "" # no pawn anymore
        boardSetup[new_y + 1][new_x] = "" # no pawn anymore

        if captured_pawn_name[0] == "w":
            captured_pieces[1].append(captured_pawn_name)
        else:
            captured_pieces[0].append(captured_pawn_name)

    new_piece = canvas.create_image((new_x * 100) + 50, (new_y * 100) + 50, image=globals()[piece_sprite_name]) # create a new piece at the new position
    
    # update the board data
    boardData[old_y][old_x] = "" # good
    boardData[new_y][new_x] = new_piece

    boardSetup[old_y][old_x] = "" # good
    boardSetup[new_y][new_x] = piece_name

    return boardData, boardSetup


def castle(king, rook, flags): # castle the king and rook

    king_tile = locate_piece(king, True)
    rook_tile = locate_piece(rook, True)

    (king_tile, king_id) = king_tile
    (rook_tile, rook_id) = rook_tile

    (king_x, king_y) = (7, 2)
    (rook_x, rook_y) = (7, 3)

    if "-q" in flags:
        (king_x, king_y) = (7, 6)
        (rook_x, rook_y) = (7, 5)
        
    if king[0] == "b":
        king_x = abs(7 - king_x)
        rook_x = abs(7 - rook_x)

    canvas.delete(king_id)
    canvas.delete(rook_id)

    king_sprite_name = king.replace(king[-1], "")
    rook_sprite_name = rook.replace(rook[-1], "")

    new_king = canvas.create_image((king_y * 100) + 50, (king_x * 100) + 50,
                                    image=globals()[king_sprite_name])  # create a new piece at the new position

    new_rook = canvas.create_image((rook_y * 100) + 50, (rook_x * 100) + 50,
                                   image=globals()[rook_sprite_name])  # create a new piece at the new position

    moved_pieces.append(king)
    moved_pieces.append(rook)

    if not "-q" in flags: # update board for king side castle
        boardSetup[king_x][king_y + 2] = "" # good
        boardSetup[rook_x][rook_y - 3] = ""
        boardSetup[king_x][king_y] = king
        boardSetup[rook_x][rook_y] = rook

        boardData[king_x][king_y + 2] = "" # good
        boardData[rook_x][rook_y - 3] = ""
        boardData[king_x][king_y] = new_king
        boardData[rook_x][rook_y] = new_rook
    else:
        print("update board for queen-side castle")

    return boardData, boardSetup



