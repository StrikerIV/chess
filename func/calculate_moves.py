from globals import *

from func.rotation import rotate_board, rotate_notation
from func.convert_notation import convert_notation


def calculate_moves(piece_data, position):
    board = boardSetup

    # for move in moves:
    # move = rotate_notation(move) # orient the moves to the board
    moves = []

    (piece, name) = piece_data
    (xpos, ypos) = position

    if name[0] == "b":
        board = rotate_board(board)
        xpos, ypos = (7 - xpos, 7 - ypos)

    if "bPawn" in name or "wPawn" in name:  # calculate pawn moves

        # normal moves
        if board[ypos - 1][xpos] == "":  # if the space in front of the pawn is empty (always check this first)
            moves.append(convert_notation((xpos, ypos - 1), True))

        if ypos == 6 and board[ypos - 2][xpos] == "":  # if the pawn is on the starting row, and the space 2 in front of it is empty
            moves.append(convert_notation((xpos, ypos - 2), True))

        # attack moves 
        if xpos > 0 and board[ypos - 1][xpos - 1] != "" and board[ypos - 1][xpos - 1][0] != name[0]:
            moves.append(convert_notation((xpos - 1, ypos - 1), True))

        if xpos < 7 and board[ypos - 1][xpos + 1] != "" and board[ypos - 1][xpos + 1][0] != name[0]:
            moves.append(convert_notation((xpos + 1, ypos - 1), True))

    if "bKnight" in name or "wKnight" in name:  # calculate knight moves (find an algorithm for this)
        knight_moves = [
            (1, 2), (2, 1), (2, -1), (1, -2),
            (-1, -2), (-2, -1), (-2, 1), (-1, 2)
        ]

        for i in range(8):
            tx = xpos + knight_moves[i][0]
            ty = ypos + knight_moves[i][1]

            if 0 <= tx <= 7 and 0 <= ty <= 7:
                if board[ty][tx] == "":
                    moves.append(convert_notation((tx, ty), True))
                elif board[ty][tx][0] != name[0]:
                    moves.append(convert_notation((tx, ty), True))

    if "bBishop" in name or "wBishop" in name or "bQueen" in name or "wQueen" in name: # calculate bishop moves and queen moves (since they move the same way)
        bishop_moves = [
            (1, 1), (1, -1), (-1, -1), (-1, 1)
        ]

        for i in range(4):
            tx = xpos
            ty = ypos

            while True:
                tx += bishop_moves[i][0]
                ty += bishop_moves[i][1]

                if 0 <= tx <= 7 and 0 <= ty <= 7:
                    if board[ty][tx] == "":
                        moves.append(convert_notation((tx, ty), True))
                    elif board[ty][tx][0] != name[0]:
                        moves.append(convert_notation((tx, ty), True))
                        break
                    else:
                        break
                else:
                    break
    
    if "bRook" in name or "wRook" in name or "bQueen" in name or "wQueen" in name: # calculate rook moves and queen moves (since they move the same way)
        rook_moves = [
            (1, 0), (0, 1), (-1, 0), (0, -1)
        ]

        for i in range(4):
            tx = xpos
            ty = ypos

            while True:
                tx += rook_moves[i][0]
                ty += rook_moves[i][1]

                if 0 <= tx <= 7 and 0 <= ty <= 7:
                    if board[ty][tx] == "":
                        moves.append(convert_notation((tx, ty), True))
                    elif board[ty][tx][0] != name[0]:
                        moves.append(convert_notation((tx, ty), True))
                        break
                    else:
                        break
                else:
                    break

    if "bKing" in name or "wKing" in name:  # calculate king moves as the last step
        king_moves = [
            (1, 1), (1, -1), (-1, -1), (-1, 1),
            (1, 0), (0, 1), (-1, 0), (0, -1)
        ]

        for i in range(8):
            tx = xpos + king_moves[i][0]
            ty = ypos + king_moves[i][1]

            if 0 <= tx <= 7 and 0 <= ty <= 7:
                if board[ty][tx] == "":
                    moves.append(convert_notation((tx, ty), True))
                elif board[ty][tx][0] != name[0]:
                    moves.append(convert_notation((tx, ty), True))
               
    if name[0] == "b": # rotate the moves back to the original board (for the black pieces)
        new_moves = []

        for move in moves:
            new_moves.append(rotate_notation(move))  # orient the moves to the board

        return new_moves
    else:
        return moves
