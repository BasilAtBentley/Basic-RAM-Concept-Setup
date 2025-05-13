#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# to avoid circular module dependencies, when references only used for type hints
# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from enum import Enum
from typing import TYPE_CHECKING

# THIRD PARTY IMPORTS

# INTERNAL (THIS LIBRARY) IMPORTS
from .result_layers import FullResultLayer

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .area_load import AreaLoad
    from .line_load import LineLoad
    from .line_segment_2D import LineSegment2D
    from .model import Model
    from .point_2D import Point2D
    from .point_load import PointLoad
    from .polygon_2D import Polygon2D

# -------------------------------------------------------------------------------------------------

class LoadingCause(Enum):
    """The cause of a loading upon the structure.

    The available values are:

    * SELF_DEAD: loads due to the weight of the structure
    * BALANCE: loads due to the force of the tendons and anchors upon the structure
    * HYPERSTATIC: theoretical load due to restraint of post-tensioning
    * STRESSING_DEAD: dead loads in place at time of stressing of the tendons
    * OTHER_DEAD: dead loads not included in SELF_DEAD or STRESSING_DEAD
    * LIVE_REDUCIBLE: loads defined as reducible in the applicable buildingcode
    * LIVE_UNREDUCIBLE: loads defined as unreducible in the applicable building code
    * LIVE_STORAGE: loads from storage
    * LIVE_PARKING: loads from vehicle parking
    * LIVE_ROOF: loads on roof
    * SNOW: loads from snow
    * OTHER_GRAVITY: gravity loads of no specified type
    * TEMPERATURE: temperature change loads
    * SHRINKAGE: shrinkage strain loads
    * WIND_SERVICE: wind loads defined at service limit state levels
    * WIND_ULTIMATE: wind loads defined at strength limit state levels
    * SEISMIC_SERVICE: seismic loads defined at service limit state levels
    * SEISMIC_ULTIMATE: seismic loads defined at strength limit state levels
    """
    SELF_DEAD = "self_dead"
    BALANCE = "balance"
    HYPERSTATIC = "hyperstatic"
    STRESSING_DEAD = "stressing_dead"
    OTHER_DEAD = "other_dead"
    LIVE_REDUCIBLE = "live_reducible"
    LIVE_UNREDUCIBLE = "live_unreducible"
    LIVE_STORAGE = "live_storage"
    LIVE_PARKING = "live_parking"
    LIVE_ROOF = "live_roof"
    SNOW = "snow"
    OTHER_GRAVITY = "other"
    TEMPERATURE = "temperature"
    SHRINKAGE = "shrinkage"
    WIND_SERVICE = "wind_service_"
    WIND_ULTIMATE = "wind_ultimate_"
    SEISMIC_SERVICE = "seismic_service_"
    SEISMIC_ULTIMATE = "seismic_ultimate_"

    # PUBLIC OPERATIONS

    def is_changable_in_loading(self) -> bool:
        """Can a :any:`LoadingLayer` with this `LoadCause` be changed to another `LoadCause`?"""
        # except for these 5 types, LoadingLayers can have their loading type modified
        return not self in [LoadingCause.SELF_DEAD, LoadingCause.BALANCE, LoadingCause.HYPERSTATIC, LoadingCause.TEMPERATURE, LoadingCause.SHRINKAGE]

    def can_have_transfer_variation(self) -> bool:
        """Can a :any:`LoadingType` with this `LoadCause` support a transfer loading option?"""
         # except for these 5 types, LoadingLayers can have a transfer option
        return not self in [LoadingCause.SELF_DEAD, LoadingCause.HYPERSTATIC, LoadingCause.STRESSING_DEAD, LoadingCause.TEMPERATURE, LoadingCause.SHRINKAGE]

    def can_have_indexed_variations(self) -> bool:
        """Can a :any:`LoadingType` with this `LoadCause` support indexed variations of the `LoadCause`?"""
         # only theese 4 types can have indexed variation
        return self in [LoadingCause.WIND_SERVICE, LoadingCause.WIND_ULTIMATE, LoadingCause.SEISMIC_SERVICE, LoadingCause.SEISMIC_ULTIMATE]

    def can_have_normal_analysis(self) -> bool:
        """This loadings of this cause can use LoadingAnalysisType.NORMAL."""
        # only hyperstatic can't support normal analysis
        return not self in [LoadingCause.HYPERSTATIC]

    def can_have_self_equilibrium_analysis(self) -> bool:
        """This loadings of this cause can use LoadingAnalysisType.SELF_EQUILIBRIUM."""
        # all but these 5 can have self-equilibrium analysis
        return not self in [LoadingCause.SELF_DEAD, LoadingCause.BALANCE, LoadingCause.HYPERSTATIC, LoadingCause.TEMPERATURE, LoadingCause.SHRINKAGE]

    def can_have_hyperstatic_analysis(self) -> bool:
        """This loadings of this cause can use LoadingAnalysisType.HYPERSTATIC."""
        # only hyperstatic supports that type of analysis
        return self in [LoadingCause.HYPERSTATIC]

    # INTERNAL OPERATIONS

    @classmethod
    def _to_API(cls, internal_value: str) -> LoadingCause:
        """Convert the internal value to the BeamBehavior value (raise exception if invalid)."""
        return LoadingCause(internal_value) # will raise exception if invalid

    def _to_internal(self) -> str:
        """Convert the enum value into an internal string."""
        return self.value

# -------------------------------------------------------------------------------------------------

class LoadingAnalysisType(Enum):
    """For specifying analysis types for :any:`LoadingLayer`.

    The available values are:

    * NORMAL: standard analysis for the type of loading (force, strain, shrinkage)
    * HYPERSTATIC: special value only allowed on hyperstatic loading types (never attempt to set this value)
    * SELF_EQUILIBRIUM: force analysis with all support removed (applied loads must be in self-equilibrium)    
    """
    NORMAL = "normal"
    HYPERSTATIC = "hyperstatic"
    SELF_EQUILIBRIUM = "floating"

    # PUBLIC OPERATIONS

    def valid_for_loading_cause(self, load_cause: LoadingCause) -> bool:
        """Determine if this LoadingAnalysisType is valid for the given load_cause."""
        if self == LoadingAnalysisType.NORMAL:
            return load_cause.can_have_normal_analysis()

        if self == LoadingAnalysisType.HYPERSTATIC:
            return load_cause.can_have_hyperstatic_analysis()

        if self == LoadingAnalysisType.SELF_EQUILIBRIUM:
            return load_cause.can_have_self_equilibrium_analysis()

        raise Exception("Unknown LoadingAnalysisType: " + str(self))

    # INTERNAL OPERATIONS

    @classmethod
    def _to_API(cls, internal_value: str) -> LoadingAnalysisType:
        """Convert the internal value to the LoadingAnalysisType value (raise exception if invalid)."""
        return LoadingAnalysisType(internal_value) # will raise exception if invalid

    def _to_internal(self) -> str:
        """Convert the enum value into an internal string."""
        return self.value

# -------------------------------------------------------------------------------------------------

class LoadingType:
    """An immutable value holding the type of a :any:`LoadingLayer`.
    
    This is effectively a combination of:
    
    * :any:`cause` : what is causing the load?
    * :any:`is_transfer` : is this a transfer load (applied to this level from other levels)
    * :any:`LoadingType.index` : if this `LoadingType` is indexable, what is its index? (0 for no index)
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = [
         "_cause",
         "_index",
         "_is_transfer"
    ]

    def __init__(self, cause: LoadingCause, is_transfer: bool  = False , index: int  = 0):
        """This constructor should only be called by Model."""

        if is_transfer and not cause.can_have_transfer_variation():
            raise Exception (cause.name + " cannot be used with transfer loadings")

        if (index != 0) and not cause.can_have_indexed_variations():
            raise Exception (cause.name + " cannot be used with indexed variations")    

        if (index == 0) and cause.can_have_indexed_variations():
            raise Exception (cause.name + " must have indices greater than zero")    

        if (index < 0):
            raise Exception ("LoadingType indices must be >= 0")    

        self._cause = cause
        self._is_transfer = is_transfer
        self._index = index

    # PUBLIC PROPERTIES

    cause : LoadingCause = property(lambda self: self._cause, None, None, "The :any:`LoadingCause` of this `LoadingType`.")

    is_transfer : bool = property(lambda self: self._is_transfer, None, None, "Is this loading a transfer variation of the :any:`cause`.")

    index : int = property(lambda self: self._index, None, None, "The index of the variation of of the :any:`cause` (0 if not an indexed variation)")

    # PYTHON EQUALITY OPERATIONS

    def __eq__(self,obj):
        """Equals operation for Data objects"""
        if (obj.__class__ == self.__class__):
            return (self._cause == obj._cause) and (self._is_transfer == obj._is_transfer) and (self._index == obj._index)
        else:
            return False


    # INTERNAL OPERATIONS

    def _to_internal(self) -> str:
        """Create the string representation of this LoadingType to store."""
        # the strings to be created look like:
        #   "other_dead"
        #   "other_dead_transfer"
        #   "wind_service_1"
        #   "wind_service_1_transfer"
        value = self.cause._to_internal()

        if self.index > 0:
            value = value + str(self.index)

        if self.is_transfer:
            value = value + "_transfer"

        return value

    @classmethod
    def _to_API(cls, value: str) -> LoadingType:
        """Create a LoadingType from the given value."""
        
        # find the cause
        # note that cause names are unique and will only appear at the start of values
        for loading_cause in LoadingCause:
            internal_loading_cause = loading_cause._to_internal()
            if value.startswith(internal_loading_cause):
                cause = loading_cause
                remaining_value = value[len(internal_loading_cause):]
                break
        
        if remaining_value is None:
            raise Exception("Unexpected LoadingType value: " + value)

        # determine if this is transfer
        transfer_value = "_transfer"
        is_transfer = remaining_value.endswith(transfer_value)
        if is_transfer:
            index_value = remaining_value[: len(remaining_value) - len(transfer_value)]
        else:
            index_value = remaining_value

        # determine index, there are 3 options:
        #   index_value is empty (index is zero)
        #   index_value is an integer
        #   index_value is invalid
        if len(index_value) == 0:
            index = 0
        else:
            try:
                index = int(index_value)
                assert index > 0
            except:
                raise Exception("Unexpected LoadingType value: " + value)
        
        # this can raise an exception if the combination of the 3 values is invalid
        return LoadingType(cause, is_transfer, index)

# -------------------------------------------------------------------------------------------------


class LoadingLayer(FullResultLayer):
    """LoadingLayer is an abstract superclass for :any:`ForceLoadingLayer`, :any:`TemperatureLoadingLayer` and :any:`ShrinkageLoadingLayer`.
    
    It is NOT a superclass for :any:`MassLoadingLayer` as that layer does not actually define a loading that can be analyzed.
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

        # set _read_only flag based on the type of loading
        loading_type = self._get_string_property("LoadingType")
        self._read_only = (loading_type == "self_dead") or (loading_type == "balance") or (loading_type == "hyperstatic")

    # INTERNAL SUPPORT FOR loading_type and analysis_type
    # (required because there are strict rules for setting, not any value can be set)

    def _get_loading_type(self) -> LoadingType:
        """Get the loading type from this LoadingLayer."""
        internal_string = self._get_string_property("LoadingType")
        return LoadingType._to_API(internal_string)

    def _get_analysis_type(self) -> LoadingAnalysisType:
        """Get the analysis type from this LoadingLayer."""
        internal_string = self._get_string_property("AnalysisType")
        return LoadingAnalysisType._to_API(internal_string)

    def _set_loading_type(self, value: LoadingType) -> None:
        """Sets the given loading type, if that is valid."""
        self._set_property_raise_if_read_only()

        # cannot reset certain loading types
        current_loading_type = self._get_loading_type()
        if not current_loading_type.cause.is_changable_in_loading():
            # hit this for Shrinkage and Temperature types, which are not read-only
            raise Exception("LoadingLayer with loading_type of " + current_loading_type.cause.name + "cannot have its loading_type changed.")
        
        # also cannot set to those unchangable loading types
        if not value.cause.is_changable_in_loading():
            raise Exception("Cannot change a LoadingLayer to have a loading_type of " + value.cause.name + ".")

        # finally check the analysis type (don't expect this will ever be a problem with current options)
        current_analysis_type  = self._get_analysis_type()
        if not current_analysis_type.valid_for_loading_cause(value.cause):
            raise Exception("Cannot change a LoadingLayer to have a loading_type of " + value.cause.name + "when it has analysis_type of " + current_analysis_type.name + ".")            
        
        self._set_string_property("LoadingType", value._to_internal())

    def _set_analysis_type(self, value: LoadingAnalysisType) -> None:
        """Sets the given analysis type, if that is valid."""
        self._set_property_raise_if_read_only()

        # cannot reset certain loading types
        loading_type = self._get_loading_type()

        if not value.valid_for_loading_cause(loading_type.cause):
            raise Exception("Cannot set LoadingAnalysisType " + value.name + "in LoadingLayer with loading cause " + loading_type.cause.name + ".")
        
        self._set_string_property("AnalysisType", value._to_internal())

    # PUBLIC PROPERTIES

    loading_type : LoadingType = property(_get_loading_type, _set_loading_type, None, "The :any:`LoadingType` of this `LoadingLayer`.")

    analysis_type : LoadingAnalysisType = property(_get_analysis_type, _set_analysis_type, None, "The :any:`LoadingAnalysisType` of this `LoadingLayer`.")

    # PUBLIC OPERATIONS

    # this needs to be overridden whereever deletion is not available
    def delete(self) -> None:
        """Removes this `LoadingLayer` from the :any:`Model`."""
        self._delete()



