from abc import abstractmethod
from enum import Enum

import print_util


class Color(Enum):
    WHITE = "green"
    BLACK = "red"
    EMPTY = "empty"


class Position:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def move(self, x: int, y: int, dry: bool = False) -> bool:
        if 0 > x > 8 or 0 > y > 8:
            return False
        if not dry:
            self.x = x
            self.y = y
        return True


class Piece:
    def __init__(self, x: int, y: int, color: Color):
        self.position = Position(x, y)
        self.color = color

    @abstractmethod
    def legal_move(self, position: Position, dry: bool = False) -> bool:
        if position.x == self.position.x and position.y == self.position.y:
            return False


class Pawn(Piece):
    def legal_move(self, position: Position, dry: bool = False, attack: bool = False) -> bool:
        super()
        old_y = self.position.y
        new_y = position.y
        old_x = self.position.x
        new_x = position.x

        if (new_y != old_y and not attack) or (attack and abs(old_y - new_y) != 1):
            return False

        start = 1 if self.color == Color.WHITE else 6
        direction = 1 if self.color == Color.WHITE else -1
        if (old_x == start and (new_x - start == 2 * direction or new_x - start == 1 * direction) and not attack) \
                or new_x - old_x == direction:
            return self.position.move(new_x, new_y, dry)

        return False


class Rook(Piece):
    def legal_move(self, position: Position, dry: bool = False) -> bool:
        super()
        new_x = position.x
        old_x = self.position.x
        new_y = position.y
        old_y = self.position.y

        if old_x == new_x or old_y == new_y:
            return self.position.move(new_x, new_y, dry)

        return False


class Knight(Piece):
    def legal_move(self, position: Position, dry: bool = False) -> bool:
        super()
        if abs(self.position.x - position.x) == 2 and abs(self.position.y - position.y) == 1:
            return self.position.move(position.x, position.y, dry)
        elif abs(self.position.x - position.x) == 1 and abs(self.position.y - position.y) == 2:
            return self.position.move(position.x, position.y, dry)
        return False


class Bishop(Piece):
    def legal_move(self, position: Position, dry: bool = False) -> bool:
        super()
        old_x = self.position.x
        new_x = position.x
        old_y = self.position.y
        new_y = position.y

        if abs(new_x - old_x) == abs(new_y - old_y):
            return self.position.move(new_x, new_y, dry)
        return False


class Queen(Piece):
    def legal_move(self, position: Position, dry: bool = False) -> bool:
        super()
        old_x = self.position.x
        new_x = position.x
        old_y = self.position.y
        new_y = position.y

        if old_x == new_x or old_y == new_y or abs(new_x - old_x) == abs(new_y - old_y):
            return self.position.move(new_x, new_y, dry)
        return False


class King(Piece):
    def legal_move(self, position: Position, dry: bool = False) -> bool:
        super()
        old_x = self.position.x
        new_x = position.x
        old_y = self.position.y
        new_y = position.y

        if abs(new_x - old_x) <= 1 and abs(new_y - old_y) <= 1:
            return self.position.move(new_x, new_y, dry)
        return False


class EmptyField(Piece):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, Color.EMPTY)

    def legal_move(self, position: Position, dry: bool = False) -> bool:
        return False


class Board:
    def __init__(self):
        self.fields = [
            [Rook(0, 0, Color.WHITE), Knight(0, 1, Color.WHITE), Bishop(0, 2, Color.WHITE), Queen(0, 3, Color.WHITE),
             King(0, 4, Color.WHITE), Bishop(0, 5, Color.WHITE), Knight(0, 6, Color.WHITE), Rook(0, 7, Color.WHITE)],
            [Pawn(1, 0, Color.WHITE), Pawn(1, 1, Color.WHITE), Pawn(1, 2, Color.WHITE), Pawn(1, 3, Color.WHITE),
             Pawn(1, 4, Color.WHITE), Pawn(1, 5, Color.WHITE), Pawn(1, 6, Color.WHITE), Pawn(1, 7, Color.WHITE)],
            [EmptyField(5, y) for y in range(8)],
            [EmptyField(4, y) for y in range(8)],
            [EmptyField(3, y) for y in range(8)],
            [EmptyField(2, y) for y in range(8)],
            [Pawn(6, 0, Color.BLACK), Pawn(6, 1, Color.BLACK), Pawn(6, 2, Color.BLACK), Pawn(6, 3, Color.BLACK),
             Pawn(6, 4, Color.BLACK), Pawn(6, 5, Color.BLACK), Pawn(6, 6, Color.BLACK), Pawn(6, 7, Color.BLACK)],
            [Rook(7, 0, Color.BLACK), Knight(7, 1, Color.BLACK), Bishop(7, 2, Color.BLACK), Queen(7, 3, Color.BLACK),
             King(7, 4, Color.BLACK), Bishop(7, 5, Color.BLACK), Knight(7, 6, Color.BLACK), Rook(7, 7, Color.BLACK)]]

    def is_path_free(self, selected_piece: Piece, target_position: Position) -> bool:
        old_x, old_y = selected_piece.position.x, selected_piece.position.y
        new_x, new_y = target_position.x, target_position.y
        dx, dy = new_x - old_x, new_y - old_y
        abs_dx, abs_dy = abs(dx), abs(dy)
        step_x, step_y = 1 if dx > 0 else -1, 1 if dy > 0 else -1

        for i in range(1, max(abs_dx, abs_dy)):
            x = old_x + i * step_x
            y = old_y + i * step_y
            try:
                if not isinstance(self.fields[x][y], EmptyField):
                    return False
            except IndexError:
                continue

        return True

    def is_check(self, player: Color) -> bool:
        king_position = None
        for row in self.fields:
            for piece in row:
                if isinstance(piece, King) and piece.color == player:
                    king_position = piece.position
                    break
            if king_position:
                break

        for row in self.fields:
            for piece in row:
                if isinstance(piece, Piece) and piece.color != player and self.is_path_free(piece, king_position):
                    if isinstance(piece, Pawn) and piece.legal_move(king_position, attack=True, dry=True):
                        return True
                    elif piece.legal_move(king_position, dry=True):
                        return True
        return False

    def is_checkmate(self, player: Color) -> bool:
        if not self.is_check(player):
            return False

        for row in self.fields:
            for piece in row:
                if isinstance(piece, Piece) and piece.color == player:
                    for row2 in self.fields:
                        for piece2 in row2:
                            if isinstance(piece2, EmptyField) and piece.legal_move(piece2.position, dry=True):
                                piece.position.move(piece2.position.x, piece2.position.y, dry=True)
                                if not self.is_check(player):
                                    piece.position.move(piece.position.x, piece.position.y, dry=True)
                                    return False
                                piece.position.move(piece.position.x, piece.position.y, dry=True)
        return True
