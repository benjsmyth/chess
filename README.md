# chess
A complete implementation of chess.

## Complete features
- Board environment (see `chessboard.py`, but be warned - it's a bit of a mess!)
    - Board display
    - Piece taking
    - Piece movement
        - Although I believe I covered nearly all cases of legal and illegal movements,
    there is quite likely something that I missed.
        - Consequently the AI may choose to make an illegal move that I never considered checking.
        - One significant bug is that the AI does not recognize a 2-Pawn opener as a legal move.
- AI environment (see `computer.py`)
    - Internal state
    - AB-minimax

## Incomplete features
- Promotion
- Castling
- Stalemate
- Check / Checkmate

## Evaluation method
- Simple weighted sum of (# of attacking pieces - # of opposing pieces).
- The weights are a maximum count of the # of spaces a piece can cover.
    - For example, a Rook can occupy 8 spaces in either direction, for a total of 16.
