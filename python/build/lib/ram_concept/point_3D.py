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

class Point3D:
    """A read-only 3D Point."""
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = [
        "_x",
        "_y",
        "_z"
    ]

    def __init__(self, x: float, y: float, z: float):
        self._x = x
        self._y = y
        self._z = z

    # Python Special Functions
    
    def __repr__(self):
        return (f'{self.__class__.__name__}('f'{self.x!r}, {self.y!r}, {self.z!r})')    
     
    def __add__(self, other):
        """Add the point-like other and return the result."""
        return Point3D(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        """Subtract the point-like other and return the result."""
        return Point3D(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        """Multiply by the float-like other and return the result."""
        return Point3D(self.x * other, self.y  * other, self.z  * other)

    @staticmethod
    def from_bracket_string(bracket_string: str) -> Point3D:
        """Create a `Point3D` from the given string in [x][y][z] format."""
        parser = BracketParser(bracket_string)

        if parser.count_remaining_tokens() != 3:
            raise Exception("Invalid Point3D bracket string: " + bracket_string)

        x = float(parser.next_token())
        y = float(parser.next_token())
        z = float(parser.next_token())

        return Point3D(x,y,z)

    # PYTHON EQUALITY OPERATIONS

    def __eq__(self,obj):
        """Equals operation for Point3D objects"""
        if (obj.__class__ == self.__class__):
            return  (self._x == obj._x) and \
                    (self._y == obj._y) and \
                    (self._z == obj._z)
        else:
            return False

    # PROPERTY ACCESS

    x = property(lambda self: self._x, None, None, "The x value.")

    y = property(lambda self: self._y, None, None, "The y value.")

    z = property(lambda self: self._z, None, None, "The z value.")

    # BRACKET STRING OPERATIONS

    def to_bracket_string(self) -> str:
        """Returns the point in [x][y][z] format."""

        return "[" + str(self.x) + "][" + str(self.y) + "][" + str(self.z) + "]"

    #   UTILITY METHODS
    
    def approx_eq(self, other: Point3D, translation_tolerance=1e-12) -> bool:
        """Compare this to other, using given absolute tolerances."""
        return  (abs(self.x - other.x) <= translation_tolerance) and \
                (abs(self.y - other.y) <= translation_tolerance) and \
                (abs(self.z - other.z) <= translation_tolerance)
