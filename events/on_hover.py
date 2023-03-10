from globals import *


def on_hover(event):
    x_pos = event.x // 100
    y_pos = event.y // 100

    if x_pos > 7 or y_pos > 7:  # out of bounds leaving the board
        return

    if boardSetup[y_pos][x_pos] != "":
        root.config(cursor="hand2")
    else:
        root.config(cursor="arrow")
