from __future__ import annotations

from bidict import bidict


class BoardVector:
    def __init__(self, x, y):
        self._x: int = x
        self._y: int = y

    def __eq__(self, other):
        if isinstance(other, BoardVector):
            return self.x == other.x and self.y == other.y
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, other: BoardVector):
        return BoardVector(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"vector({self.x}, {self.y})"

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def pair(self) -> tuple[int, int]:
        return self.x, self.y


vector = BoardVector  # alias for BoardVector


class BoardException(Exception):
    pass


class TileOccupiedException(BoardException):
    pass


class OutOfBoundsExcepion(BoardException):
    pass


class DuplicateObjectException(BoardException):
    pass


class HasOwnerException(BoardException):
    pass


class ObjectNotFound(BoardException):
    pass


class BoardObject:
    def __init__(self):
        self._board: Board = None

    @property
    def board(self):
        return self._board

    def get_pos(self):
        return self.board.get_object_pos(self)

    def move(self, transform: BoardVector):
        return self.board.move_object(self, transform)


class Board:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._objects = bidict()

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    def _is_out_of_bounds(self, pos: BoardVector):
        return pos.x not in range(self.width) or pos.y not in range(self.height)

    def _check_out_of_bounds(self, pos: BoardVector):
        if self._is_out_of_bounds(pos):
            raise OutOfBoundsExcepion("Given position is out of bounds.")

    def remove_object(self, obj: BoardObject):
        obj._board = None
        del self._objects.inverse[obj]

    def remove_object_at(self, pos: BoardVector):
        self.remove_object(self._objects[pos])

    def get_object_at(self, pos: BoardVector):
        return self._objects.get(pos, None)

    def get_object_pos(self, obj: BoardObject):
        return self._objects.inverse.get(obj, None)

    def emplace_object(self, obj: BoardObject, pos: BoardVector, force_emplacement=False) -> bool:
        self._check_out_of_bounds(pos)

        if obj in self._objects.values():
            raise DuplicateObjectException("The same object can not be placed on a board twice.")

        if obj._board is not None:
            raise HasOwnerException("The given object is placed on another board.")

        if self.get_object_at(pos) is not None:
            if force_emplacement:
                self.remove_object_at(pos)
            else:
                return False

        obj._board = self
        self._objects[pos] = obj

        return True

    def move_object_to(self, obj: BoardObject, pos: BoardVector):
        if self._is_out_of_bounds(pos):
            return False

        if self.get_object_at(pos) is not None:
            return False

        self._objects.inverse[obj] = pos
        return True

    def move_object(self, obj: BoardObject, transform: BoardVector):
        return self.move_object_to(obj, self.get_object_pos(obj) + transform)

    def objects(self):
        for pos, obj in self._objects.items():
            yield pos, obj
