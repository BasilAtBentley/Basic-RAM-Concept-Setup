#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# ****** NOT EXPOSING CALCULATIONS AT THIS TIME *********
# # STANDARD LIBRARY IMPORTS
# from __future__ import annotations
# from typing import TYPE_CHECKING

# # THIRD PARTY IMPORTS

# # INTERNAL (THIS LIBRARY) IMPORTS
# from .data import Data

# # IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
# if TYPE_CHECKING:
#     from .calc_options import CalcOptions
#     from .model import Model

# # -------------------------------------------------------------------------------------------------

# class Calculations(Data):
#     """Calculations exists solely as a parent for CalcOptions.
    
#     Calculations contains no useful properties.
#     There is always 1 Calculations object and it is a child of MasterData.
#     """
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    #__slots__ = []

    
#     def __init__(self, uid: int, model: Model):
#         """This constructor should only be called by Model."""

#         super().__init__(uid, model)

#     # KEY CHILD ACCESSORS

#     def get_calc_options(self) -> CalcOptions:
#         """Gets the CalcOptions child Data."""

#         return self._get_only_child_of_type("CalcOptions")

