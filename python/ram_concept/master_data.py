#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# ****** NOT EXPOSING MASTERDATA AT THIS TIME *********
# # STANDARD LIBRARY IMPORTS
# from __future__ import annotations
# from typing import TYPE_CHECKING

# # THIRD PARTY IMPORTS

# # INTERNAL (THIS LIBRARY) IMPORTS
# from .data import Data

# # IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
# if TYPE_CHECKING:
#     from .cad_manager import CadManager
#     from .calculations import Calculations
#     from .materials import Materials
#     from .model import Model
#     from .units import Units

# # -------------------------------------------------------------------------------------------------

# class MasterData(Data):
#     """MasterData represents the top object in the concept data tree."""
    
#     def __init__(self, uid: int, model: Model):
#         """This constructor should only be called by Model."""

#         super().__init__(uid, model)

#     # KEY CHILD ACCESSORS

#     def get_cad_manager(self) -> CadManager:
#         """Gets the CadManager child Data."""

#         return self._get_only_child_of_type("CadManager")

#     def get_calculations(self) -> Calculations:
#         """Gets the Calculations child Data."""

#         return self._get_only_child_of_type("Calculations")

#     def get_materials(self) -> Materials:
#         """Gets the Materials child Data."""

#         return self._get_only_child_of_type("Materials")
               
#     def get_units(self) -> Units:
#         """Gets the Units child Data."""

#         return self._get_only_child_of_type("Units")

