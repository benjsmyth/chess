from collections import namedtuple

META = {  # Chessboard metadata
    'width': 8,
    'ranks': (ranks := [*range(1, 9)]),  # [1, 2, ... 8]
    'files': (files := [chr(i) for i in range(97, 105)]),  # ['a', 'b', ... 'h']
    'ords': [(rank, file) for rank in ranks for file in files]}  # [(1, 'a'), (1, 'b'), ... (8, 'f')]

STATE = namedtuple(  # Game state
    typename='state',
    field_names=['board', 'player', 'opponent', 'depth'],
    defaults=[3])  # Depth = 3
