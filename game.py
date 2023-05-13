import os
import pieces

ILLEGAL_MOVE_MESSAGE = "illegal move"
COLOR_UNDEFINED_MESSAGE = "color undefined"
EMPTY_FIELD_MESSAGE = "empty field"
CANT_PARSE = "Can't parse position"
INVALID_SELECTION = "Invalid selection!"
WHITE = pieces.Color.WHITE
BLACK = pieces.Color.BLACK


def clear():
    os.system("cls || clear")


def parse_position(input_str) -> (pieces.Position, bool):
    columns = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    try:
        column = columns[input_str[0].lower()]
        row = int(input_str[1]) - 1
        if 0 <= row <= 7:
            return pieces.Position(row, column), True
        else:
            print(INVALID_SELECTION)
            return None, False
    except (KeyError, IndexError, ValueError):
        print(INVALID_SELECTION)
        return None, False


def play():
    clear()
    board = pieces.Board()
    player = WHITE
    while True:
        print(f"{player.value} turn")
        board.print_board()

        piece = input("select piece->")
        piece_position, success = parse_position(piece)
        if not success:
            clear()
            print(CANT_PARSE)
            continue

        selected_piece = board.fields[piece_position.x][piece_position.y]
        if not isinstance(selected_piece, pieces.Pawn) or selected_piece.color != player:
            clear()
            print(INVALID_SELECTION)
            continue

        target = input("select target position->")
        target_position, success = parse_position(target)
        if not success:
            clear()
            print(CANT_PARSE)
            continue

        clear()
        if selected_piece.legal_move(target_position):
            board.fields[target_position.x][target_position.y] = selected_piece
            board.fields[piece_position.x][piece_position.y] = pieces.EmptyField(piece_position.x, piece_position.y)
            player = BLACK if player == WHITE else WHITE
        else:
            print(ILLEGAL_MOVE_MESSAGE)
