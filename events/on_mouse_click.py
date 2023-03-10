from globals import *

from func.draw_moves import *
from func.calculate_moves import *


def on_click(event):
    global heldPieceData

    x_pos = event.x // 100
    y_pos = event.y // 100

    piece_id = boardData[x_pos][y_pos]
    piece_name = boardSetup[y_pos][x_pos]
    print(piece_name, "name of piece")
    # (isHeld, piece, name, positions, moves)
    (holding, heldPieceId, heldPieceName, position, moves) = heldPieceData

    if x_pos > 7 or y_pos > 7:  # out of bounds leaving the board
        return

    if holding:  # a piece is currently being held
        if x_pos == position[0] and y_pos == position[1]:  # if the piece is being dropped on the same space it was picked up from
            return

        if not moves[0]:  # if the piece has moves
            return

        # check if they clicked on one of their own pieces
        if boardSetup[y_pos][x_pos] != "":
            if boardSetup[y_pos][x_pos][0] == heldPieceName[0]:
                # if they did, then set the held piece to that piece
                print("SWAP PIECE")

        if convert_notation((x_pos, y_pos), True) in moves[
            0]:  # if the piece is being dropped on a valid move (moving the piece)

            moved_pieces.append(heldPieceName)  # append to show the piece has been moved
            print(moved_pieces, "moved pieces")

            for move in moves[1]:  # delete the previously rendered moves as the piece has been moved
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

            # before the turn is over, check if the king is in check
            moved_piece_moves = calculate_moves((new_piece_id, heldPieceName), (x_pos, y_pos))

            for move in moved_piece_moves:

                if move is None:
                    continue

                loc = convert_notation(move, False)

                if boardSetup[loc[1]][loc[0]] == new_color + "King1":
                    # render a red circle around the king to indicate it is in check
                    canvas.create_oval(
                        (loc[0] * 100) + 5, (loc[1] * 100) + 5, (loc[0] * 100) + 95, (loc[1] * 100) + 95, outline="red",
                        width=5)
                    break

            heldPieceData = (False, "", new_color, (0, 0), ([], []))  # reset the held piece data

    # pick up a piece
    elif boardSetup[y_pos][x_pos] != "":  # if the space clicked on is a piece (not empty)
        if piece_name[0] == heldPieceName[0]:  # if the color is of the player's piece

            rendered_piece_background = canvas.create_rectangle(
                # make the background yellow to indicate the piece is being held
                (x_pos * 100), (y_pos * 100), (x_pos * 100) + 100, (y_pos * 100) + 100, fill="yellow", outline="yellow")

            moves = calculate_moves((piece_id, piece_name), (x_pos, y_pos))
            rendered_moves = draw_moves(moves)
            rendered_moves.append(rendered_piece_background)

            heldPieceData = (True, piece_id, piece_name,
                             (x_pos, y_pos), (moves, rendered_moves))  # update the held piece data

            canvas.tag_raise(piece_id)  # place the piece on top of the selection background
    else:
        return
