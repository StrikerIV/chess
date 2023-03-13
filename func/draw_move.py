from globals import canvas, boardData

from func.convert_notation import convert_notation


def draw_move(move):

    (move, capture) = move
    (x, y) = convert_notation(move, False)
    rendered = []
    
    if "-m" not in capture if type(capture) == str else False or capture == True:
        rendered = canvas.create_oval(
            (x * 100)+5, (y * 100)+5, (x * 100) + 95, (y * 100) + 95, outline="gray80", width=5)
    else: # normal move
        rendered = canvas.create_oval((x * 100) + 25, (y * 100) + 25, (x
                                    * 100) + 75, (y * 100) + 75, fill="gray80", outline="lightgray")  # circle


    return rendered


def draw_square(x, y, size, color):
    canvas.create_rectangle(x, y, x + size, y + size,
                            fill=color, outline=color)

