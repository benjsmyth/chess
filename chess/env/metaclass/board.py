class Board(type):
    """A metaclass, which enforces most `ChessBoard` methods to be a `classmethod`."""

    def __new__(cls, name, bases, dict) -> type:
        """Except for `__init__`, cast all non-static callables to a `classmethod`."""

        dict_items = dict.items()
        for key, value in filter(lambda k: callable(k), dict_items):
            if key != '__init__' and not isinstance(value, staticmethod):
                dict[key] = classmethod(value)
        new_board = super().__new__(cls, name, bases, dict)
        return new_board
