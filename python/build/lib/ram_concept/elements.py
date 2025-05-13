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
from .add_property import _line_segment_location_property
from .add_property import _point_location_property
from .add_property import _polygon_location_property
from .add_property import _readonly_bool_property
from .add_property import _readonly_bool_string_property
from .add_property import _readonly_data_property
from .add_property import _readonly_int_property
from .add_property import _readonly_float_property
from .cad_entity import CadEntity
from .line_segment_2D import LineSegment2D
from .point_spring import Point2D
from .point_3D import Point3D
from .polygon_2D import Polygon2D

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .concrete import Concrete
    from .model import Model

# -------------------------------------------------------------------------------------------------

class Element(CadEntity):
    """`Element` is an abstract superclass for :any:`SupportElement` and :any:`SlabElement`.
    
    `Elements` are always located on the :any:`ElementLayer`.
    """
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    concrete: Concrete  = _readonly_data_property("ConcreteMix", ":any:`Concrete` used by this `Element`")

# -------------------------------------------------------------------------------------------------

class SupportElement(Element):
    """`SupportElement` is an abstract superclass for :any:`WallElement` and :any:`ColumnElement`.
    
    `SupportElements` are always located on the :any:`ElementLayer`.
    """
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    fixed_near = _readonly_bool_property("FixedNear", "Rotational fixity of the element to the slab")

    fixed_far = _readonly_bool_property("FixedFar", "Rotational fixity of the element at the end away from the slab")

    compressible = _readonly_bool_property("Compressible", "Is the element compressible? (if False, the element is infinitely rigid vertically)")

    height = _readonly_float_property("Height", "Vertical dimension of the element")

    below_slab = _readonly_bool_string_property("SupportSet", "below", "above", "Is this element below the slab? (above the slab if false)")

    use_specified_LLR_parameters = _readonly_bool_property("UseSpecifiedLlrParameters", "Use the specified live load reduction parameters instead of the calculated ones (use the calculated ones if false).")

    specified_LLR_levels = _readonly_int_property("SpecifiedLlrLevels", "The user specified number of levels being supported (for live load reduction calculation purposes")

    specified_trib_area = _readonly_float_property("SpecifiedTribArea", "The user specified tributary area being supported (for live load reduction calculation purposes, if the live load reduction code uses tributary area)")

    specified_influence_area = _readonly_float_property("SpecifiedInfluenceArea", "The user specified influences area being supported (for live load reduction calculation purposes, if the live load reduction code uses influence area)")

    llr_max_reduction = _readonly_float_property("LlrMaxReduction", "The maximum allowed (by user) live load reduction percentage for this support (0->100).")

# -------------------------------------------------------------------------------------------------

class WallElement(SupportElement):
    """`WallElement` represents a wall element on the :any:`ElementLayer`."""
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    shear_wall = _readonly_bool_property("ShearWall", "If True, the `WallElement` is fixed to the slab horizontally")

    thickness = _readonly_float_property("WallThickness", "The through-thickness of the `WallElement`")

    location: LineSegment2D = _line_segment_location_property("Read-only :any:`LineSegment2D` location of the `WallElement`")

    # FUTURE: add remaining WallElement properties?

# -------------------------------------------------------------------------------------------------

class ColumnElement(SupportElement):
    """`ColumnElement` represents a column element on the :any:`ElementLayer`."""
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    b = _readonly_float_property("B", "The width of the `ColumnElement` (if zero, `ColumnElement` is round)")

    d = _readonly_float_property("D", "The depth of the `ColumnElement` (diameter if b=0)")

    i_factor = _readonly_float_property("IFactor", "The bending stiffness multiplier (or 'crack factor')")

    angle = _readonly_float_property("Angle", "The plan view angle of the `ColumnElement` (at 0, the 'b' dimension is along x-axis)")

    roller = _readonly_bool_property("Roller", "Is the far end of the `ColumnElement` free to move laterally?")

    location: Point2D = _point_location_property("Read-only :any:`Point2D` location of the `ColumnElement`")

# -------------------------------------------------------------------------------------------------

class SlabElement(Element):
    """`SlabElement` represents a slab element on the :any:`ElementLayer`."""
    # internally this maps to both TriSlabElement and QuadSlabElement
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    thickness = _readonly_float_property("SlabThickness","Thickness of the slab or beam")

    toc = _readonly_float_property("TOC", "Top of concrete elevation")

    kMr  = _readonly_float_property("SlabKMr",  "Stiffness multiplier for bending moments about the r-axis")
    kMs  = _readonly_float_property("SlabKMs",  "Stiffness multiplier for bending moments about the s-axis")
    kMrs = _readonly_float_property("SlabKMrs", "Stiffness multiplier for twisting moments about the r-s axes")
    kFr  = _readonly_float_property("SlabKFr",  "Stiffness multiplier for axial forces in the r-axis direction")
    kFs  = _readonly_float_property("SlabKFs",  "Stiffness multiplier for axial forces in the s-axis direction")
    kVrs = _readonly_float_property("SlabKVrs", "Stiffness multiplier for in-plane shear forces along the r-s axes")

    r_axis : float = _readonly_float_property("SlabRAxis", "CCW/ACW angle from 3 o'clock to the r-axis (for value of zero, the r-axis is parallel to the global x-axis).")

    location: Polygon2D = _polygon_location_property("Read-only :any:`Polygon2D` location of the `SlabElement`")    

# -------------------------------------------------------------------------------------------------

class WallElementGroup(CadEntity):
    """`WallElementGroup` represents a group of :any:`WallElement` whose reactions are summarized together."""

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    

    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # INTERNAL PROPERTY DEFINITION

    def _wallgroup_centroid_property() -> property:
        """Defines property access for the WallGroup centroid property."""
        def getter(self) -> Point3D:
            return self._get_point3D_property("CentroidNear")
            
        return property(getter,None,None, "The centroid location for the near end of this `WallElementGroup`")

    # PUBLIC PROPERTIES
    
    centroid = _wallgroup_centroid_property()
    reaction_angle = _readonly_float_property("Angle", "The angle about which for this `WallElementGroup` (anti-clockwise from 3 o'clock; at zero the reaction x-axis aligns with the global x-axis).")
    total_area = _readonly_float_property("TotalWallArea", "The total wall area for this `WallElementGroup` (sum of individual wall element area).")
    total_length = _readonly_float_property("TotalWallLength", "The total length for this `WallElementGroup` (sum of individual wall element length).")

    


