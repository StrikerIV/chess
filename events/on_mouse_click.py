from globals import *

from func.calculate_moves import *
from func.select_piece import select_piece
from func.deselect_piece import deselect_piece
from func.locate_piece import locate_piece
from func.move_piece import move_piece, castle
from func.unrender_moves import unrender_moves

def on_click(event):
    global boardSetup, boardData, heldPieceData, rendered_moves

    x_pos = event.x // 100
    y_pos = event.y // 100

    if x_pos > 7 or y_pos > 7:  # out of bounds leaving the board
        return

    tile = convert_notation((x_pos, y_pos), True)
    print(tile, "clicked tile")
    (holding, holding_piece_name) = heldPieceData

    holding_piece_color = holding_piece_name[0]

    for x in range(0, 8):
        for y in range(0, 8):
            piece_id = boardData[y][x]
            piece_name = boardSetup[y][x]
            
            if piece_id == "":
                continue
            
            moves = calculate_moves((piece_id, piece_name), (x, y))
            available_moves[piece_name] = moves

    if holding:
        piece_name = boardSetup[y_pos][x_pos]
        castling = False

        if available_moves[holding_piece_name] != []: # check if attempting to castle
            move = [move for move in available_moves[holding_piece_name] if tile in move[0]]
            
            if move != []:
                move = move[0]
                if "castle" in move[1] if type(move[1]) == list else move[1]:
                    castling = True

        if not piece_name == "" and holding_piece_color == piece_name[0] and castling == False: # swap pieces
            
            heldPieceData = deselect_piece(rendered_moves) # deselect the piece

            piece_data = select_piece(tile) # select the new piece

            heldPieceData = piece_data[0]
            rendered_moves = piece_data[1]
        else:
            move = [move for move in available_moves[holding_piece_name] if tile in move[0]][0]
            (move, move_type) = move

            if any(tile in move[0] for move in available_moves[holding_piece_name]):
                if boardSetup[y_pos][x_pos] == "" and castling == False:
                    held_piece_tile = locate_piece(holding_piece_name)

                    unrender_moves(rendered_moves) # unrender all moves
                    
                    (boardData, boardSetup) = move_piece(held_piece_tile, tile, move[1]) # move from held piece to tile
                    
                    heldPieceData = (False, "b" if heldPieceData[1][0] == "w" else "w")
                else:
                    if "castle" in move_type:
                        king_tile = locate_piece(holding_piece_name)

                        #unrender_moves(rendered_moves)

                        #(boardData, boardSetup) = castle(held_piece_tile, tile, move[1])
                    else:
                        print("capture")
    else:
        # pick up a piece
        piece_name = boardSetup[y_pos][x_pos]
        
        if piece_name == "":
            return
        
        if piece_name[0] == heldPieceData[1][0]:
            piece_data = select_piece(tile)

            heldPieceData = piece_data[0]
            rendered_moves = piece_data[1]

    # TODO: check if the king is in check
    current_turn = heldPieceData[1]

    if holding:
        king_moves = []

        if current_turn == "w": # white's turn, see if white is in check
            king_moves = available_moves["wKing1"]
        else:
            king_moves = available_moves["bKing1"]
        
        print(king_moves)
