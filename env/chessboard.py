from env.constants import META
from env.metaclass.board import Board
from env.pieces import PIECE_SETS
from env.players import *


class ChessBoard(metaclass=Board):
    """An arbitrary chessboard with reference to its players."""

    board = [
        [None for _ in range(META['width'])] for _ in range(META['width'])]

    @staticmethod
    def filetoidx(file: str) -> int:
        """Convert a letter in `[a, h]` to its corresponding index in `[0, 7]`."""

        file_index = META['files'].index(file)
        return file_index

    @staticmethod
    def ranktoidx(rank: int) -> int:
        """Convert a rank in `[1, 8]` to its corresponding index in `[0, 7]`."""

        rank_index = META['ranks'].index(rank)
        return rank_index

    def __init__(self, p1: Player=TEAMS['player'], p2: Computer=TEAMS['computer']) -> None:
        """Assign players to the chessboard and arrange their chesspieces."""

        self.p1 = p1
        self.p2 = p2
        white_set = self.p1.piece_set
        black_set = self.p2.piece_set
        for piece in white_set + black_set:
            self.set(piece.ords, piece)

    def __str__(cls) -> None:
        """Print a graphical representation of the chessboard to the terminal."""

        FILE_GAP, INDENT = 3, 5
        DOT, PIPE, SPACE, NEWLINE, NULL = \
            '.', '|', ' ', '\n', ''
        PADDED_DOT = SPACE + DOT + SPACE
        PADDED_PIPE = SPACE + PIPE + SPACE
        for rank, row in enumerate(cls.board):
            print(rank + 1, end=PADDED_PIPE)
            for piece in row:
                print(PADDED_DOT if piece is None else piece, end=SPACE)
            print(NEWLINE)
        print(str(SPACE for _ in range(INDENT)), end=NULL)
        for file in META.files.upper():
            print(file + SPACE * FILE_GAP, end=NULL)

    def ordstoidx(cls, ords: tuple[str, int | str]) -> tuple[int, int]:
        """Convert a coordinate on the chessboard to its corresponding indices."""

        file, rank = ords
        file, rank = file.lower(), int(rank)
        indices = cls.ranktoidx(rank), cls.filetoidx(file)
        return indices

    def get(cls, ords: tuple[int, int]) -> object:
        """Get the object occupied at a coordinate."""

        rank, file = ords
        return cls.board[rank][file]

    def set(cls, piece: object, ords: tuple[int, int]) -> None:
        """Set an object at a coordinate."""

        rank, file = ords
        cls.board[rank][file] = piece
        piece.ords = ords

    def move(cls, src: tuple[int, int], dest: tuple[int, int]) -> object:
        """Move a chesspiece from one coordinate to another."""

        src_piece = cls.get(src)
        dest_piece = cls.get(dest)
        cls.set(src_piece, dest)
        cls.set(None, src)
        return dest_piece

    def occupied(cls, ords: tuple[int, int]) -> bool:
        """Determine whether or not a coordinate is occupied."""

        occupant = cls.get(ords)
        occupied = bool(occupant)
        return occupied

    def valid(cls, move: tuple[tuple[int, int], tuple[int, int]], player: Player) -> bool:
        """Validate an arbitrary movement on the board."""

        valid = False
        src, dest = move
        piece = cls.get(src)
        if src not in META['ords'] or dest not in META['ords']:  # Out-of-bounds
            raise ValueError("Cannot move outside the board.")
        if src is dest:  # Same position
            raise ValueError("Cannot move to the same position.")
        if piece is None:  # Empty source
            raise ValueError("Cannot move from an empty position.")
        if piece.team is not player.team:  # Opponent's pieces
            raise ValueError("Cannot move an opposing piece.")
        if piece.valid(move, player):  # Validate piece
            valid = True
        return valid

    def neighborhood(cls, center: tuple[int, int], proxim: int=1) -> object:
        """Yield the neighbors around a center within a given proximity."""

        ords_idx = map(cls.ordstoidx, META['ords'])
        pieces = filter(cls.occupied, ords_idx)
        center_file, center_rank = center
        for piece in pieces:
            file, rank = piece.ords
            file_dist = abs(ord(file) - ord(center_file))
            rank_dist = abs(int(rank) - int(center_rank))
            if max(file_dist, rank_dist) <= proxim:
                yield piece
