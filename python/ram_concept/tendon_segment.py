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
from .add_property import _bool_property
from .add_property import _int_property
from .add_property import _enum_int_property
from .add_property import _float_property
from .add_property import _line_segment_location_property
from .add_property import _no_none_data_property
from .add_property import _readonly_data_property
from .add_property import _readonly_float_property
from .bracket_parser import BracketParser
from .cad_entity import CadEntity
from .enums import ElevationReference
from .line_segment_2D import LineSegment2D
from .pt_system import PTSystem
from .tendon_node import TendonNode

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model


# -------------------------------------------------------------------------------------------------

class TendonSegment(CadEntity):
    """`TendonSegment` is a tendon segment between profile points.
    
    `TendonSegments` are always located on a :any:`TendonLayer`.
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PROPERTY PROPERTIES

    # note that we use user-based indexing (1..N) and not internal indexing (0..N) to match the UI names

    pt_system: PTSystem  = _no_none_data_property("PTSystem", PTSystem, ":any:`PTSystem` used by this `TendonSegment`")

    harped = _bool_property("Harped", "Is this `TendonSegment` harped? (if true, ignore `inflection_ratio`)")
    inflection_ratio = _float_property("InflectionRatio", "Location of inflection point as a fractional distance along this `TendonSegment`.")

    stress_at_end_1 = _readonly_float_property("StressEnd0", "Stress in the `TendonSegment` at start point")
    stress_at_end_2 = _readonly_float_property("StressEnd1", "Stress in the `TendonSegment` at end point")

    strand_count = _float_property("NumStrands", "Number of strands in `TendonSegment`")

    half_span_ratio_end_1 = _float_property("HalfSpanRatioEnd0", "The (tendon) span ratio at end 1.")
    half_span_ratio_end_2 = _float_property("HalfSpanRatioEnd1", "The (tendon) span ratio at end 2.")

    node_1: TendonNode = _readonly_data_property("TendonNode0", "The `TendonNode` at the start point.")
    node_2: TendonNode = _readonly_data_property("TendonNode1", "The `TendonNode` at the end point.")

    elevation_reference_1: ElevationReference = _enum_int_property("ElevationReferenceNode0", ElevationReference, ":any:`ElevationReference`: The `ElevationReference` for `node_1`.")
    elevation_reference_2: ElevationReference = _enum_int_property("ElevationReferenceNode1", ElevationReference, ":any:`ElevationReference`: The `ElevationReference` for `node_2`.")

    elevation_value_1 = _float_property("ElevationValueNode0", "The elevation value for `node_1`.")
    elevation_value_2 = _float_property("ElevationValueNode1", "The elevation value for `node_2`.")

    auto_locate_profile_2 = _bool_property("AutoLocateProfile1", "Automatically located profile 2 point (node_2) for equal balance loads")

    strand_to_duct_offset = _float_property("StrandCGStoDuctCGSOffset", "The offset between the strand CGS and duct CGS")

    location : LineSegment2D = _line_segment_location_property("Read-only :any:`LineSegment2D` location of this `TendonSegment`.")

    # OPERATIONS

    def elevations_along_segment(self, fractional_lengths: List[float])-> List[float]:
        """Determines the elevations at all the given fractional distances along the `TendonSegment`.
        0.0 is the fractional length for end 1 and 1.0 is the fractional length at end 2.
        Values are only guaranteed to be correct after a Call All.
        """
        command = "[GET_PROFILE_ELEVATIONS_USER]"
        for fraction in fractional_lengths:
            # we don't check for bad fractions as concept will do that checking internally
            command = command + "[" + str(fraction) + "]"

        result = self._command(command) # may raise an exception

        return BracketParser.parse_floats(result)

    def other_node(self, node: TendonNode)->TendonNode:
        """Return the :any:`TendonNode` this `TendonSegment` is connected to that is not the given :any:`TendonNode`.
        This can be helpful when determining a chain of `TendonSegment`s.
        An Exception is raised if the given node is not connected to this `TendonSegment`."""
        if node == self.node_1:
            return self.node_2

        if node == self.node_2:
            return self.node_1

        raise Exception("TendonNode is not connected to this TendonSegment")

# -------------------------------------------------------------------------------------------------

class DefaultTendonSegment(TendonSegment):
    """`DefaultTendonSegment` represents a `TendonSegment` that stores the default values for future `TendonSegments` that are created.

    An `Exception` will be raised if the `location`, `node_1` or `node_2` properties of `DefaultTendonSegment` are accessed.
    
    There is only 1 and always 1 `DefaultTendonSegment` in the `Model`. It is accessed through :any:`CadManager.default_tendon_segment`
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # TendonSegment OVERRIDES

    def elevations_along_segment(self, fractional_lengths: List[float])-> List[float]:
        """This method will raise an exception, as `elevations_along_segment` is not available for `DefaultTendonSegment`."""
        raise Exception("elevations_along_segment() is not supported for DefaultTendonSegment")

    # CadEntity OVERRIDES

    def delete(self) -> None:
        """This method will raise an exception, as `delete` is not available for default objects."""
        raise Exception("delete() is not supported for default CadEntities")

