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
from .add_property import _float_property
from .add_property import _polygon_location_property
from .cad_entity import CadEntity
from .polygon_2D import Polygon2D
from .spring import Spring

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class AreaSpring(Spring):
    """`AreaSpring` is an polygon-shaped spring that provides support to slabs.
    
    `AreaSprings` are always located on the :any:`StructureLayer` ("Mesh Input" layer).
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    kFr0 = _float_property("ASKFr0", "Lateral spring stiffness in r-axis direction at first point in shape")
    kFr1 = _float_property("ASKFr1", "Lateral spring stiffness in r-axis direction at second point in shape")
    kFr2 = _float_property("ASKFr2", "Lateral spring stiffness in r-axis direction at third point in shape")

    kFs0 = _float_property("ASKFs0", "Lateral spring stiffness in s-axis direction at first point in shape")
    kFs1 = _float_property("ASKFs1", "Lateral spring stiffness in s-axis direction at second point in shape")
    kFs2 = _float_property("ASKFs2", "Lateral spring stiffness in s-axis direction at third point in shape")

    kFz0 = _float_property("ASKFz0", "Lateral spring stiffness in z-axis direction at first point in shape")
    kFz1 = _float_property("ASKFz1", "Lateral spring stiffness in z-axis direction at second point in shape")
    kFz2 = _float_property("ASKFz2", "Lateral spring stiffness in z-axis direction at third point in shape")

    kMr0 = _float_property("ASKMr0", "Rotational spring stiffness about r-axis at first point in shape")
    kMr1 = _float_property("ASKMr1", "Rotational spring stiffness about r-axis at second point in shape")
    kMr2 = _float_property("ASKMr2", "Rotational spring stiffness about r-axis at third point in shape")

    kMs0 = _float_property("ASKMs0", "Rotational spring stiffness about s-axis at first point in shape")
    kMs1 = _float_property("ASKMs1", "Rotational spring stiffness about s-axis at second point in shape")
    kMs2 = _float_property("ASKMs2", "Rotational spring stiffness about s-axis at third point in shape")

    location : Polygon2D = _polygon_location_property("Read-only :any:Polygon2D location of this `AreaSpring`.")

    # CONVENIENCE PROPERTY SETTING OPERATIONS

    def set_spring_stiffnesses(self, kFr: float, kFs: float, kFz: float, kMr: float, kMs: float) -> None:
        """Sets the given (uniform) spring stiffness"""
        self.kFr0 = kFr
        self.kFr1 = kFr
        self.kFr2 = kFr

        self.kFs0 = kFs
        self.kFs1 = kFs
        self.kFs2 = kFs

        self.kFz0 = kFz
        self.kFz1 = kFz
        self.kFz2 = kFz

        self.kMr0 = kMr
        self.kMr1 = kMr
        self.kMr2 = kMr

        self.kMs0 = kMs
        self.kMs1 = kMs
        self.kMs2 = kMs

    def zero_spring_stiffnesses(self) -> None:
        """Sets all spring stiffnesses to zero"""
        self.set_spring_stiffnesses(0,0,0,0,0)

# -------------------------------------------------------------------------------------------------

class DefaultAreaSpring(AreaSpring):
    """`DefaultAreaSpring` represents a `AreaSpring` that stores the default values for future `AreaSprings` that are created.

    An `Exception` will be raised if the `location` property of `DefaultAreaSpring` is accessed.
    
    There is only 1 and always 1 `DefaultAreaSpring` in the `Model`. It is accessed through :any:`CadManager.default_area_spring`
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # CadEntity OVERRIDES

    def delete(self) -> None:
        """This method will raise an exception, as `delete` is not available for default objects."""
        raise Exception("delete() is not supported for default CadEntities")

