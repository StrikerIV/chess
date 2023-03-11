from globals import *

from func.draw_moves import *
from func.calculate_moves import *


def on_click(event):
    global heldPieceData

    x_pos = event.x // 100
    y_pos = event.y // 100

    if x_pos > 7 or y_pos > 7:  # out of bounds leaving the board
        return

    piece_id = boardData[x_pos][y_pos]
    piece_name = boardSetup[y_pos][x_pos]

    # (isHeld, piece, name, positions, moves)
    (holding, heldPieceId, heldPieceName, position, moves) = heldPieceData
    (moves, pieces) = moves


    if holding:  # a piece is currently being held
        if x_pos == position[0] and y_pos == position[1]:  # if the piece is being dropped on the same space it was picked up from
            return

        move_data = moves[[x[0] for i, x in enumerate(moves)].index(convert_notation((x_pos, y_pos), True))]  # get the move data
        print(move_data, "Data")  

        if boardSetup[y_pos][x_pos] != "":
            if boardSetup[y_pos][x_pos][0] == heldPieceName[0]:
                move_data = moves[[x[0] for i, x in enumerate(moves)].index(convert_notation((x_pos, y_pos), True))]  # get the move data

                if not move_data[1] == "castling":  # if the move is not a castle
                    # if they did, then set the held piece to that piece

                    # delete the previously rendered moves
                    for move in pieces:
                        canvas.delete(move)

                    # highlight the new piece
                    rendered_piece_background = canvas.create_rectangle(
                    # make the background yellow to indicate the piece is being held
                    (x_pos * 100), (y_pos * 100), (x_pos * 100) + 99, (y_pos * 100) + 99, fill="yellow", outline="yellow")

                    new_moves = calculate_moves((piece_id, piece_name), (x_pos, y_pos))  # calculate the new moves
                    new_rendered_moves = draw_moves(new_moves)  # render the new moves
                    new_rendered_moves.append(rendered_piece_background)  # add the background to the list of rendered moves

                    heldPieceData = (True, piece_id, piece_name, (x_pos, y_pos), (new_moves, new_rendered_moves))
                    canvas.tag_raise(piece_id)  # place the piece on top of the selection background

        if not moves:  # if the piece has moves
            return

        # check if they clicked on one of their own pieces

        if convert_notation((x_pos, y_pos), True) in [x[0] for i, x in enumerate(moves)]:  # if the piece is being dropped on a valid move (moving the piece)
            
            move_data = moves[[x[0] for i, x in enumerate(moves)].index(convert_notation((x_pos, y_pos), True))]  # get the move data
            
            if move_data[1] == "castling":  # if the move is a capture
                
                rook_loc = convert_notation(move_data[0], False) # get the rook data
                rook_id = boardData[rook_loc[0]][rook_loc[1]] # convert the rook data to the rook id
                rook_name = boardSetup[rook_loc[1]][rook_loc[0]] # convert the rook data to the rook name

                moved_pieces.append(heldPieceName)  # append to show the piece has been moved
                moved_pieces.append(rook_name)  # append to show the piece has been moved

                for move in pieces:  # delete the previously rendered moves as the piece has been moved
                    canvas.delete(move)

                canvas.delete(heldPieceId)  # delete the piece being held
                canvas.delete(rook_id)  # delete the rook being moved
                
                new_rook_id = canvas.create_image(((x_pos + 3) * 100), (y_pos * 100), image=globals()[rook_name.replace(rook_name[-1], "")], anchor=NW) # create the new rook image
                new_king_id = canvas.create_image(((x_pos + 2) * 100), (y_pos * 100), image=globals()[heldPieceName.replace(heldPieceName[-1], "")], anchor=NW) # create the new rook image

                # update the board data
                boardData[x_pos + 2][y_pos] = new_king_id
                boardData[x_pos + 3][y_pos] = new_rook_id
                boardSetup[y_pos][x_pos + 2] = heldPieceName
                boardSetup[y_pos][x_pos + 3] = rook_name

                boardData[x_pos][y_pos] = ""
                boardData[x_pos + 4][y_pos] = "" 
                boardSetup[y_pos][x_pos] = ""
                boardSetup[y_pos][x_pos + 4] = ""

                new_color = "w" if heldPieceName[0] == "b" else "b"
                heldPieceData = (False, "", new_color, (0, 0), ([], []))  # reset the held piece data

            else:
                moved_pieces.append(heldPieceName)  # append to show the piece has been moved

                for move in pieces:  # delete the previously rendered moves as the piece has been moved
                    canvas.delete(move)

                canvas.delete(heldPieceId)  # delete the piece being held

                if boardSetup[y_pos][
                    x_pos] != "":  # if the space the piece is being dropped on is occupied (taking a piece)
                    canvas.delete(boardData[x_pos][y_pos])  # delete the piece to be taken
                    takenPieces.append(boardSetup[y_pos][
                                        x_pos])  # add the piece to the taken pieces list

                boardData[x_pos][y_pos] = boardData[position[0]][
                    position[1]]  # move the piece to the new location in the board data
                boardData[position[0]][position[1]] = ""  # remove the piece from the old location in the board data

                boardSetup[y_pos][x_pos] = boardSetup[position[1]][
                    position[0]]  # move the piece to the new location in the board setup
                boardSetup[position[1]][position[0]] = ""  # remove the piece from the old location in the board setup

                # create the new piece
                held_piece_sprite_name = heldPieceName.replace(heldPieceName[-1], '')
                new_piece_id = canvas.create_image((x_pos * 100), (y_pos * 100), image=globals()[held_piece_sprite_name],
                                                anchor=NW)

                boardData[x_pos][y_pos] = new_piece_id  # add the new piece to the board data

                # raise the piece to the top of the canvas
                canvas.tag_raise(new_piece_id)

                new_color = "w" if heldPieceName[0] == "b" else "b"

                heldPieceData = (False, "", new_color, (0, 0), ([], []))  # reset the held piece data

    # pick up a piece
    elif boardSetup[y_pos][x_pos] != "":  # if the space clicked on is a piece (not empty)
        print("here??")
        if piece_name[0] == heldPieceName[0]:  # if the color is of the player's piece

            rendered_piece_background = canvas.create_rectangle(
                # make the background yellow to indicate the piece is being held
                (x_pos * 100), (y_pos * 100), (x_pos * 100) + 99, (y_pos * 100) + 99, fill="yellow", outline="yellow")

            moves = calculate_moves((piece_id, piece_name), (x_pos, y_pos))

            rendered_moves = draw_moves(moves)
            rendered_moves.append(rendered_piece_background)

            heldPieceData = (True, piece_id, piece_name,
                             (x_pos, y_pos), (moves, rendered_moves))  # update the held piece data

            canvas.tag_raise(piece_id)  # place the piece on top of the selection background

    else:
        return
