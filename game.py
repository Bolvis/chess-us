import os
import pieces

ILLEGAL_MOVE_MESSAGE = "illegal move"
COLOR_UNDEFINED_MESSAGE = "color undefined"
EMPTY_FIELD_MESSAGE = "empty field"
INVALID_SELECTION = "Invalid selection!"
CANT_PARSE = "Can't parse position"
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


def fail(message: str):
    clear()
    print(pieces.red(message))


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
            fail(CANT_PARSE)
            continue

        selected_piece = board.fields[piece_position.x][piece_position.y]
        if not isinstance(selected_piece, pieces.Piece) or selected_piece.color != player:
            fail(INVALID_SELECTION)
            continue

        target = input("select target position->")
        target_position, success = parse_position(target)
        if not success:
            fail(CANT_PARSE)
            continue

        if not board.is_path_free(selected_piece, target_position) and not isinstance(selected_piece, pieces.Knight):
            fail(ILLEGAL_MOVE_MESSAGE)
            continue

        target_field = board.fields[target_position.x][target_position.y]
        if not isinstance(target_field, pieces.EmptyField) and isinstance(selected_piece, pieces.Pawn):
            if not selected_piece.legal_move(target_position, True):
                fail(ILLEGAL_MOVE_MESSAGE)
                continue
        elif not selected_piece.legal_move(target_position):
            fail(ILLEGAL_MOVE_MESSAGE)
            continue

        board.fields[target_position.x][target_position.y] = selected_piece
        board.fields[piece_position.x][piece_position.y] = pieces.EmptyField(piece_position.x, piece_position.y)
        player = BLACK if player == WHITE else WHITE
