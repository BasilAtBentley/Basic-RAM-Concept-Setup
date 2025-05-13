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
from .data import Data

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .model import Model

# -------------------------------------------------------------------------------------------------

class Signs(Data):
    """Signs represents the singleton Signs objects in a :any:`Model`, which controls the user sign convention.
    
    The API operates using the same sign convention as the RAM Concept UI. The methods in this class
    affect both the UI and the API. Generally you will want to:

    - Call :any:`get_signs` after opening the file, and store the return value.
    - Call :any:`set_positive_signs` to set the sign system as being all positive
    - Call :any:`set_signs` before closing (and saving) the file to restore the units to their original state.

    For newly created files, you will want to call :any:`set_standard_signs` prior to closing (and saving)
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)
  
    # PUBLIC OPERATIONS

    def set_positive_signs(self) -> None:
        """Sets the user sign convention (used by the API) to be:

        - All forces positive in positive axis direction (e.g. both loads and reactions are positive upward)
        - All moments positive using right-hand rule about axes
        - All displacements positive along positive axis direction
        - All rotations positive using right-hand rule about axes
        - Sagging moments positive
        - Tensile stresses positive
        - Etc.
        """
        self._command("[RESET_SIGNS][all_positive]")

    def set_standard_signs(self) -> None:
        """Sets the user sign convention (also used by the API) to one that feels natural to most users."""
        self._command("[RESET_SIGNS][standard]")


    def get_signs(self) -> str:
        """Returns the current sign settings that affect both the API and the UI.
        The return value for this is only intended for use in the :any:`set_signs` method.
        The `get_signs`/`set_signs` pair allow you to restore the signs in a file after modifying them with :any:`set_positive_signs`."""
        return self._command("[GET_SIGNS]")

    def set_signs(self, sign_settings: str) -> None:
        """Restores the sign settings to the given value, which is required to have been returned from :any:`get_signs`"""
        self._command("[SET_SIGNS][" + sign_settings + "]")
        