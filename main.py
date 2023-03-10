from globals import *

from events.on_hover import on_hover
from events.on_mouse_click import on_click

from func.draw_moves import draw_square

for x in range(0, bLength, int(bLength/tiles)):
    for y in range(0, bWidth, int(bWidth/tiles)):
        xPos = x // 100
        yPos = y // 100

        draw_square(x, y, 100, "white" if (x + y) % 200 == 0 else "gray28")

        if boardSetup[yPos][xPos] != "":
            piece_name = boardSetup[yPos][xPos]

            if piece_name[-1].isdigit():
                piece_name = piece_name.replace(piece_name[-1], "")

            piece = canvas.create_image(
                x, y, image=globals()[piece_name], anchor=NW)
            boardData[xPos].append(piece)
        else:
            boardData[xPos].append("")

canvas.pack()

root.title("Chess")
root.bind("<Button-1>", on_click)
root.bind("<Motion>", on_hover)

root.resizable(False, False)

root.mainloop()
