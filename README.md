# chess
An incomplete implementation of chess.

## Complete features
- Board environment
    - Board display
    - Piece taking
    - Piece movement
        - Bug: AI does not recognize a 2-Pawn opener as a legal move.
- AI environment (see `players.py`)
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
