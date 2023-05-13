import os

from pieces import Rook, King, Color, Knight, Bishop, Pawn, Queen, EmptyField, Position

ILLEGAL_MOVE_MESSAGE = "illegal move"
COLOR_UNDEFINED_MESSAGE = "color undefined"
EMPTY_FIELD_MESSAGE = "empty field"


def green(text):
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(0, 255, 0, text)


def blue(text):
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(0, 0, 255, text)


class Board:
    def __init__(self):
        self.fields = [
            [Rook(0, 0, Color.WHITE), Knight(0, 1, Color.WHITE), Bishop(0, 2, Color.WHITE), Queen(0, 3, Color.WHITE),
             King(0, 4, Color.WHITE), Bishop(0, 5, Color.WHITE), Knight(0, 6, Color.WHITE), Rook(0, 7, Color.WHITE)],
            [Pawn(1, 0, Color.WHITE), Pawn(1, 1, Color.WHITE), Pawn(1, 2, Color.WHITE), Pawn(1, 3, Color.WHITE),
             Pawn(1, 4, Color.WHITE), Pawn(1, 5, Color.WHITE), Pawn(1, 6, Color.WHITE), Pawn(1, 7, Color.WHITE)],
            [EmptyField(2, y) for y in range(8)],
            [EmptyField(4, y) for y in range(8)],
            [EmptyField(3, y) for y in range(8)],
            [EmptyField(5, y) for y in range(8)],
            [Pawn(6, 0, Color.BLACK), Pawn(6, 1, Color.BLACK), Pawn(6, 2, Color.BLACK), Pawn(6, 3, Color.BLACK),
             Pawn(6, 4, Color.BLACK), Pawn(6, 5, Color.BLACK), Pawn(6, 6, Color.BLACK), Pawn(6, 7, Color.BLACK)],
            [Rook(7, 0, Color.BLACK), Knight(7, 1, Color.BLACK), Bishop(7, 2, Color.BLACK), Queen(7, 3, Color.BLACK),
             King(7, 4, Color.BLACK), Bishop(7, 5, Color.BLACK), Knight(7, 6, Color.BLACK), Rook(7, 7, Color.BLACK)]]

    def print_board(self):
        print("  A B C D E F G H")
        print("  ---------------")
        for row in range(8):
            print(row + 1, end="|")
            for col in range(8):
                piece = self.fields[row][col]
                if isinstance(piece, Rook):
                    match piece.color:
                        case Color.BLACK:
                            print(green("R"), end=" ")
                        case Color.WHITE:
                            print(blue("R"), end=" ")
                elif isinstance(piece, Knight):
                    match piece.color:
                        case Color.BLACK:
                            print(green("H"), end=" ")
                        case Color.WHITE:
                            print(blue("H"), end=" ")
                elif isinstance(piece, Bishop):
                    match piece.color:
                        case Color.BLACK:
                            print(green("B"), end=" ")
                        case Color.WHITE:
                            print(blue("B"), end=" ")
                elif isinstance(piece, Queen):
                    match piece.color:
                        case Color.BLACK:
                            print(green("Q"), end=" ")
                        case Color.WHITE:
                            print(blue("Q"), end=" ")
                elif isinstance(piece, King):
                    match piece.color:
                        case Color.BLACK:
                            print(green("K"), end=" ")
                        case Color.WHITE:
                            print(blue("K"), end=" ")
                elif isinstance(piece, EmptyField):
                    print("#", end=" ")
                elif isinstance(piece, Pawn):
                    match piece.color:
                        case Color.BLACK:
                            print(green("P"), end=" ")
                        case Color.WHITE:
                            print(blue("P"), end=" ")
                else:
                    print(" ", end=" ")
            print("|", row + 1)
        print("  ---------------")
        print("  A B C D E F G H")


def clear():
    os.system("cls || clear")


def parse_position(input_str) -> (Position, bool):
    columns = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    try:
        column = columns[input_str[0].lower()]
        row = int(input_str[1]) - 1
        if 0 <= row <= 7:
            return Position(row, column), True
        else:
            print("Invalid row.")
            return None, False
    except (KeyError, IndexError, ValueError):
        print("Invalid position.")
        return None, False


def play():
    clear()
    board = Board()
    player = Color.WHITE
    while True:
        print(f"{player.value} turn")
        board.print_board()

        piece = input("select piece->")
        piece_position, success = parse_position(piece)
        if not success:
            clear()
            print("Can't parse position")
            continue

        selected_piece = board.fields[piece_position.x][piece_position.y]
        if not isinstance(selected_piece, Pawn) or selected_piece.color != player:
            clear()
            print("Invalid piece selection!")
            continue

        target = input("select target position->")
        target_position, success = parse_position(target)
        if not success:
            clear()
            print("Can't parse position")
            continue

        clear()
        if selected_piece.legal_move(target_position):
            board.fields[target_position.x][target_position.y] = selected_piece
            board.fields[piece_position.x][piece_position.y] = EmptyField(piece_position.x, piece_position.y)
            player = Color.BLACK if player == Color.WHITE else Color.WHITE
        else:
            print(ILLEGAL_MOVE_MESSAGE)
