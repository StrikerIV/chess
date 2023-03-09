from tkinter import *
from tksvg import SvgImage

length, width = 800, 1250
bLength, bWidth = 800, 800
tiles = 8

root = Tk()
root.title("Chess")

canvas = Canvas(height=length, width=width)

# boardSetup = [
#     ["bRook", "bKnight", "bBishop", "bQueen", "bKing", "bBishop", "bKnight", "bRook"],
#     ["bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn", "bPawn"],
#     ["", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", ""],
#     ["wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn", "wPawn"],
#     ["wRook", "wKnight", "wBishop", "wQueen", "wKing", "wBishop", "wKnight", "wRook"],
# ]

boardSetup = [
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "bBishop", "bPawn", "bQueen", "", "", "", ""],
    ["", "wBishop", "wPawn", "wQueen", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
]

boardData = [
    [], [], [], [], [], [], [], []
]

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

heldPiece = (False, None, None, (0, 0), ([], [])) # (isHeld, piece, name, positions, moves)
test = None

def draw_square(x, y, size, color):
    canvas.create_rectangle(x, y, x + size, y + size, fill=color, outline=color)

def calculate_diagonals(position, depth, color):
    (xPos, yPos) = position

    moves = []

    for i in range(1, depth+1):     # top left diagonal
        if(xPos-i >= 0 and yPos-i >= 0 and boardSetup[yPos-i][xPos-i] == ""):
            moves.append((xPos-i, yPos-i))
        else:
            if(xPos-i >= 0 and yPos-i >= 0 and boardSetup[yPos-i][xPos-i][0] != color):
                moves.append((xPos-i, yPos-i, True))
            break
    
    for i in range(1, depth+1):     # top right diagonal
        if(xPos+i <= 7 and yPos-i >= 0 and boardSetup[yPos-i][xPos+i] == ""):
            moves.append((xPos+i, yPos-i))
        else:
            if(xPos+i <= 7 and yPos-i >= 0 and boardSetup[yPos-i][xPos+i][0] != color):
                moves.append((xPos+i, yPos-i, True))
            break

    for i in range(1, depth+1):     # bottom left diagonal
        if(xPos-i >= 0 and yPos+i <= 7 and boardSetup[yPos+i][xPos-i] == ""):
            moves.append((xPos-i, yPos+i))
        else:
            if(xPos-i >= 0 and yPos+i <= 7 and boardSetup[yPos+i][xPos-i][0] != color):
                moves.append((xPos-i, yPos+i, True))
            break
            
    for i in range(1, depth+1):     # bottom right diagonal
        if(xPos+i <= 7 and yPos+i <= 7 and boardSetup[yPos+i][xPos+i] == ""):
            moves.append((xPos+i, yPos+i))
        else:
            if(xPos+i <= 7 and yPos+i <= 7 and boardSetup[yPos+i][xPos+i][0] != color):
                moves.append((xPos+i, yPos+i, True))
            break
            
    return moves

def calculate_rows(position, depth):
    (xPos, yPos) = position
    print(position, "position")

    leftMoves = []
    rightMoves = []
    upMoves = []
    downMoves = []

    for i in range(1, depth+1):     # left
        if(xPos-i >= 0 and boardSetup[yPos][xPos-i] == ""):
            leftMoves.append((xPos-i, yPos))
        else:
            break
    
    for i in range(1, depth+1):     # right
        if(xPos+i <= 7 and boardSetup[yPos][xPos+i] == ""):
            rightMoves.append((xPos+i, yPos))
        else:
            break

    for i in range(1, depth+1):     # up
        if(yPos-i >= 0 and boardSetup[yPos-i][xPos] == ""):
            upMoves.append((xPos, yPos-i))
        else:
            break
    
    for i in range(1, depth+1):     # down
        if(yPos+i <= 7 and boardSetup[yPos+i][xPos] == ""):
            downMoves.append((xPos, yPos+i))
        else:
            break

    rowMoves = leftMoves + rightMoves
    columnMoves = upMoves + downMoves

    return (rowMoves, columnMoves)



def calculate_moves(pieceData, position):
    moves = []

    (piece, name) = pieceData
    (xPos, yPos) = position

    if(name == "wPawn" or name == "bPawn"): # pawn
        if(name == "wPawn"):
            print(position, boardSetup[yPos-1][xPos])
            if(boardSetup[yPos-1][xPos] == ""):
                moves.append((xPos, yPos-1))
            if(boardSetup[yPos-1][xPos+1][0] != name[0]): 
                moves.append((xPos-1, yPos-1, True)) # true means it's an attack move
            if(boardSetup[yPos-1][xPos-1][0] != name[0]):
                moves.append((xPos+1, yPos-1, True)) # true means it's an attack move
        else:
            if(boardSetup[yPos+1][xPos] == ""):
                moves.append((xPos, yPos+1))
            if(boardSetup[yPos+1][xPos+1][0] != name[0]): 
                moves.append((xPos-1, yPos+1, True))
            if(boardSetup[yPos+1][xPos-1][0] != name[0]):
                moves.append((xPos+1, yPos+1, True))

    # if(name == "wKnight" or name == "bKnight"): # knight
        

    if(name == "wBishop" or name == "bBishop"): # bishop
        moves = calculate_diagonals(position, 7, name[0])

    if(name == "wRook" or name == "bRook"): # rook
        calculated_moves = calculate_rows(position, 7)
        moves = calculated_moves[0] + calculated_moves[1]
            
    if(name == "wQueen" or name == "bQueen"): # queen
        calculated_moves = calculate_rows(position, 7)
        moves = calculated_moves[0] + calculated_moves[1]
        moves += calculate_diagonals(position, 7, name[0])
    
    if(name == "wKing" or name == "bKing"): # king
        if(name == "wKing"):
            if(yPos-1 >= 0):
                if(boardSetup[yPos-1][xPos] == ""):
                    moves.append((xPos, yPos-1))
                if(xPos-1 >= 0):
                    if(boardSetup[yPos-1][xPos-1] == ""):
                        moves.append((xPos-1, yPos-1))
                if(xPos+1 <= 7):
                    if(boardSetup[yPos-1][xPos+1] == ""):
                        moves.append((xPos+1, yPos-1))
            if(yPos+1 <= 7):
                if(boardSetup[yPos+1][xPos] == ""):
                    moves.append((xPos, yPos+1))
                if(xPos-1 >= 0):
                    if(boardSetup[yPos+1][xPos-1] == ""):
                        moves.append((xPos-1, yPos+1))
                if(xPos+1 <= 7):
                    if(boardSetup[yPos+1][xPos+1] == ""):
                        moves.append((xPos+1, yPos+1))
            if(xPos-1 >= 0):
                if(boardSetup[yPos][xPos-1] == ""):
                    moves.append((xPos-1, yPos))
            if(xPos+1 <= 7):
                if(boardSetup[yPos][xPos+1] == ""):
                    moves.append((xPos+1, yPos))
        else: # black king
            if(yPos-1 >= 0):
                if(boardSetup[yPos-1][xPos] == ""):
                    moves.append((xPos, yPos-1))
                if(xPos-1 >= 0):
                    if(boardSetup[yPos-1][xPos-1] == ""):
                        moves.append((xPos-1, yPos-1))
                if(xPos+1 <= 7):
                    if(boardSetup[yPos-1][xPos+1] == ""):
                        moves.append((xPos+1, yPos-1))
            if(yPos+1 <= 7):
                if(boardSetup[yPos+1][xPos] == ""):
                    moves.append((xPos, yPos+1))
                if(xPos-1 >= 0):
                    if(boardSetup[yPos+1][xPos-1] == ""):
                        moves.append((xPos-1, yPos+1))
                if(xPos+1 <= 7):
                    if(boardSetup[yPos+1][xPos+1] == ""):
                        moves.append((xPos+1, yPos+1))
            if(xPos-1 >= 0):
                if(boardSetup[yPos][xPos-1] == ""):
                    moves.append((xPos-1, yPos))
            if(xPos+1 <= 7):
                if(boardSetup[yPos][xPos+1] == ""):
                    moves.append((xPos+1, yPos))

    return moves
        

def draw_moves(moves):
    rendered = []

    for move in moves:
        try:
            _ = move[2]
            rended = canvas.create_oval((move[0] * 100)+5, (move[1] * 100)+5, (move[0] * 100) + 95, (move[1] * 100) + 95, outline="gray80", width=5)
            rendered.append(rended)
        except IndexError: # 
            rended = canvas.create_oval((move[0] * 100) + 25, (move[1] * 100) + 25, (move[0] * 100) + 75, (move[1] * 100) + 75, fill="gray80", outline="lightgray") # circle
            rendered.append(rended)

    return rendered

def on_mouse_click(event):
    global heldPiece
    global test

    xPos = event.x // 100
    yPos = event.y // 100
    
    piece = boardData[xPos][yPos]
    name = boardSetup[yPos][xPos]

    if(piece != "" and heldPiece[0] == False):
        print("here")
        if(heldPiece[0] == True): # a piece is currently selected
            moves = heldPiece[4]
            for move in moves[1]:
                canvas.delete(move)

        if (name != ""):
            moves = calculate_moves((piece, name), (xPos, yPos))
            rendered_moves = draw_moves(moves)
            rendered_piece = canvas.create_rectangle((xPos * 100), (yPos * 100), (xPos * 100) + 100, (yPos * 100) + 100, fill="yellow", outline="yellow") # make the background yellow
            rendered_moves.append(rendered_piece)

            canvas.tag_raise(piece) # bring the piece to the top

            heldPiece = (True, piece, name, (xPos, yPos), (moves, rendered_moves))
    
    if(heldPiece[0] == True):
        print("here2")
        if((xPos, yPos) in heldPiece[4][0]): # if the move is valid

            canvas.delete(heldPiece[1])
            
            boardSetup[heldPiece[3][1]][heldPiece[3][0]] = ""
            boardSetup[yPos][xPos] = heldPiece[2]
            boardData[xPos][yPos] = canvas.create_image(xPos * 100, yPos * 100, image=globals()[heldPiece[2]], anchor=NW)

            for move in heldPiece[4][1]:
                canvas.delete(move)

            heldPiece = (False, None, None, (0, 0), ([], [])) # (isHeld, piece, name, positions, moves)
        else: # make the selected piece the new selected piece
            print("here3")
            for move in heldPiece[4][1]:
                canvas.delete(move)

            moves = calculate_moves((piece, name), (xPos, yPos))
            rendered_moves = draw_moves(moves)
            rendered_piece = canvas.create_rectangle((xPos * 100), (yPos * 100), (xPos * 100) + 100, (yPos * 100) + 100, fill="yellow", outline="yellow") # make the background yellow
            rendered_moves.append(rendered_piece)

            canvas.tag_raise(piece) # bring the piece to the top

            heldPiece = (True, piece, name, (xPos, yPos), (moves, rendered_moves))


def on_hover(event):
    global heldPiece

    xPos = event.x // 100
    yPos = event.y // 100

    if(xPos > 7 or yPos > 7): # out of bounds leaving the board
        return
    
    if(boardSetup[yPos][xPos] != ""):
        root.config(cursor="hand2")
    else:
        root.config(cursor="arrow")
    

for x in range(0, bLength, int(bLength/tiles)):
    for y in range (0, bWidth, int(bWidth/tiles)):
        xPos = x // 100
        yPos = y // 100

        draw_square(x, y, 100, "gray28" if (x + y) % 200 == 0 else "white")

        if(boardSetup[yPos][xPos] != ""):
            piece = canvas.create_image(x, y, image=globals()[boardSetup[yPos][xPos]], anchor=NW)
            boardData[xPos].append(piece)
        else:
            boardData[xPos].append("")

canvas.pack()

root.bind("<Button-1>", on_mouse_click)
root.bind("<Motion>", on_hover)

root.resizable(False, False)

root.mainloop()