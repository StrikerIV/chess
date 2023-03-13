from globals import *

def convert_notation(position, chess_notation=False): # chess_notation = True when converting (0, 7) to "a1", chess_notation = False when converting "a1" to (0, 7)
    if chess_notation:
        (x, y) = position

        letter = chr((x) + 97)
        number = abs(y)

        return letter + str(number)
    else:
        letter = position[0]
        number = position[1]

        x = ord(letter) - 97
        y = int(number)

        return (x, y)
