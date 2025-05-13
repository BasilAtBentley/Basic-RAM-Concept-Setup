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

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class ShrinkageAreaLoad(CadEntity):
    """`ShrinkageAreaLoad` is an polygon-shaped strain-change that is applied to slabs.
    
    `ShrinkageAreaLoad` are always located on a :any:`ShrinkageLoadingLayer` (and are created via :any:`ShrinkageLoadingLayer.add_shrinkage_area_load`).
    """
    # internally this maps to a combination of AreaLoadForImposedStrainBase and AreaLoadForShrinkage

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    strain_change_at_top = _float_property("ALStop", "Strain change at top of slab.")

    strain_change_at_bottom = _float_property("ALSbot", "Strain change at bottom of slab.")

    location : Polygon2D = _polygon_location_property("Read-only :any:`Polygon2D` location of this `ShrinkageAreaLoad`.")

    # CONVENIENCE PROPERTY SETTING OPERATIONS

    def set_strain_change(self, strain_change: float) -> None:
        """Sets the given (uniform top and bottom) strain change"""
        self.strain_change_at_top = strain_change
        self.strain_change_at_bottom = strain_change

# -------------------------------------------------------------------------------------------------

class DefaultShrinkageAreaLoad(ShrinkageAreaLoad):
    """`DefaultShrinkageAreaLoad` represents a `ShrinkageAreaLoad` that stores the default values for future `ShrinkageAreaLoad` that are created.

    An `Exception` will be raised if the `location` property of `DefaultShrinkageAreaLoad` is accessed.
    
    There is only 1 and always 1 `DefaultShrinkageAreaLoad` in the `Model`. It is accessed through :any:`CadManager.default_shrinkage_area_load`
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


