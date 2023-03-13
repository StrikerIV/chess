from tkinter import *
from tksvg import SvgImage

length, width = 799, 799
bLength, bWidth = 800, 800
tiles = 8

root = Tk()
canvas = Canvas(height=length, width=width)

boardSetup = [
    ["bRook1", "", "", "", "bKing1", "", "", "bRook2"],
    ["bPawn1", "bPawn2", "bPawn3", "bPawn4", "bPawn5", "bPawn6", "bPawn7", "bPawn8"],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["", "", "", "", "", "", "", ""],
    ["wPawn1", "wPawn2", "wPawn3", "wPawn4", "wPawn5", "wPawn6", "wPawn7", "wPawn8"],
    ["wRook1", "", "", "","wKing1", "", "", "wRook2"],
]



# boardSetup = [
#     ["", "", "", "", "", "", "", ""],
#     ["", "bPawn1", "", "", "", "", "", ""],
#     ["", "", "wPawn1", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", ""],
#     ["", "", "", "", "", "", "", ""],
# ]

boardData = [
    [], [], [], [], [], [], [], []
]

captured_pieces = [[], []]  # [black, white]
available_moves = {} # (piece, moves)
moved_pieces = []
rendered_moves = []

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

heldPieceData = (False, "w")  # (holding a piece, name of the piece) 
inCheck = False