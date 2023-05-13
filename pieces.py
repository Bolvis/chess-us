from enum import Enum

from game import ILLEGAL_MOVE_MESSAGE, EMPTY_FIELD_MESSAGE


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

        print(ILLEGAL_MOVE_MESSAGE)
        return False


class Knight(Pawn):
    def legal_move(self, position: Position) -> bool:
        if abs(self.position.x - position.x) == 2 and abs(self.position.y - position.y) == 1:
            return self.position.move(position.x, position.y)
        elif abs(self.position.x - position.x) == 1 and abs(self.position.y - position.y) == 2:
            return self.position.move(position.x, position.y)
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
            return self.position.move(new_x, new_y)
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
            return self.position.move(new_x, new_y)
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
            return self.position.move(new_x, new_y)
        else:
            print(ILLEGAL_MOVE_MESSAGE)
            return False


class EmptyField(Pawn):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, Color.EMPTY)

    def legal_move(self, position: Position) -> bool:
        print(EMPTY_FIELD_MESSAGE)
        return False

