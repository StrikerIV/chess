def locate_piece(piece, board):
    for x, row in enumerate(board):
        for y, piece_ in enumerate(row):
            if piece_ == piece:
                return x, y