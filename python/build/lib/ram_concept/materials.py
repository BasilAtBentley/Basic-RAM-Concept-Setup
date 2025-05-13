#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# ****** NOT EXPOSING MATERIALS AT THIS TIME *********
# # # STANDARD LIBRARY IMPORTS
# from __future__ import annotations
# from typing import TYPE_CHECKING

# # THIRD PARTY IMPORTS

# # INTERNAL (THIS LIBRARY) IMPORTS
# from .data import Data

# # IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
# if TYPE_CHECKING:
#     from .concretes import Concretes
#     from .model import Model

# # -------------------------------------------------------------------------------------------------

# class Materials(Data):
#     """Materials represents the collection of all the Material(s) in the model.
    
#     This is a singleton object which always exists in every model.
#     """
    
#     def __init__(self, uid: int, model: Model):
#         """This constructor should only be called by Model."""

#         super().__init__(uid, model)

#     # KEY CHILD ACCESSORS

#     def get_concretes(self, ) -> Concretes:
#         """Gets the Concretes child Data."""
        
#         return self._get_only_child_of_type("Concretes")
