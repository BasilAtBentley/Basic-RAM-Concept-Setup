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
from .cad_layer import CadLayer
from .data import Data
from .elements import ColumnElement
from .elements import WallElement
from .elements import WallElementGroup
from .point_5D import Point5D
from .point_6D import Point6D
from .utilities import _user_str_to_API_float

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model
    from typing import Union

# -------------------------------------------------------------------------------------------------

class ReactionContext(Enum):
    """For specifying the context of reactions upon the slab.

    The meaning of the values is:

    * STANDARD: Reaction due to standard load factors and full loading (no pattern loading).
    * MAX_MR: Reaction occuring simultaneously with the maximum Mr reaction.
    * MIN_MR: Reaction occuring simultaneously with the minimum Mr reaction.
    * MAX_MS: Reaction occuring simultaneously with the maximum Ms reaction.
    * MIN_MS: Reaction occuring simultaneously with the minimum Ms reaction.
    * MAX_FZ: Reaction occuring simultaneously with the maximum Fz reaction.
    * MIN_FZ: Reaction occuring simultaneously with the minimum Fz reaction.
    """
    STANDARD = "ContextStandard"
    MAX_FZ = "ContextMaxFz"
    MIN_FZ = "ContextMinFz"
    MAX_MR = "ContextMaxMx"
    MIN_MR = "ContextMinMx"
    MAX_MS = "ContextMaxMy"
    MIN_MS = "ContextMinMy"
    # may add ContextMaxSR in future

    def _to_internal(self) -> str:
        """Convert the enum value into an internal string."""
        return self.value

# -------------------------------------------------------------------------------------------------

class EnvelopeResultLayer(CadLayer):
    """The abstract class represents a CadLayer that contains "enveloped" results.

    "Enveloped" results are those with maximum and minimum values, taken from multiple analyses.
    This contrasts with "full" results which also contain "standard" analysis values which are from
    a single analysis or a linear combination of single analyses.

    Result contexts labeled as "STANDARD" are not available in an `EnvelopedResultLayer` unless it is also
    a :any:`FullResultLayer`.
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # INTERNAL CONSTANTS

    _POINT_REACTION_Fr = "PointReactionFx"
    _POINT_REACTION_Fs = "PointReactionFy"
    _POINT_REACTION_Fz = "PointReactionFz"
    _POINT_REACTION_Mr = "PointReactionMx"
    _POINT_REACTION_Ms = "PointReactionMy"
    _POINT_REACTION_Mz = "PointReactionMz"

    _SUBSECTION_NEAR = "SubsectionNear"

    # RESULT ACCESS OPERATIONS

    # PUBLIC RESULT ACCESS OPERATIONS

    def column_reaction(self, column_element: ColumnElement, context: ReactionContext)->Point5D:
        """Return this layer's reaction upon that slab from the given `ColumnElement`, consistent with the given `ReactionContext`."""
        context_value = context._to_internal()
        Fr = self._analysis_result_float(column_element, self._POINT_REACTION_Fr, self._SUBSECTION_NEAR, context_value)
        Fs = self._analysis_result_float(column_element, self._POINT_REACTION_Fs, self._SUBSECTION_NEAR, context_value)
        Fz = self._analysis_result_float(column_element, self._POINT_REACTION_Fz, self._SUBSECTION_NEAR, context_value)
        Mr = self._analysis_result_float(column_element, self._POINT_REACTION_Mr, self._SUBSECTION_NEAR, context_value)
        Ms = self._analysis_result_float(column_element, self._POINT_REACTION_Ms, self._SUBSECTION_NEAR, context_value)

        return Point5D(Fr, Fs, Fz, Mr, Ms)

    def wall_group_reaction(self, wall_group: Union[WallElement,WallElementGroup], context: ReactionContext)->Point6D:
        """Return this layer's reaction upon that slab from the wall group, consistent with the given ReactionContext.
        For backward compatability, WallElement is accepted as well; THAT USAGE IS DEPRECATED."""

        context_value = context._to_internal()
        # either wall group or wall element will work with the analysis_result_float() function.
        # While WallElement usage is deprecated the wall element version will find the summary and return its result
        Fr = self._analysis_result_float(wall_group, self._POINT_REACTION_Fr, self._SUBSECTION_NEAR, context_value)
        Fs = self._analysis_result_float(wall_group, self._POINT_REACTION_Fs, self._SUBSECTION_NEAR, context_value)
        Fz = self._analysis_result_float(wall_group, self._POINT_REACTION_Fz, self._SUBSECTION_NEAR, context_value)
        Mr = self._analysis_result_float(wall_group, self._POINT_REACTION_Mr, self._SUBSECTION_NEAR, context_value)
        Ms = self._analysis_result_float(wall_group, self._POINT_REACTION_Ms, self._SUBSECTION_NEAR, context_value)
        Mz = self._analysis_result_float(wall_group, self._POINT_REACTION_Mz, self._SUBSECTION_NEAR, context_value)

        return Point6D(Fr, Fs, Fz, Mr, Ms, Mz)

    # INTERNAL RESULT ACCESS OPERATIONS

    def _analysis_result_float(self, data: Data, value: str, sub_section: str, context: str)->float:
        """Return the give value at the given subsection for the given context for this layer."""
        layer_uid = str(self.uid)
        cmd = "[GET_ANALYSIS_USER][" + layer_uid +  "][" + context + "][" + value + "][" + sub_section + "]"
        result = data._command(cmd)

        return _user_str_to_API_float(result)


# -------------------------------------------------------------------------------------------------

class FullResultLayer(EnvelopeResultLayer):
    """The abstract class represents a CadLayer that contains both enveloped and standard results.

    Effectively this layer class supports all the results available through the EnvelopeResultLayer
    plus the contexts labelled as "STANDARD".
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)




    
