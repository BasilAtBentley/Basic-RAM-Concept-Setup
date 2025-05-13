#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from typing import List
from typing import TYPE_CHECKING

# THIRD PARTY IMPORTS

# INTERNAL (THIS LIBRARY) IMPORTS
from .bracket_parser import BracketParser
from .point_2D import Point2D

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    pass

# -------------------------------------------------------------------------------------------------

class Polygon2D:
    """A read-only 2D polygon."""

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = [
        "_points"
    ]

    def __init__(self, points: List[Point2D]):
        self._points = points.copy()

    @staticmethod
    def from_bracket_string(bracket_string: str) -> Polygon2D:
        """Create a `Polygon2D` from the given string in [[x][y]][[x][y]][[x][y]]... format."""
        parser = BracketParser(bracket_string)

        if parser.count_remaining_tokens() < 3:
            raise Exception("Invalid Polygon2D bracket string: " + bracket_string)

        points: List[Point2D] = []
        while parser.has_next_token():
            points.append(Point2D.from_bracket_string(parser.next_token()))
        
        return Polygon2D(points)

    # PYTHON EQUALITY OPERATIONS

    def __eq__(self,obj):
        """Equals operation for Polygon2D objects"""
        if (obj.__class__ == self.__class__):
            return (self._points == obj._points) 
        else:
            return False

    # PROPERTY ACCESS

    point_count: int = property(lambda self: len(self._points), None, None, "The number of points in this polygon.")

    points: List[Point2D] = property(lambda self: self._points.copy(), None, None, "The points in this polyon (a copy that can be modified).")

    # POINT ACCESS

    def point_at(self, index: int) -> Point2D:
        """Returns the point at the given zero-based index."""

        return self._points[index]

    #   UTILITY METHODS

    def to_point_list_bracket_string(self) -> str:
        """Returns the list of points as a sequence of bracket strings, such as [[x1][y1]][[x2][y2]][[x3][y3]][[x4][y4]]"""

        bracket_string = ""
        for point in self._points:
            bracket_string = bracket_string + "[" + point.to_bracket_string() + "]"
        
        return bracket_string
            
    def approx_eq(self, other: Polygon2D, absolute=1e-12, relative=1e-6) -> bool:
        """Compare this to other, using give abs tolerance and the given rel tolerance times value in self.
        
        The comparison is done for all points independently"""
        if self.point_count != other.point_count:
            return False
        
        for i_point in range(self.point_count):
            if not self.point_at(i_point).approx_eq(other.point_at(i_point), absolute,relative):
                return False
        
        return True
