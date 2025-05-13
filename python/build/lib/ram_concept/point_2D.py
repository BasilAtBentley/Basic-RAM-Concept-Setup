#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from typing import TYPE_CHECKING

# THIRD PARTY IMPORTS

# INTERNAL (THIS LIBRARY) IMPORTS
from .bracket_parser import BracketParser

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    pass

# -------------------------------------------------------------------------------------------------

class Point2D:
    """A read-only 2D Point."""
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = [
        "_x",
        "_y"
    ]

    def __init__(self, x: float, y: float):
        self._x = x
        self._y = y
    
    # Python Special Functions
    
    def __repr__(self):
        return (f'{self.__class__.__name__}('f'{self.x!r}, {self.y!r})')
     
    def __add__(self, other):
        """Add the point-like other and return the result."""
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Subtract the point-like other and return the result."""
        return Point2D(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """Multiply by the float-like other and return the result."""
        return Point2D(self.x * other, self.y  * other)

    @staticmethod
    def from_bracket_string(bracket_string: str) -> Point2D:
        """Create a `Point2D` from the given string in [x][y] format."""
        parser = BracketParser(bracket_string)

        if parser.count_remaining_tokens() != 2:
            raise Exception("Invalid Point2D bracket string: " + bracket_string)

        x = float(parser.next_token())
        y = float(parser.next_token())

        return Point2D(x,y)

    # PYTHON EQUALITY OPERATIONS

    def __eq__(self,obj):
        """Equals operation for Point2D objects"""
        if (obj.__class__ == self.__class__):
            return (self._x == obj._x) and (self._y == obj._y)
        else:
            return False

    # PROPERTY ACCESS

    x = property(lambda self: self._x, None, None, "The x coordinate.")

    y = property(lambda self: self._y, None, None, "The y coordinate.")

    # BRACKET STRING OPERATIONS

    def to_bracket_string(self) -> str:
        """Returns the point in [x][y] format."""

        return "[" + str(self.x) + "][" + str(self.y) + "]"

    def to_point_list_bracket_string(self) -> str:
        """Returns the point in [[x][y]] format."""

        return "[" + self.to_bracket_string() + "]"

    #   UTILITY METHODS
    
    def approx_eq(self, other: Point2D, absolute=1e-12, relative=1e-6) -> bool:
        """Compare this to other, using give abs tolerance and the given rel tolerance times value in self."""
        x_tolerance = max(abs(absolute), abs(self.x * relative))
        y_tolerance = max(abs(absolute), abs(self.y * relative))

        return (abs(self.x - other.x) <= x_tolerance) and (abs(self.y - other.y) <= y_tolerance)
