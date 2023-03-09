from tkinter import *
from tksvg import SvgImage

length, width = 800, 1250
bLength, bWidth = 800, 800
tiles = 8

root = Tk()
root.title("Chess")

canvas = Canvas(height=length, width=width)

boardSetup = [
    ["bRook1", "bKnight1", "bBishop1", "bQueen", "bKing", "bBishop2", "bKnight2", "bRook2"],
    ["bPawn1", "bPawn2", "bPawn3", "bPawn4", "bPawn5", "bPawn6", "bPawn7", "bPawn8"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wPawn1", "wPawn2", "wPawn3", "wPawn4", "wPawn5", "wPawn6", "wPawn7", "wPawn8"],
    ["wRook1", "wKnight1", "wBishop1", "wQueen", "wKing", "wBishop2", "wKnight2", "wRook2"],
]

# boardSetup = [
#     ["", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", ""],
#     ["", "bBishop", "bPawn", "bQueen", "bRook", "bKing", "", ""],
#     ["", "wBishop", "wPawn", "wQueen", "wRook", "wKing", "", ""],
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

# (isHeld, piece, name, positions, moves)
heldPiece = (False, None, "w", (0, 0), ([], []))
test = None


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

    print(x, y, "rotate test before")
    x = (7 - x)
    y = (7 - y)

    letter = chr(x + 97)
    number = str(abs(y - 8))
    
    print(x, y, letter, number, "rotate test after")
    
    return(letter + number)

    

def locate_piece(piece, board):
    for x, row in enumerate(board):
        for y, piece_ in enumerate(row):
            if piece_ == piece:
                return(x, y)
        
def convert_notation(position, chess_notation = False): # direction = True when converting to chess notation, False when converting to board notation
    if(chess_notation): # convert (a1, b2, c3, etc) to (0, 0), (1, 1), (2, 2), etc
        x = position[0]
        y = position[1]
        
        letter = chr(x + 97)
        num = abs(y - 8)
        
        return(letter + str(num))
    else: # convert (0, 0), (1, 1), (2, 2), etc to (a1, b2, c3, etc)
        print(position, "convert test 2")
        x = ord(position[0]) - 97
        y = abs(7 - int(position[1])) + 1 # add 1 to account for 0 indexing
        
        return(x, y)


def calculate_moves(pieceData, position):
    board = boardSetup
    black = False
    
            # for move in moves:
            # move = rotate_notation(move) # orient the moves to the board
    moves = []

    (piece, name) = pieceData
    (xPos, yPos) = position
    
    if(name[0] == "b"):
        board = rotate_board(board)
        xPos, yPos = (7 - xPos, 7 - yPos)

    if("bPawn" in name or "wPawn" in name): # calculate pawn moves woop woop
        if(board[yPos - 1][xPos] == ""): # if the space in front of the pawn is empty (always check this first)
            moves.append(convert_notation((xPos, yPos - 1), True))
        
        if(yPos == 6 and board[yPos - 2][xPos] == ""): # if the pawn is on the starting row, and the space 2 in front of it is empty
            moves.append(convert_notation((xPos, yPos - 2), True))

        
    if(name[0] == "b"):
        new_moves = []
        
        for move in moves:
            print("rotating!")
            new_moves.append(rotate_notation(move)) # orient the moves to the board
        
        print(new_moves)
        return new_moves
    else:
        return moves



def draw_moves(moves):
    rendered = []

    for move in moves:
        loc = convert_notation(move, False)
        try:
            _ = move[2]
            rended = canvas.create_oval(
                (loc[0] * 100)+5, (loc[1] * 100)+5, (loc[0] * 100) + 95, (loc[1] * 100) + 95, outline="gray80", width=5)
            rendered.append(rended)
        except IndexError:
            rended = canvas.create_oval((loc[0] * 100) + 25, (loc[1] * 100) + 25, (loc[0]
                                        * 100) + 75, (loc[1] * 100) + 75, fill="gray80", outline="lightgray")  # circle
            rendered.append(rended)

    return rendered


def on_mouse_click(event):
    global heldPiece
    global test

    xPos = event.x // 100
    yPos = event.y // 100

    piece = boardData[xPos][yPos]
    name = boardSetup[yPos][xPos]

    if (piece != "" and heldPiece[0] == False):

        if (heldPiece[0] == True):  # a piece is currently selected
            moves = heldPiece[4]

            for move in moves[1]:
                canvas.delete(move)

        if (name != ""):
            moves = calculate_moves((piece, name), (xPos, yPos))
            rendered_moves = draw_moves(moves)
            rendered_piece = canvas.create_rectangle((xPos * 100), (yPos * 100), (xPos * 100) + 100, (
                yPos * 100) + 100, fill="yellow", outline="yellow")  # make the background yellow
            rendered_moves.append(rendered_piece)

            canvas.tag_raise(piece)  # bring the piece to the top

            heldPiece = (True, piece, name, (xPos, yPos),
                         (moves, rendered_moves))

    if (heldPiece[0] == True):
        if ((xPos, yPos) in heldPiece[4][0]):  # if the move is valid

            canvas.delete(heldPiece[1])

            boardSetup[heldPiece[3][1]][heldPiece[3][0]] = ""
            boardSetup[yPos][xPos] = heldPiece[2]
            boardData[xPos][yPos] = canvas.create_image(
                xPos * 100, yPos * 100, image=globals()[heldPiece[2]], anchor=NW)

            for move in heldPiece[4][1]:
                canvas.delete(move)

            # (isHeld, piece, name, positions, moves)
            heldPiece = (False, None, None, (0, 0), ([], []))
        else:  # make the selected piece the new selected piece
            # take the piece
            if (heldPiece[0] == True and heldPiece[1] != piece and name[0] != heldPiece[2][0]):
                canvas.delete(piece)

                if (name[0] == "b"):
                    takenPieces[0].append(name)
                else:
                    takenPieces[0].append(name)

                # move the piece to the taken piece
                canvas.delete(heldPiece[1])

                boardSetup[heldPiece[3][1]][heldPiece[3][0]] = ""
                boardSetup[yPos][xPos] = heldPiece[2]
                boardData[xPos][yPos] = canvas.create_image(
                    xPos * 100, yPos * 100, image=globals()[heldPiece[2]], anchor=NW)

                for move in heldPiece[4][1]:
                    canvas.delete(move)

                # (isHeld, piece, name, positions, moves)
                heldPiece = (False, None, None, (0, 0), ([], []))

            else:
                for move in heldPiece[4][1]:
                    canvas.delete(move)

                moves = calculate_moves((piece, name), (xPos, yPos))
                rendered_moves = draw_moves(moves)
                rendered_piece = canvas.create_rectangle((xPos * 100), (yPos * 100), (xPos * 100) + 100, (
                    yPos * 100) + 100, fill="yellow", outline="yellow")  # make the background yellow
                rendered_moves.append(rendered_piece)

                canvas.tag_raise(piece)  # bring the piece to the top

                heldPiece = (True, piece, name, (xPos, yPos),
                             (moves, rendered_moves))


def on_hover(event):
    global heldPiece

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
