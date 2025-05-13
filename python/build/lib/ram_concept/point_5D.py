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

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    pass

# -------------------------------------------------------------------------------------------------

class Point5D:
    """A read-only 5D Point.

    This class is primarily used for the reporting of results (displacements or forces/moments).
    The x- and y- axes referred to may actually be the r- and s- axes of the particular result
    (these can be thought of as local x- and y- axes)
    
    The dimensions of this point are:
    
    * x: position in the x-axis direction (or force in the x-axis direction)
    * y: position in the y-axis direction (or force in the y-axis direction)
    * z: position in the z-axis direction (or force in the z-axis direction)
    * rot_x: rotation about the x-axis (or moment about the x-axis direction)
    * rot_y: rotation about the y-axis (or moment about the y-axis direction)
    """
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = [
        "_x",
        "_y",
        "_z",
        "_rot_x",
        "_rot_y"
    ]

    def __init__(self, x: float, y: float, z: float, rot_x: float, rot_y: float):
        self._x = x
        self._y = y
        self._z = z
        self._rot_x = rot_x
        self._rot_y = rot_y
    

    def __repr__(self):
        return (f'{self.__class__.__name__}('f'{self.x!r}, {self.y!r}, {self.z!r}, {self.rot_x!r}, {self.rot_y!r})')    

    def __eq__(self,obj):
        """Equals operation for Point5D objects"""
        if (obj.__class__ == self.__class__):
            return  (self._x == obj._x) and \
                    (self._y == obj._y) and \
                    (self._z == obj._z) and \
                    (self._rot_x == obj._rot_x) and \
                    (self._rot_y == obj._rot_y)
        else:
            return False

    # PROPERTY ACCESS

    x = property(lambda self: self._x, None, None, "The x value (typically displacement or force).")

    y = property(lambda self: self._y, None, None, "The y value (typically displacement or force).")

    z = property(lambda self: self._z, None, None, "The z value (typically displacement or force).")

    rot_x = property(lambda self: self._rot_x, None, None, "The rotation-about-x value (typically rotation or moment).")

    rot_y = property(lambda self: self._rot_y, None, None, "The rotation-about-y value (typically rotation or moment).")

    #   UTILITY METHODS
    
    def approx_eq(self, other: Point5D, translation_tolerance=1e-12, rotation_tolerance=1e-12) -> bool:
        """Compare this to other, using given absolute tolerances."""
        return  (abs(self.x - other.x) <= translation_tolerance) and \
                (abs(self.y - other.y) <= translation_tolerance) and \
                (abs(self.z - other.z) <= translation_tolerance) and \
                (abs(self.rot_x - other.rot_x) <= rotation_tolerance) and \
                (abs(self.rot_y - other.rot_y) <= rotation_tolerance) 
