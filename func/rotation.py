from func.convert_notation import convert_notation

def rotate_notation(position):  # position = chess notation
    # 180 degree rotation of the given chess position (e.g. "a1" -> "h8")
    (x, y) = convert_notation(position)
    (x, y) = (7 - x, 7 - y)

    return convert_notation((x, y),  True)
    
    
    


def rotate_board(board):
    for _ in range(2):
        board = list(reversed(list(zip(*board))))

    return board

