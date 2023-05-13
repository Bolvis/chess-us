from enum import Enum


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
            return False

        old_x = self.position.x
        new_x = position.x

        match self.color:
            case Color.BLACK:
                if (old_x == 6 and old_x - new_x <= 2) or old_x - new_x == 1:
                    return self.position.move(new_x, position.y)
            case Color.WHITE:
                if (old_x == 1 and new_x - old_x <= 2) or new_x - old_x == 1:
                    return self.position.move(new_x, position.y)
        return False


class Rook(Pawn):
    def legal_move(self, position: Position) -> bool:
        new_x = position.x
        old_x = self.position.x
        new_y = position.y
        old_y = self.position.y

        if old_x == new_x or old_y == new_y:
            return self.position.move(new_x, new_y)

        return False


class Knight(Pawn):
    def legal_move(self, position: Position) -> bool:
        if abs(self.position.x - position.x) == 2 and abs(self.position.y - position.y) == 1:
            return self.position.move(position.x, position.y)
        elif abs(self.position.x - position.x) == 1 and abs(self.position.y - position.y) == 2:
            return self.position.move(position.x, position.y)
        return False


class Bishop(Pawn):
    def legal_move(self, position: Position) -> bool:
        old_x = self.position.x
        new_x = position.x
        old_y = self.position.y
        new_y = position.y

        if abs(new_x - old_x) == abs(new_y - old_y):
            return self.position.move(new_x, new_y)
        return False


class Queen(Pawn):
    def legal_move(self, position: Position) -> bool:
        old_x = self.position.x
        new_x = position.x
        old_y = self.position.y
        new_y = position.y

        if old_x == new_x or old_y == new_y or abs(new_x - old_x) == abs(new_y - old_y):
            return self.position.move(new_x, new_y)
        return False


class King(Pawn):
    def legal_move(self, position: Position) -> bool:
        old_x = self.position.x
        new_x = position.x
        old_y = self.position.y
        new_y = position.y

        if abs(new_x - old_x) <= 1 and abs(new_y - old_y) <= 1:
            return self.position.move(new_x, new_y)
        return False


class EmptyField(Pawn):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, Color.EMPTY)

    def legal_move(self, position: Position) -> bool:
        return False


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
