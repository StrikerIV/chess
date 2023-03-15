from globals import *

from func.calculate_moves import *
from func.select_piece import select_piece
from func.deselect_piece import deselect_piece
from func.locate_piece import locate_piece
from func.move_piece import move_piece, castle
from func.unrender_moves import unrender_moves
from func.capture_piece import capture_piece

def on_click(event):
    global boardSetup, boardData, heldPieceData, rendered_moves

    x_pos = event.x // 100
    y_pos = event.y // 100

    if x_pos > 7 or y_pos > 7:  # out of bounds leaving the board
        return

    tile = convert_notation((x_pos, y_pos), True)

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

        if available_moves[holding_piece_name]:  # check if attempting to castle
            move = [move for move in available_moves[holding_piece_name]
                    if tile in move[0]]

            if move:
                move = move[0]
                if "castle" in move[1] if type(move[1]) == list else move[1]:
                    castling = True

        # swap pieces
        if not piece_name == "" and holding_piece_color == piece_name[0] and castling == False:

            heldPieceData = deselect_piece(
                rendered_moves)  # deselect the piece

            piece_data = select_piece(tile)  # select the new piece

            heldPieceData = piece_data[0]
            rendered_moves = piece_data[1]
        else:
            move = [move for move in available_moves[holding_piece_name] if tile in move[0]]

            if not move:
                return
            
            (move, move_type) = move[0]

            if any(tile in move[0] for move in available_moves[holding_piece_name]):
                if boardSetup[y_pos][x_pos] == "" and castling == False:
                    held_piece_tile = locate_piece(holding_piece_name)

                    unrender_moves(rendered_moves)  # unrender all moves

                    (boardData, boardSetup) = move_piece(held_piece_tile,
                                                         tile, move[1])  # move from held piece to tile

                    heldPieceData = (
                        False, "b" if heldPieceData[1][0] == "w" else "w")
                else:
                    if type(move_type) == str and "castle" in move_type: # castling of the kings
                        x_offset = 0

                        if "-q" in move_type:
                            if "-m" in move_type:  # queen-side middle square,
                                x_offset = 1
                            else:  # queen-side rook square
                                x_offset = 0
                        else:  # king-side castle
                            if "-m" in move_type:
                                x_offset = -2

                        rook_name = boardSetup[y_pos][x_pos + x_offset]

                        unrender_moves(rendered_moves)

                        (boardData, boardSetup) = castle(
                            holding_piece_name, rook_name, move_type)

                        heldPieceData = (
                            False, "b" if heldPieceData[1][0] == "w" else "w")
                    elif type(move_type) == str and move_type == "enPassant": # en passant for pawns
                        held_piece_tile = locate_piece(holding_piece_name)

                        unrender_moves(rendered_moves)  # unrender all moves

                        (boardData, boardSetup) = move_piece(held_piece_tile,
                                                            tile, move_type)  # move from held piece to tile

                        heldPieceData = (
                            False, "b" if heldPieceData[1][0] == "w" else "w")
                    else: # take the piece!
                        held_piece_tile = locate_piece(holding_piece_name)

                        (t_x, t_y) = convert_notation(tile)
                        taken_piece_name = boardSetup[t_y][t_x]

                        unrender_moves(rendered_moves)  # unrender all moves
                        
                        (boardData, boardSetup) = capture_piece(held_piece_tile, tile)

                        if taken_piece_name[0] == "w":
                            captured_pieces[1].append(taken_piece_name)
                        else:
                            captured_pieces[0].append(taken_piece_name)

                        heldPieceData = (
                            False, "b" if heldPieceData[1][0] == "w" else "w")
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

    if holding:
        king = ""
        if holding_piece_name[0] == "b":
            king = "wKing1"
        else:
            king = "bKing1"

        king_moves = available_moves[king]
        king_tile = locate_piece(king)

        # loop through all available moves on the board
        for piece in available_moves:
            moves = available_moves[piece]

            for move in moves:
                if move in king_moves:
                    # remove move as it would put the king in check
                    print(f"move {move} is invalid for kind")
                elif king_tile in king_moves:
                    print(f"king is in check with move {king_tile} by piece {piece}")