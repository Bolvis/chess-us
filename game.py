import os
from enum import Enum

ILLEGAL_MOVE_MESSAGE = "illegal move"
COLOR_UNDEFINED_MESSAGE = "color undefined"
EMPTY_FIELD_MESSAGE = "empty field"


class Color(Enum):
    BLACK = "black"
    WHITE = "white"
    EMPTY = "empty"


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self, x: int, y: int) -> bool:
        if 0 > x > 8 or 0 > y > 8:
            print(ILLEGAL_MOVE_MESSAGE)
            return False
        self.x = x
        self.y = y
        return True


class Pawn:
    def __init__(self, x: int, y: int, color: Color):
        self.position = Position(x, y)
        self.color = color

    def legal_move(self, position: Position) -> bool:
        if self.position.y != position.y:
            print(ILLEGAL_MOVE_MESSAGE)
            return False

        old_x = self.position.x
        new_x = position.x

        match self.color:
            case Color.BLACK:
                if old_x == 7 and old_x - new_x <= 2:
                    return position.move(new_x, position.y)
                else:
                    print(ILLEGAL_MOVE_MESSAGE)
            case Color.WHITE:
                if old_x == 1 and new_x - old_x <= 2:
                    return position.move(new_x, position.y)
                else:
                    print(ILLEGAL_MOVE_MESSAGE)
            case _:
                print(COLOR_UNDEFINED_MESSAGE)
        return False


class Rook(Pawn):
    def legal_move(self, position: Position) -> bool:
        new_x = position.x
        old_x = self.position.x
        new_y = position.y
        old_y = self.position.y

        if old_x == new_x or old_y == new_y:
            return position.move(new_x, new_y)

        print(ILLEGAL_MOVE_MESSAGE)
        return False


class Knight(Pawn):
    def legal_move(self, position: Position) -> bool:
        if abs(self.position.x - position.x) == 2 and abs(self.position.y - position.y) == 1:
            return position.move(position.x, position.y)
        elif abs(self.position.x - position.x) == 1 and abs(self.position.y - position.y) == 2:
            return position.move(position.x, position.y)
        else:
            print(ILLEGAL_MOVE_MESSAGE)
            return False


class Bishop(Pawn):
    def legal_move(self, position: Position) -> bool:
        old_x = self.position.x
        new_x = position.x
        old_y = self.position.y
        new_y = position.y

        if abs(new_x - old_x) == abs(new_y - old_y):
            return position.move(new_x, new_y)
        else:
            print(ILLEGAL_MOVE_MESSAGE)
            return False


class Queen(Pawn):
    def legal_move(self, position: Position) -> bool:
        old_x = self.position.x
        new_x = position.x
        old_y = self.position.y
        new_y = position.y

        if old_x == new_x or old_y == new_y or abs(new_x - old_x) == abs(new_y - old_y):
            return position.move(new_x, new_y)
        else:
            print(ILLEGAL_MOVE_MESSAGE)
            return False


class King(Pawn):
    def legal_move(self, position: Position) -> bool:
        old_x = self.position.x
        new_x = position.x
        old_y = self.position.y
        new_y = position.y

        if abs(new_x - old_x) <= 1 and abs(new_y - old_y) <= 1:
            return position.move(new_x, new_y)
        else:
            print(ILLEGAL_MOVE_MESSAGE)
            return False


class EmptyField(Pawn):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, Color.EMPTY)

    def legal_move(self, position: Position) -> bool:
        print(EMPTY_FIELD_MESSAGE)
        return False


def green(text):
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(0, 255, 0, text)


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
                    print(green("R") if piece.color == Color.BLACK else "R", end=" ")
                elif isinstance(piece, Knight):
                    print(green("H") if piece.color == Color.BLACK else "H", end=" ")
                elif isinstance(piece, Bishop):
                    print(green("B") if piece.color == Color.BLACK else "B", end=" ")
                elif isinstance(piece, Queen):
                    print(green("Q") if piece.color == Color.BLACK else "Q", end=" ")
                elif isinstance(piece, King):
                    print(green("K") if piece.color == Color.BLACK else "K", end=" ")
                elif isinstance(piece, EmptyField):
                    print("#", end=" ")
                elif isinstance(piece, Pawn):
                    print(green("P") if piece.color == Color.BLACK else "P", end=" ")
                else:
                    print(" ", end=" ")
            print("|", row + 1)
        print("  ---------------")
        print("  A B C D E F G H")


def clear():
    os.system("cls || clear")


def parse_position(input_str) -> Position:
    columns = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}
    try:
        column = columns[input_str[0].lower()]
        row = int(input_str[1]) - 1
        if 0 <= row <= 7:
            return Position(row, column)
        else:
            print("Invalid row.")
            return None
    except (KeyError, IndexError, ValueError):
        print("Invalid position.")
        return None


def is_valid_position(position: Position, board: Board) -> bool:
    return True


def play():
    board = Board()
    player = Color.WHITE
    while True:
        print(f"{player} turn")
        board.print_board()
        piece = input("select piece->")
        piece_position = parse_position(piece)
        if not is_valid_position(piece_position, board):
            print("Invalid position!")
            continue
        selected_piece = board.fields[piece_position.x][piece_position.y]
        if not isinstance(selected_piece, Pawn) or selected_piece.color != player:
            print("Invalid piece selection!")
            continue
        target = input("select target position->")
        target_position = parse_position(target)
        if not is_valid_position(target_position, board):
            print("Invalid position!")
            continue
        if selected_piece.legal_move(target_position):
            board.fields[target_position.x][target_position.y] = selected_piece
            board.fields[piece_position.x][piece_position.y] = EmptyField(piece_position.x, piece_position.y)
            player = Color.BLACK if player == Color.WHITE else Color.WHITE
        clear()


play()
