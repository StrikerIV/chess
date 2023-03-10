from globals import *

def on_hover(event):
    xPos = event.x // 100
    yPos = event.y // 100

    if (xPos > 7 or yPos > 7):  # out of bounds leaving the board
        return

    if (boardSetup[yPos][xPos] != ""):
        root.config(cursor="hand2")
    else:
        root.config(cursor="arrow")
