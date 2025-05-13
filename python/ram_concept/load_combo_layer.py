#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# to avoid circular module dependencies, when references only used for type hints
# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from enum import Enum
from typing import List
from typing import TYPE_CHECKING

# THIRD PARTY IMPORTS

# INTERNAL (THIS LIBRARY) IMPORTS
from .add_property import _enum_int_property
from .add_property import _data_child_list_property
from .add_property import _float_property
from .result_layers import FullResultLayer

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .loading_layer import LoadingLayer
    from .load_factor import LoadFactor
    from .model import Model

# -------------------------------------------------------------------------------------------------

class LoadComboSummingType(Enum):
    """The strategy for summing of :any:`LoadingLayer` within of a :any:`LoadComboLayer`.

    The available values are:

    * SINGLE: The :any:`LoadComboLayer` represents a single factored set of :any:`LoadingLayer`
    * LATERAL_GROUP: The :any:`LoadComboLayer` represents the envelope of a generated set of virtual load combinations based on the key lateral loading type. See RAM Concept manual for details.
    """
    SINGLE = 1
    LATERAL_GROUP = 2
    
    # INTERNAL OPERATIONS

    @classmethod
    def _to_API(cls, internal_value: int) -> LoadComboSummingType:
        """Convert the internal value to the LoadComboType value (raise exception if invalid)."""
        return LoadComboSummingType(internal_value) # will raise exception if invalid

    def _to_internal(self) -> int:
        """Convert the enum value into an internal integer."""
        return self.value

# -------------------------------------------------------------------------------------------------

class LoadComboLateralGroupType(Enum):
    """The :any:`LoadingLayer` type that is considered when :any:`LoadComboLayer.summing_type` is :any:`LoadComboSummingType.LATERAL_GROUP`.

    The available values are:

    * WIND_SERVICE: Service level wind loads (corresponds to :any:`LoadingCause.WIND_SERVICE`)
    * WIND_ULTIMATE: Ultimate level wind loads (corresponds to :any:`LoadingCause.WIND_ULTIMATE`)
    * SEISMIC_SERVICE: Service level seismic loads (corresponds to :any:`LoadingCause.SEISMIC_SERVICE`)
    * SEISMIC_ULTIMATE: Ultimate level seismic loads (corresponds to :any:`LoadingCause.SEISMIC_ULTIMATE`)
    """
    WIND_SERVICE = 100
    WIND_ULTIMATE = 200
    SEISMIC_SERVICE = 300
    SEISMIC_ULTIMATE = 400
    
    # INTERNAL OPERATIONS

    @classmethod
    def _to_API(cls, internal_value: int) -> LoadComboLateralGroupType:
        """Convert the internal value to the LoadComboLateralGroupType value (raise exception if invalid)."""
        return LoadComboLateralGroupType(internal_value) # will raise exception if invalid

    def _to_internal(self) -> int:
        """Convert the enum value into an internal integer."""
        return self.value

# -------------------------------------------------------------------------------------------------

class LoadComboAnalysisType(Enum):
    """The analysis type of a :any:`LoadComboLayer`.

    The available values are:

    * LINEAR: Strictly linear summing of :any:`LoadingLayer` results is performed
    * NONLINEAR: Zero-tension iterations are performed.
    """
    LINEAR = 1
    NONLINEAR = 2
    
    # INTERNAL OPERATIONS

    @classmethod
    def _to_API(cls, internal_value: int) -> LoadComboAnalysisType:
        """Convert the internal value to the LoadComboAnalysisType value (raise exception if invalid)."""
        return LoadComboAnalysisType(internal_value) # will raise exception if invalid

    def _to_internal(self) -> int:
        """Convert the enum value into an internal integer."""
        return self.value

# -------------------------------------------------------------------------------------------------


class LoadComboLayer(FullResultLayer):
    """`LoadComboLayer` represents a load combination with factors that can be applied to :any:`LoadingLayer`.
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    # FUTURE: add criteria layer properties when we have them

    summing_type: LoadComboSummingType = _enum_int_property("LoadComboType", LoadComboSummingType, ":any:`LoadComboSummingType`: The method for summing of :any:`LoadingLayer`.")

    analysis_type: LoadComboAnalysisType = _enum_int_property("LoadComboAnalysis", LoadComboAnalysisType, ":any:`LoadComboAnalysisType`: The analysis method used for this `LoadComboLayer`.")

    group_loading_type: LoadComboLateralGroupType = _enum_int_property("GroupLoadingType", LoadComboLateralGroupType, ":any:`LoadComboLateralGroupType`: The :any:`LoadingLayer` type that is considered when `summing_type` is `LATERAL_GROUP`")

    group_standard_load_factor: float = _float_property("GroupStandardLoadFactor", "The standard load factor to multiply `group_loading_type` results by.")

    group_alternate_envelope_load_factor: float = _float_property("GroupAltEnvelopeLoadFactor", "The load factor to multiply `group_loading_type` results by when considering enveloping.")

    load_factors : List[LoadFactor] = _data_child_list_property("LoadFactor", "All of the :any:`LoadFactor` for this `LoadComboLayer`")

    # PUBLIC OPERATIONS

    def load_factor(self, loading_layer: LoadingLayer) -> LoadFactor:
        """Get the :any:`LoadFactor` corresponding to the given :any:`LoadingLayer`."""
        for load_factor in self.load_factors:
            if load_factor.loading == loading_layer:
                return load_factor
        
        # never expect to get here
        raise Exception("No LoadFactor for given LoadingLayer (" + loading_layer.name + ")???")

    def delete(self) -> None:
        """Remove this `LoadComboLayer` from the :any:`Model`."""
        self._delete()



