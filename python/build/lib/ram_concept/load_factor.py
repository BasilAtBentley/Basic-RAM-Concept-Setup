#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from sys import float_info
from typing import TYPE_CHECKING

# THIRD PARTY IMPORTS

# INTERNAL (THIS LIBRARY) IMPORTS
from .add_property import _float_property
from .add_property import _readonly_data_property
from .data import Data

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .loading_layer import LoadingLayer
    from .model import Model

# -------------------------------------------------------------------------------------------------

class LoadFactor(Data):
    """`LoadFactor` represents the load factors with which a :any:`LoadingLayer` is included in a :any:`LoadComboLayer`.

    `LoadFactors` are created and deleted automatically as `LoadComboLayers` and `LoadingLayers` are created and deleted.

    If the relevant :any:`LoadComboLayer.summing_type` is :any:`LoadComboSummingType.LATERAL_GROUP` and this `LoadFactor`
    refers to a lateral loading, then this `LoadFactor` and its values are ignored.

    If the relevant :any:`LoadComboLayer.analysis_type` is :any:`LoadComboAnalysisType.NONLINEAR` then the `alternate_load_factor`
    is ignored.

    `LoadFactors` are accessed through :any:`LoadComboLayer.load_factor`.
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []

    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # PUBLIC PROPERTIES

    # name inherited from Data
    # number inherited from Data, but not useful

    standard_load_factor: float = _float_property("StandardLoadFactor", "The standard load factor to multiply loading results by.")

    alternate_envelope_load_factor: float = _float_property("AltEnvelopeLoadFactor", "The load factor to multiply loading results by when considering enveloping.")

    loading: LoadingLayer = _readonly_data_property("Loading", "The :any:`LoadingLayer` to which the factors apply.")





    