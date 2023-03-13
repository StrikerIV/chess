from globals import heldPieceData, boardData, boardSetup, canvas, available_moves

from func.convert_notation import convert_notation
from func.draw_move import draw_move

def select_piece(tile):
    global heldPieceData

    (x, y) = convert_notation(tile, False)

    piece_id = boardData[y][x]
    piece_name = boardSetup[y][x]

    moves = available_moves[piece_name]

    piece_background = canvas.create_rectangle((x * 100), (y * 100), (x * 100) + 100, (y * 100) + 100, fill="yellow", outline="yellow")
    rendered_moves = [piece_background]
    
    for move in moves:
        rendered = draw_move(move)
        rendered_moves.append(rendered)
    
    canvas.tag_raise(piece_id)

    return ((True, piece_name), rendered_moves)