from globals import canvas

def unrender_moves(moves):
    for move in moves:
        canvas.delete(move)
        