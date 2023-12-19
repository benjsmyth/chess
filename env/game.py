from copy import deepcopy
from env.chessboard import ChessBoard
from env.constants import STATE
from env.pieces import PIECES, PIECE_SETS
from env.players import *


class Game:
    """A human-versus-computer game of chess."""

    def __init__(self, p1: Player=TEAMS['player'], p2: Computer=TEAMS['computer']) -> None:
        """Initialize the players and chessboard."""

        self.p1 = p1  # Player 1
        self.p2 = p2  # Player 2 (Computer)
        self.p1.piece_set = PIECE_SETS['white']
        self.p2.piece_set = PIECE_SETS['black']
        self.board = ChessBoard()

    def play(self) -> Player | None:
        """Play an entire game of chess."""

        player = self.p1
        game_over = False
        while not game_over:  # Game loop
            print(self.board)  # Show board state
            if player is self.p1:  # Player turn
                valid_move = False
                while not valid_move:  # Enforce legal moves
                    move = input("Move: ").split()
                    if player.valid(move, self.board):
                        valid_move = True
                        player.claim(move, self.board)
                    else: print("Illegal move.")
            else:  # Computer turn
                move = self.p2.ab_search(  # Alpha-beta search
                    game=self,
                    state=STATE(  # Game state
                        board=deepcopy(self.board),
                        player=deepcopy(player),  # self.p2
                        opponent=deepcopy(self.p1),
                        depth=STATE.depth),
                    depth=0)  # Search from root
                player.claim(move, self.p2)
            if winner := self.in_check() or self.in_stalemate():
                game_over = True
            player = self.p1 if player is self.p2 else self.p2
        return winner or None

    def actions(self, state: namedtuple) -> set:
        """Return the set of legal actions for the state."""
        return state.player.get_moves()

    def result(self, state: namedtuple, action: tuple[int, int]) -> namedtuple:
        """Determine the result of an action on a state."""

        ords = deepcopy(state.ords)
        player = deepcopy(state.player)
        opponent = deepcopy(state.opponent)
        for piece_type in PIECES:
            player.pieces[piece_type].clear()
            opponent.pieces[piece_type].clear()
        state.board.move(action)
        for ords_ in ords:
            piece = state.board.get(ords_)
            if piece is not None:
                if piece.team == player.team:
                    player.pieces[piece.name].append(piece)
                else: opponent.pieces[piece.name].append(piece)
        return STATE(  # State produced by the action
            board=state.board,
            player=player,
            opponent=opponent,
            depth=state.depth)

    def evaluate(self, state):
        """Make an evaluation on the current state of the game."""

        distance = lambda p: (len(state.player.pieces[p.name]) - len(state.opponent.pieces[p.name]))
        return sum(piece.WEIGHT * distance(piece) for piece in PIECES.values())

    def in_check(self, state) -> bool:
        """Determine whether or not the game is in check."""
        return state.player.in_check() or state.opponent.in_check()

    def in_stalemate(self, state) -> bool:
        """Determine whether or not the game is in stalemate."""
        return state.board.in_stalemate()

    def at_cutoff(self, state) -> bool:
        """Determine whether or not the game has reached maximum depth."""
        return state.depth == STATE.depth

    def at_terminal(self, state):
        """Determine whether or not the game is in a terminal state."""
        return self.in_check(state) or self.in_stalemate(state)

    def report(self):
        """Report the game winner."""
        print(f"The winner is {self.winner}.")
