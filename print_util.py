import os

import pieces


def green(text):
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(0, 255, 0, text)


def red(text):
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(255, 0, 0, text)


def clear():
    os.system("cls || clear")


def print_board(board: pieces.Board):
    print("  A B C D E F G H")
    print("  ---------------")
    for row in range(7, -1, -1):
        print(row + 1, end="|")
        for col in range(8):
            piece = board.fields[row][col]
            if isinstance(piece, pieces.Rook):
                match piece.color:
                    case pieces.Color.BLACK:
                        print(red("R"), end=" ")
                    case pieces.Color.WHITE:
                        print(green("R"), end=" ")
            elif isinstance(piece, pieces.Knight):
                match piece.color:
                    case pieces.Color.BLACK:
                        print(red("H"), end=" ")
                    case pieces.Color.WHITE:
                        print(green("H"), end=" ")
            elif isinstance(piece, pieces.Bishop):
                match piece.color:
                    case pieces.Color.BLACK:
                        print(red("B"), end=" ")
                    case pieces.Color.WHITE:
                        print(green("B"), end=" ")
            elif isinstance(piece, pieces.Queen):
                match piece.color:
                    case pieces.Color.BLACK:
                        print(red("Q"), end=" ")
                    case pieces.Color.WHITE:
                        print(green("Q"), end=" ")
            elif isinstance(piece, pieces.King):
                match piece.color:
                    case pieces.Color.BLACK:
                        print(red("K"), end=" ")
                    case pieces.Color.WHITE:
                        print(green("K"), end=" ")
            elif isinstance(piece, pieces.EmptyField):
                print("#", end=" ")
            elif isinstance(piece, pieces.Pawn):
                match piece.color:
                    case pieces.Color.BLACK:
                        print(red("P"), end=" ")
                    case pieces.Color.WHITE:
                        print(green("P"), end=" ")
            else:
                print(" ", end=" ")
        print("|", row + 1)
    print("  ---------------")
    print("  A B C D E F G H")
