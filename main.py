from tkinter import *
from tksvg import SvgImage

length, width = 800, 1250
bLength, bWidth = 800, 800
tiles = 8

root = Tk()
root.title("Chess")

canvas = Canvas(height=length, width=width)

boardSetup = [
    ["bRook1", "bKnight1", "bBishop1", "bQueen1",
        "bKing1", "bBishop2", "bKnight2", "bRook2"],
    ["bPawn1", "bPawn2", "bPawn3", "bPawn4",
        "bPawn5", "bPawn6", "bPawn7", "bPawn8"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wPawn1", "wPawn2", "wPawn3", "wPawn4",
        "wPawn5", "wPawn6", "wPawn7", "wPawn8"],
    ["wRook1", "wKnight1", "wBishop1", "wQueen1",
        "wKing1", "wBishop2", "wKnight2", "wRook2"],
]

# boardSetup = [
#     ["", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", ""],
#     ["", "bBishop1", "bPawn1", "bQueen", "bRook1", "bKing", "", ""],
#     ["", "wBishop1", "wPawn1", "wQueen", "wRook1", "wKing", "", ""],
#     ["", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", ""],
# ]

# boardSetup = [
#     ["", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "wPawn1", ""],
#     ["", "", "", "", "", "", "", ""],
#     ["", "bPawn1", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", ""],
# ]

boardData = [
    [], [], [], [], [], [], [], []
]

takenPieces = [[], []]  # [black, white]

bPawn = SvgImage(file="sprites/black/pawn.svg", scale=2.25)
bKnight = SvgImage(file="sprites/black/knight.svg", scale=2.25)
bBishop = SvgImage(file="sprites/black/bishop.svg", scale=2.25)
bRook = SvgImage(file="sprites/black/rook.svg", scale=2.25)
bQueen = SvgImage(file="sprites/black/queen.svg", scale=2.25)
bKing = SvgImage(file="sprites/black/king.svg", scale=2.25)

wPawn = SvgImage(file="sprites/white/pawn.svg", scale=2.25)
wKnight = SvgImage(file="sprites/white/knight.svg", scale=2.25)
wBishop = SvgImage(file="sprites/white/bishop.svg", scale=2.25)
wRook = SvgImage(file="sprites/white/rook.svg", scale=2.25)
wQueen = SvgImage(file="sprites/white/queen.svg", scale=2.25)
wKing = SvgImage(file="sprites/white/king.svg", scale=2.25)

# (isHeld, piece, name, positions, moves, {other data})
heldPieceData = (False, None, "w", (0, 0), ([], []))
inCheck = False


def draw_square(x, y, size, color):
    canvas.create_rectangle(x, y, x + size, y + size,
                            fill=color, outline=color)


def rotate_board(board):
    for _ in range(2):
        board = list(reversed(list(zip(*board))))

    return board


def rotate_notation(position):  # position = chess notation
    x = ord(position[0]) - 97
    y = abs(int(position[1])) - 1

    x = (7 - x)
    y = (7 - y)

    letter = chr(x + 97)
    number = str(abs(y) + 1)

    return (letter + number)


def locate_piece(piece, board):
    for x, row in enumerate(board):
        for y, piece_ in enumerate(row):
            if piece_ == piece:
                return (x, y)


# direction = True when converting to chess notation, False when converting to board notation
def convert_notation(position, chess_notation=False):
    if (chess_notation):  # convert (a1, b2, c3, etc) to (0, 0), (1, 1), (2, 2), etc
        # see if the position is invalid (out of bounds)
        if (position[0] < 0 or position[0] > 7 or position[1] < 0 or position[1] > 7):
            return None
        
        x = position[0]
        y = position[1]

        letter = chr(x + 97)
        num = abs(y - 8)

        return (letter + str(num))
    else:  # convert (0, 0), (1, 1), (2, 2), etc to (a1, b2, c3, etc)
        print(position, "convert test 2")
        x = ord(position[0]) - 97
        y = abs(8 - int(position[1]))

        return (x, y)

def calculate_diagonal_moves(board, position):
    moves = []
    bishopMoves = [
            (1, 1), (1, -1), (-1, -1), (-1, 1)
        ]
    
    (xPos, yPos) = position

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

    return moves

def is_in_check(name, board, moves):
    kingPos = locate_piece(name, board)
    for move in moves:
        if (move == convert_notation(kingPos, True)):
            return True
    return False

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


def draw_moves(moves):
    rendered = []

    for move in moves:
        if move == None:
            continue

        loc = convert_notation(move, False)

        print(move, loc, "draw moves test")
        if(boardData[loc[0]][loc[1]] != ""):
            rended = canvas.create_oval(
                (loc[0] * 100)+5, (loc[1] * 100)+5, (loc[0] * 100) + 95, (loc[1] * 100) + 95, outline="gray80", width=5)
            rendered.append(rended)
        else:
            rended = canvas.create_oval((loc[0] * 100) + 25, (loc[1] * 100) + 25, (loc[0]
                                        * 100) + 75, (loc[1] * 100) + 75, fill="gray80", outline="lightgray")  # circle
            rendered.append(rended)

    return rendered


def on_mouse_click(event):
    global heldPieceData
    global test

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


def on_hover(event):
    global heldPieceData

    xPos = event.x // 100
    yPos = event.y // 100

    if (xPos > 7 or yPos > 7):  # out of bounds leaving the board
        return

    if (boardSetup[yPos][xPos] != ""):
        root.config(cursor="hand2")
    else:
        root.config(cursor="arrow")


for x in range(0, bLength, int(bLength/tiles)):
    for y in range(0, bWidth, int(bWidth/tiles)):
        xPos = x // 100
        yPos = y // 100

        draw_square(x, y, 100, "white" if (x + y) % 200 == 0 else "gray28")

        if (boardSetup[yPos][xPos] != ""):
            piece_name = boardSetup[yPos][xPos]

            if (piece_name[-1].isdigit()):
                piece_name = piece_name.replace(piece_name[-1], "")

            piece = canvas.create_image(
                x, y, image=globals()[piece_name], anchor=NW)
            boardData[xPos].append(piece)
        else:
            boardData[xPos].append("")

canvas.pack()

root.bind("<Button-1>", on_mouse_click)
root.bind("<Motion>", on_hover)

root.resizable(False, False)

root.mainloop()
