def rotate_notation(position):  # position = chess notation
    x = ord(position[0]) - 97
    y = abs(int(position[1]))

    x = (7 - x)
    y = (7 - y)

    letter = chr(x + 97)
    number = str(abs(y))

    return letter + number


def rotate_board(board):
    for _ in range(2):
        board = list(reversed(list(zip(*board))))

    return board

