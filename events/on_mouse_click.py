from globals import *

from func.draw_moves import *
from func.calculate_moves import *

def on_click(event):
    global heldPieceData
    
    xPos = event.x // 100
    yPos = event.y // 100

    pieceId = boardData[xPos][yPos]
    pieceName = boardSetup[yPos][xPos]

    # (isHeld, piece, name, positions, moves)
    (holding, heldPieceId, heldPieceName, position, moves) = heldPieceData

    if (xPos > 7 or yPos > 7):  # out of bounds leaving the board
        return

    if (holding):  # a piece is currently being held
        print(heldPieceData, "held piece after holding")
        if (xPos == position[0] and yPos == position[1]):  # if the piece is being dropped on the same space it was picked up from
            return

        if (moves[0] == []):  # if the piece has moves
            return

        # check if they clicked on one of their own pieces
        if (boardSetup[yPos][xPos] != ""):
            if (boardSetup[yPos][xPos][0] == heldPieceName[0]):
                # if they did, then set the held piece to that piece
                print("SWAP PIECE")

        if (convert_notation((xPos, yPos), True) in moves[0]):  # if the piece is being dropped on a valid move (moving the piece)
            for move in moves[1]:  # delete the previously rendered moves as the piece has been moved
                canvas.delete(move)
            
            canvas.delete(heldPieceId) # delete the piece being held

            if (boardSetup[yPos][xPos] != ""):  # if the space the piece is being dropped on is occupied (taking a piece)
                canvas.delete(boardData[xPos][yPos])  # delete the piece to be taken
                takenPieces.append(boardSetup[yPos][xPos])  # add the piece to the taken pieces list                                  

            boardData[xPos][yPos] = boardData[position[0]][position[1]]  # move the piece to the new location in the board data
            boardData[position[0]][position[1]] = ""  # remove the piece from the old location in the board data

            boardSetup[yPos][xPos] = boardSetup[position[1]][position[0]]  # move the piece to the new location in the board setup
            boardSetup[position[1]][position[0]] = "" # remove the piece from the old location in the board setup

            # create the new piece
            heldPieceSpriteName = heldPieceName.replace(heldPieceName[-1], '')
            newPieceId = canvas.create_image((xPos * 100), (yPos * 100), image=globals()[heldPieceSpriteName], anchor=NW)
            boardData[xPos][yPos] = newPieceId  # add the new piece to the board data

            # raise the piece to the top of the canvas
            canvas.tag_raise(newPieceId)

            newColor = "w" if heldPieceName[0] == "b" else "b"

            # before the turn is over, check if the king is in check
            movedPieceMoves = calculate_moves((newPieceId, heldPieceName), (xPos, yPos))

            for move in movedPieceMoves:

                if (move == None):
                    continue

                loc = convert_notation(move, False)

                if (boardSetup[loc[1]][loc[0]] == newColor + "King1"):
                    # render a red circle around the king to indicate it is in check
                    canvas.create_oval(
                (loc[0] * 100)+5, (loc[1] * 100)+5, (loc[0] * 100) + 95, (loc[1] * 100) + 95, outline="red", width=5)
                    break
            heldPieceData = (False, "", newColor, (0, 0), ([], []))  # reset the held piece data

    # pick up a piece
    elif (boardSetup[yPos][xPos] != ""):  # if the space clicked on is a piece (not empty)
        if (pieceName[0] == heldPieceName[0]):  # if the color is of the player's piece

            rendered_piece_background = canvas.create_rectangle(  # make the background yellow to indicate the piece is being held
                (xPos * 100), (yPos * 100), (xPos * 100) + 100, (yPos * 100) + 100, fill="yellow", outline="yellow")
            
            moves = calculate_moves((pieceId, pieceName), (xPos, yPos))
            rendered_moves = draw_moves(moves)
            rendered_moves.append(rendered_piece_background)

            heldPieceData = (True, pieceId, pieceName,
                             (xPos, yPos), (moves, rendered_moves))  # update the held piece data

            canvas.tag_raise(pieceId)  # place the piece on top of the selection background
    else:
        return