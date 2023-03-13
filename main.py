from globals import *

from events.on_hover import on_hover
from events.on_mouse_click import on_click

from func.draw_move import draw_square
from func.convert_notation import convert_notation

def main():
    global boardSetup, boardData, tiles, bLength, bWidth, canvas, root

    for x in range(0, bLength, int(bLength/tiles)):
        for y in range(0, bWidth, int(bWidth/tiles)):
            x_pos = x // 100
            y_pos = y // 100

            draw_square(x, y, 100, "white" if (x + y) % 200 == 0 else "gray28") # draw the tile
            
            # add letter and numbers to the tile
            
            tile = convert_notation((x_pos, y_pos), True)

            if(x_pos == 0): # add numbers
                canvas.create_text(x + 8, y + 3, text=tile[1], fill="gray28" if (x + y) % 200 == 0 else "white", anchor=NW, font=("Arial", 16))
            if(y_pos == 7): # add letters
                canvas.create_text((x + 100) - 8, (y + 100) - 3, text=tile[0], fill="gray28" if (x + y) % 200 == 0 else "white", anchor=SE, font=("Arial", 16))

            if boardSetup[y_pos][x_pos] != "":
                piece_name = boardSetup[y_pos][x_pos]

                if piece_name[-1].isdigit():
                    piece_name = piece_name.replace(piece_name[-1], "")

                piece = canvas.create_image(
                    x, y, image=globals()[piece_name], anchor=NW)

                boardData[y_pos].append(piece)
            else:
                boardData[y_pos].append("")
            

    canvas.pack()

    root.title("Chess")
    root.bind("<Button-1>", on_click)
    root.bind("<Motion>", on_hover)

    root.resizable(False, False)

    root.mainloop()

main()