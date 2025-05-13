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

class TemperatureAreaLoad(CadEntity):
    """`TemperatureAreaLoad` is an polygon-shaped temperature-change that is applied to slabs.
    
    `TemperatureAreaLoad` are always located on a :any:`TemperatureLoadingLayer` (and are created via :any:`TemperatureLoadingLayer.add_temperature_area_load`).
    """
    # internally this maps to a combination of AreaLoadForImposedStrainBase and AreaLoadForTemperature

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    temperature_change_at_top = _float_property("ALTtop", "Temperature change at top of slab.")

    temperature_change_at_bottom = _float_property("ALTbot", "Temperature change at bottom of slab.")

    location : Polygon2D = _polygon_location_property("Read-only :any:`Polygon2D` location of this `TemperatureAreaLoad`.")

    # CONVENIENCE PROPERTY SETTING OPERATIONS

    def set_temperature_change(self, temperature_change: float) -> None:
        """Sets the given (uniform top and bottom) temperature change"""
        self.temperature_change_at_top = temperature_change
        self.temperature_change_at_bottom = temperature_change

# -------------------------------------------------------------------------------------------------

class DefaultTemperatureAreaLoad(TemperatureAreaLoad):
    """`DefaultTemperatureAreaLoad` represents a `TemperatureAreaLoad` that stores the default values for future `TemperatureAreaLoad` that are created.

    An `Exception` will be raised if the `location` property of `DefaultTemperatureAreaLoad` is accessed.
    
    There is only 1 and always 1 `DefaultTemperatureAreaLoad` in the `Model`. It is accessed through :any:`CadManager.default_temperature_area_load`
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


