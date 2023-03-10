def convert_notation(position, chess_notation=False): # chess_notation = True when converting (0, 0), (1, 1), (2, 2), etc to (a1, b2, c3, etc, False is in reverse
    if chess_notation:  # convert (a1, b2, c3, etc) to (0, 0), (1, 1), (2, 2), etc
        if position[0] < 0 or position[0] > 7 or position[1] < 0 or position[1] > 7:  # see if the position is invalid (out of bounds)
            return None
        
        x = position[0]
        y = position[1]

        letter = chr(x + 97)
        num = abs(y - 8)

        return letter + str(num)
    else:  # convert (0, 0), (1, 1), (2, 2), etc to (a1, b2, c3, etc)
        print(position, "convert test 2")
        x = ord(position[0]) - 97
        y = abs(8 - int(position[1]))

        return x, y