from collections import namedtuple
from env.constants import META
from itertools import chain
from math import inf
from numpy import array, dot


class Player:
    """A generic player."""

    def __init__(self, piece_set=None, near=True):
        """Initialize a player's piece set, pieces won, and point-of-view."""

        self.piece_set = piece_set
        self.pieces_won = set()
        self.near = near

    def __str__(self):
        """Return a graphical representation of a player."""
        return f"""{self.team}: {len(self.piece_set) + len(self.pieces_won)}"""

    def claim(self, move, player) -> object:
        """Claim a position on the board."""

        if piece_captured := self.board.move(move):
            if player is self.p1:  # Player takes Computer's piece
                self.p1.pieces_won.add(piece_captured)
                self.p2.pieces[piece_captured.name].remove(piece_captured)
            else:  # Computer takes Player's piece
                self.p2.pieces_won.add(piece_captured)
                self.p1.pieces[piece_captured.name].remove(piece_captured)
        return piece_captured

    def get_moves(self, board) -> set:
        """Return the set of legal moves that a player can make."""

        legal_moves = set()
        pieces = [*chain(self.piece_set.values())]
        for piece, position in dot(array(pieces), array(META)):
            move = piece.position, position
            if board.move_is_legal(*move, self):
                legal_moves.add((piece.position, position))
        return legal_moves


class Computer(Player):
    """A computer with artificial intelligence."""

    def __init__(self, near=False):
        """Initialize a Computer's point-of-view."""
        super().__init__(near)

    def __str__(self):
        """Return a graphical representation of a Computer."""
        return super().__str__()

    def ab_search(self, game, state, depth) -> tuple:
        """Run an alpha-beta search on a game state."""

        _, move = self.max_value(game, state, -inf, inf, depth + 1)
        return move

    def max_value(self, game, state, alpha, beta, depth):
        """Return a maximum value from the decision tree."""

        if game.is_cutoff(state, depth) or game.is_terminal(state):
            return game.evaluate(state), None
        value = -inf
        for action in game.actions(state):
            successor, _ = self.min_value(game, game.result(state, action), alpha, beta, depth + 1)
            if successor > value:
                value, move = successor, action
                alpha = max(alpha, value)
            if value >= beta:
                return value, move
        return value, move

    def min_value(self, game, state, alpha, beta, depth):
        """Return a minimum value from the decision tree."""

        if game.is_cutoff(state, depth) or game.is_terminal(state):
            return game.evaluate(state), None
        value = inf
        for action in game.actions(state):
            successor, _ = self.max_value(game, game.result(state, action), alpha, beta, depth + 1)
            if successor < value:
                value, move = successor, action
                beta = min(alpha, value)
            if value <= alpha:
                return value, move
        return value, move


TEAMS = {
    'player': Player(),
    'computer': Computer()}
