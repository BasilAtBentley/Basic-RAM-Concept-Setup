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
from .point_2D import Point2D

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    pass


# -------------------------------------------------------------------------------------------------

class LineSegment2D:
    """A read-only 2D line segment."""

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = [
        "_start_point",
        "_end_point"
    ]

    def __init__(self, start_point: Point2D, end_point: Point2D):
        self._start_point = start_point
        self._end_point = end_point


    def __repr__(self):
        return (f'{self.__class__.__name__}('f'{self.start_point!r}, {self.end_point!r})')  


    @staticmethod
    def from_bracket_string(bracket_string: str) -> LineSegment2D:
        """Create a `LineSegment2D` from the given string in [[x][y]][[x][y]] format."""
        parser = BracketParser(bracket_string)

        if parser.count_remaining_tokens() != 2:
            raise Exception("Invalid LineSegment2D bracket string: " + bracket_string)

        start_point = Point2D.from_bracket_string(parser.next_token())
        end_point = Point2D.from_bracket_string(parser.next_token())

        return LineSegment2D(start_point, end_point)

    # PYTHON EQUALITY OPERATIONS

    def __eq__(self,obj):
        """Equals operation for LineSegment2D objects"""
        if (obj.__class__ == self.__class__):
            return (self._start_point == obj._start_point) and (self._end_point == obj._end_point)
        else:
            return False

    # POINT ACCESS

    start_point = property(lambda self: self._start_point, None, None, "The start point of the line segment.")

    end_point = property(lambda self: self._end_point, None, None, "The end point of the line segment.")

    # MATHEMATICAL OPERATIONS

    def point_along_segment(self, ratio: float)->Point2D:
        """Calculate and return the point at the given fractional location along this segment."""
        return self.start_point + ((self.end_point - self.start_point) * ratio)

    # BRACKET STRING OPERATIONS

    def to_point_list_bracket_string(self) -> str:
        """Returns the list of points as a sequence of bracket strings, such as [[x1][y1]][[x2][y2]]"""
     
        return "[" + self.start_point.to_bracket_string() + "][" + self.end_point.to_bracket_string() + "]"

    #   UTILITY METHODS
            
    def approx_eq(self, other: LineSegment2D, absolute=1e-12, relative=1e-6) -> bool:
        """Compare this to other, using give abs tolerance and the given rel tolerance times value in self.
        
        The comparison is done for start and end points independently"""
        return (self.start_point.approx_eq(other.start_point, absolute, relative) and self.end_point.approx_eq(other.end_point, absolute, relative))
