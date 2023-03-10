from globals import canvas, boardData

from func.convert_notation import convert_notation


def draw_moves(moves):
    rendered = []

    for move in moves:
        if move is None:
            continue

        loc = convert_notation(move, False)

        if boardData[loc[0]][loc[1]] != "":
            rendered_move = canvas.create_oval(
                (loc[0] * 100)+5, (loc[1] * 100)+5, (loc[0] * 100) + 95, (loc[1] * 100) + 95, outline="gray80", width=5)
            rendered.append(rendered_move)
        else:
            rendered_capture = canvas.create_oval((loc[0] * 100) + 25, (loc[1] * 100) + 25, (loc[0]
                                        * 100) + 75, (loc[1] * 100) + 75, fill="gray80", outline="lightgray")  # circle
            rendered.append(rendered_capture)

    return rendered


def draw_square(x, y, size, color):
    canvas.create_rectangle(x, y, x + size, y + size,
                            fill=color, outline=color)

