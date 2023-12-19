from collections import namedtuple
from env.players import Player
from itertools import zip_longest


class ChessPiece:
    """An arbitrary chesspiece."""

    def __init__(self, team: Player=None, ords: tuple[int, int]=None, weight: int=1, actions: set=None):
        """Initialize a chesspiece's name, team, coordinates, weight, and actions."""

        self.name = self.__class__.__name__
        self.team = team
        self.ords = ords
        self.weight = weight
        self.actions = actions

    def __repr__(self):
        """Return a graphical representation of the piece."""
        return f"{self.team[0].lower()}{self.name[:2]}"

    def valid(self, move: tuple[tuple[int, int], tuple[int, int]], state: namedtuple) -> bool:
        """Validate a move against an arbitrary chesspiece."""

        valid = False
        src_piece, dest_piece = map(state.board.get, move)
        action = map(abs(a - b) for a, b in zip(*move))
        if src_piece.valid(move, state, action):
            if dest_piece is not None:
                if dest_piece.team is not src_piece.team:
                    valid = True  # Opposing pieces are valid
                else: raise ValueError(f"You cannot attack your own pieces.")
            else: valid = True  # Empty spaces are valid
        return valid


class Pawn(ChessPiece):
    """A pawn chesspiece."""

    def __init__(self, team: Player=None, ords: tuple[int, int]=None, weight=3):
        """Initialize a Pawn's active status and parameters."""

        self.active = False
        super().__init__(
            team=team,
            ords=ords,
            weight=weight,
            actions={
                (-1, +1),  # Northwest
                (+0, +1),  # North
                (+1, +1)})  # Northeast

    def valid(self, move: tuple[namedtuple, namedtuple], state: namedtuple, action: tuple[int, int]=None) -> bool:
        """Validate a Pawn's move."""

        src, dest = move
        dest_piece = state.board.get(dest)
        if self.player.near and src.rank > dest.rank or dest.rank < src.rank:
            raise ValueError("Pawns cannot retreat.")
        if action == (+0, +1) and dest_piece is not None:
            raise ValueError("Pawns cannot attack forward.")
        if action == (+0, +2) and self.active:
            raise ValueError("Pawns cannot repeat this move.")
        if action == (+1, +1) and dest_piece is None:
            raise ValueError("Pawns cannot attack an empty space.")
        if not self.active:  # Once it has opened, a pawn becomes active
            self.active = True
        return True


class Rook(ChessPiece):
    """A Rook chesspiece."""

    def __init__(self, team: Player=None, ords: tuple[int, int]=None, weight=8):
        """Initialize a Rook's parameters."""

        super().__init__(
            team=team,
            ords=ords,
            weight=weight,
            actions={
                (-1, +0),  # West
                (+0, -1),  # South
                (+0, +1),  # North
                (+1, +0)}),  # East

    def valid(self, move: tuple[namedtuple, namedtuple], action: tuple[int, int]) -> bool:
        """Validate a Rook's move."""

        pathway = None
        src, dest = move
        rank_dist, file_dist = action
        if file_dist == 0:
            rank_path = list(range(
                min(int(src.rank), int(dest.rank)) + 1,
                max(int(src.rank), int(dest.rank))))
            if len(rank_path) > 0:
                pathway = zip_longest(src.file, rank_path, fillvalue=src.file)
        elif rank_dist == 0:
            file_path = list(chr(file) for file in range(
                min(ord(src.file), ord(dest.file)) + 1,
                max(ord(src.file), ord(dest.file))))
            if len(file_path) > 0:
                pathway = zip_longest(file_path, src.rank, fillvalue=src.rank)
        if pathway is not None:
            for file, rank in pathway:
                pos = file + str(rank)
                block = self.get(pos)
                if block is not None:
                    raise Exception(f"Path is blocked by a {block.name}.")
        src.piece.actions.add(action)


class Knight(ChessPiece):
    """A Knight chesspiece."""

    def __init__(self, team: Player=None, ords: tuple[int, int]=None, weight=8):
        """Initialize a Knight's parameters."""

        super().__init__(
            team=team,
            ords=ords,
            weight=weight,
            actions={
                (-2, -1),  # Far-west-near-south
                (-2, +1),  # Far-west-near-north
                (-1, -2),  # Near-west-far-south
                (-1, +2),  # Near-west-far-north
                (+1, -2),  # Near-east-far-south
                (+1, +2),  # Near-east-far-north
                (+2, -1),  # Far-east-near-south
                (+2, +1)})  # Far-east-near-north

    def valid(self) -> bool:
        """Validate a Knight's move."""
        ...


class Bishop(ChessPiece):
    """A Bishop chesspiece."""

    def __init__(self, team: Player=None, ords: tuple[int, int]=None, weight=8):
        """Initialize a Bishop's parameters."""

        super().__init__(
            team=team,
            ords=ords,
            weight=weight,
            actions={
                (-1, -1),  # Southwest
                (-1, +1),  # Northwest
                (+1, -1),  # Southeast
                (+1, +1)}),  # Northeast

    def valid(self, move: tuple[namedtuple, namedtuple], action: tuple[int, int]) -> bool:
        """Validate a Bishop's move."""

        src, dest = move
        rank_dist, file_dist = action
        if abs(file_dist) == abs(rank_dist):
            if int(src.rank) < int(dest.rank):
                rank_path = list(range(
                    min(int(src.rank), int(dest.rank)) + 1,
                    max(int(src.rank), int(dest.rank))))
            else:
                rank_path = list(range(
                    max(int(src.rank), int(dest.rank)) - 1,
                    min(int(src.rank), int(dest.rank)), -1))
            if ord(src.file) < ord(dest.file):
                file_path = list(chr(file) for file in range(
                    min(ord(src.file), ord(dest.file)) + 1,
                    max(ord(src.file), ord(dest.file))))
            else:
                file_path = list(chr(file) for file in range(
                    max(ord(src.file), ord(dest.file)) - 1,
                    min(ord(src.file), ord(dest.file)), -1))
            if len(rank_path) > 0 and len(file_path) > 0:
                pathway = zip(file_path, rank_path)
        for file, rank in pathway:
            pos = file + str(rank)
            block = self.get(pos)
            if block is not None:
                raise Exception(f"Path is blocked by a {block.name}.")
        src.piece.actions.add(action)


class Queen(ChessPiece):
    """A queen chesspiece."""

    def __init__(self, team: Player=None, ords: tuple[int, int]=None, weight=8):
        """Initialize a Queen's parameters."""

        super().__init__(
            team=team,
            ords=ords,
            weight=weight,
            actions={
                (-1, -1),  # Southwest
                (-1, +0),  # West
                (-1, +1),  # Northwest
                (+0, -1),  # South
                (+0, +1),  # North
                (+1, -1),  # Southeast
                (+1, +0),  # East
                (+1, +1)})  # Northeast

    def valid(self, move: tuple[namedtuple, namedtuple], action: tuple[int, int]) -> bool:
        """Validate a Queen's move."""

        src, dest = move
        rank_dist, file_dist = action
        if file_dist == 0:
            rank_path = list(range(
                min(int(src.rank), int(dest.rank)) + 1,
                max(int(src.rank), int(dest.rank))))
            if len(rank_path) > 0:
                pathway = zip_longest(src.file, rank_path, fillvalue=src.file)
        elif rank_dist == 0:
            file_path = list(chr(file) for file in range(
                min(ord(src.file), ord(dest.file)) + 1,
                max(ord(src.file), ord(dest.file))))
            if len(file_path) > 0:
                pathway = zip_longest(file_path, src.rank, fillvalue=src.rank)
        elif abs(file_dist) == abs(rank_dist):
            if int(src.rank) < int(dest.rank):
                rank_path = list(range(
                    min(int(src.rank), int(dest.rank)) + 1,
                    max(int(src.rank), int(dest.rank))))
            else:
                rank_path = list(range(
                    max(int(src.rank), int(dest.rank)) - 1,
                    min(int(src.rank), int(dest.rank)), -1))
            if ord(src.file) < ord(dest.file):
                file_path = list(chr(file) for file in range(
                    min(ord(src.file), ord(dest.file)) + 1,
                    max(ord(src.file), ord(dest.file))))
            else:
                file_path = list(chr(file) for file in range(
                    max(ord(src.file), ord(dest.file)) - 1,
                    min(ord(src.file), ord(dest.file)), -1))
            if len(rank_path) > 0 and len(file_path) > 0:
                pathway = zip(file_path, rank_path)
            for file, rank in pathway:
                pos = file + str(rank)
                block = self.get(pos)
                if block is not None:
                    raise Exception(f"Path is blocked by a {block.name}.")
            src.piece.actions.add(action)


class King(ChessPiece):
    """A king chesspiece."""

    def __init__(self, team: Player=None, ords: tuple[int, int]=None, weight=8):
        """Initialize a King's parameters."""

        super().__init__(
            team=team,
            ords=ords,
            weight=weight,
            actions={
                (-1, -1),  # Southwest
                (-1, +0),  # West
                (-1, +1),  # Northwest
                (+0, -1),  # South
                (+0, +1),  # North
                (+1, -1),  # Southeast
                (+1, +0),  # East
                (+1, +1)})  # Northeast

    def valid(self) -> bool:
        """Validate a King's move."""
        ...


PIECES = (Pawn, Rook, Knight, Bishop, Queen, King)  # Arbitrary set of chess pieces
PIECE_SETS = {  # Standard sets of chess pieces
    'white': [*[Pawn(ords=[6, i]) for i in range(stop=8)]
              +[Rook(ords=[7, i]) for i in range(step=8, stop=8)]
              +[Knight(ords=[7, i]) for i in range(start=1, step=6, stop=7)]
              +[Bishop(ords=[7, i]) for i in range(start=2, step=4, stop=6)]
              +[Queen(ords=[7, 3])]
              +[King(ords=[7, 4])]],
    'black': [*[Pawn(ords=[1, i]) for i in range(stop=8)]
              +[Rook(ords=[0, i]) for i in range(step=8, stop=8)]
              +[Knight(ords=[0, i]) for i in range(start=1, step=6, stop=7)]
              +[Bishop(ords=[0, i]) for i in range(start=2, step=4, stop=6)]
              +[Queen(ords=[0, 4])]
              +[King(ords=[0, 3])]]}
