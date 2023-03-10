from globals import *

from func.rotation import rotate_board, rotate_notation
from func.convert_notation import convert_notation

def calculate_moves(pieceData, position):
    board = boardSetup

    # for move in moves:
    # move = rotate_notation(move) # orient the moves to the board
    moves = []

    (piece, name) = pieceData
    (xPos, yPos) = position

    if (name[0] == "b"):
        board = rotate_board(board)
        xPos, yPos = (7 - xPos, 7 - yPos)

    if ("bPawn" in name or "wPawn" in name):  # calculate pawn moves

        # normal moves
        if (board[yPos - 1][xPos] == ""):  # if the space in front of the pawn is empty (always check this first)
            moves.append(convert_notation((xPos, yPos - 1), True))

        if (yPos == 6 and board[yPos - 2][xPos] == ""):  # if the pawn is on the starting row, and the space 2 in front of it is empty
            moves.append(convert_notation((xPos, yPos - 2), True))

        # attack moves 
        if (xPos > 0 and board[yPos - 1][xPos - 1] != "" and board[yPos - 1][xPos - 1][0] != name[0]):
            moves.append(convert_notation((xPos - 1, yPos - 1), True))

        if (xPos < 7 and board[yPos - 1][xPos + 1] != "" and board[yPos - 1][xPos + 1][0] != name[0]):
            moves.append(convert_notation((xPos + 1, yPos - 1), True))

    if ("bKnight" in name or "wKnight" in name):  # calculate knight moves (find an algorithm for this)
        knightMoves = [
            (1, 2), (2, 1), (2, -1), (1, -2),
            (-1, -2), (-2, -1), (-2, 1), (-1, 2)
        ]

        for i in range(8):
            tX = xPos + knightMoves[i][0]
            tY = yPos + knightMoves[i][1]

            if (tX >= 0 and tX <= 7 and tY >= 0 and tY <= 7):
                if (board[tY][tX] == ""):
                    moves.append(convert_notation((tX, tY), True))
                elif (board[tY][tX][0] != name[0]):
                    moves.append(convert_notation((tX, tY), True))

    if ("bBishop" in name or "wBishop" in name or "bQueen" in name or "wQueen" in name): # calculate bishop moves and queen moves (since they move the same way)
        bishopMoves = [
            (1, 1), (1, -1), (-1, -1), (-1, 1)
        ]

        for i in range(4):
            tX = xPos
            tY = yPos

            while (True):
                tX += bishopMoves[i][0]
                tY += bishopMoves[i][1]

                if (tX >= 0 and tX <= 7 and tY >= 0 and tY <= 7):
                    if (board[tY][tX] == ""):
                        moves.append(convert_notation((tX, tY), True))
                    elif (board[tY][tX][0] != name[0]):
                        moves.append(convert_notation((tX, tY), True))
                        break
                    else:
                        break
                else:
                    break
    
    if ("bRook" in name or "wRook" in name or "bQueen" in name or "wQueen" in name): # calculate rook moves and queen moves (since they move the same way)
        rookMoves = [
            (1, 0), (0, 1), (-1, 0), (0, -1)
        ]

        for i in range(4):
            tX = xPos
            tY = yPos

            while (True):
                tX += rookMoves[i][0]
                tY += rookMoves[i][1]

                if (tX >= 0 and tX <= 7 and tY >= 0 and tY <= 7):
                    if (board[tY][tX] == ""):
                        moves.append(convert_notation((tX, tY), True))
                    elif (board[tY][tX][0] != name[0]):
                        moves.append(convert_notation((tX, tY), True))
                        break
                    else:
                        break
                else:
                    break

    if ("bKing" in name or "wKing" in name):  # calculate king moves as the last step
        kingMoves = [
            (1, 1), (1, -1), (-1, -1), (-1, 1),
            (1, 0), (0, 1), (-1, 0), (0, -1)
        ]

        for i in range(8):
            tX = xPos + kingMoves[i][0]
            tY = yPos + kingMoves[i][1]

            if (tX >= 0 and tX <= 7 and tY >= 0 and tY <= 7):
                if (board[tY][tX] == ""):
                    moves.append(convert_notation((tX, tY), True))
                elif (board[tY][tX][0] != name[0]):
                    moves.append(convert_notation((tX, tY), True))
               
    if (name[0] == "b"): # rotate the moves back to the original board (for the black pieces)
        new_moves = []

        for move in moves:
            new_moves.append(rotate_notation(move))  # orient the moves to the board

        return new_moves
    else:
        return moves
