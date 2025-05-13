#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# STANDARD LIBRARY IMPORTS
from __future__ import annotations
from enum import Enum
from typing import List
from typing import TYPE_CHECKING

# THIRD PARTY IMPORTS

# INTERNAL (THIS LIBRARY) IMPORTS
from .anchor_system import AnchorSystem
from .anchor_systems import AnchorSystems
from .area_spring import AreaSpring
from .area_spring import DefaultAreaSpring
from .area_load import AreaLoad
from .area_load import DefaultAreaLoad
from .beam import Beam
from .beam import DefaultBeam
from .bracket_parser import BracketParser
from .cad_manager import CadManager
from .calc_options import CalcOptions
from .column import Column
from .column import DefaultColumn
from .concrete import Concrete
from .concretes import Concretes
from .data import Data
from .duct_system import DuctSystem
from .duct_systems import DuctSystems
from .elements import ColumnElement
from .elements import SlabElement
from .elements import WallElement
from .elements import WallElementGroup
from .element_layer import ElementLayer
from .force_loading_layer import ForceLoadingLayer
from .jack import DefaultJack
from .jack import Jack
from .line_load import LineLoad
from .line_load import DefaultLineLoad
from .line_spring import LineSpring
from .line_spring import DefaultLineSpring
from .line_support import LineSupport
from .line_support import DefaultLineSupport
from .load_combo_layer import LoadComboLayer
from .load_factor import LoadFactor
from .point_load import PointLoad
from .point_load import DefaultPointLoad
from .point_spring import PointSpring
from .point_spring import DefaultPointSpring
from .point_support import PointSupport
from .point_support import DefaultPointSupport
from .pt_system import PTSystem
from .pt_systems import PTSystems
from .shrinkage_area_load import ShrinkageAreaLoad
from .shrinkage_area_load import DefaultShrinkageAreaLoad
from .shrinkage_loading_layer import ShrinkageLoadingLayer
from .signs import Signs
from .slab_area import SlabArea
from .slab_area import DefaultSlabArea
from .slab_opening import SlabOpening
from .slab_opening import DefaultSlabOpening
from .strand_material import StrandMaterial
from .strand_materials import StrandMaterials
from .structure_layer import StructureLayer
from .temperature_area_load import TemperatureAreaLoad
from .temperature_area_load import DefaultTemperatureAreaLoad
from .temperature_loading_layer import TemperatureLoadingLayer
from .tendon_layer import TendonLayer
from .tendon_node import TendonNode
from .tendon_segment import DefaultTendonSegment
from .tendon_segment import TendonSegment
from .units import Units
from .wall import Wall
from .wall import DefaultWall

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
        from .concept import Concept

# -------------------------------------------------------------------------------------------------

# -------------------------------------------------------------------------------------------------

class DesignCode(Enum):
    """For specifying concrete design code for new model setup.

    The available values are:

    * ACI318_99US: ACI 318-99 with US customary unit defaults
    * ACI318_99SI: ACI 318-99 with SI unit defaults
    * ACI318_02US: ACI 318-02 with US customary unit defaults
    * ACI318_02SI: ACI 318-02 with SI unit defaults
    * ACI318_05US: ACI 318-05 with US customary unit defaults
    * ACI318_05SI: ACI 318-05 with SI unit defaults
    * ACI318_08US: ACI 318-08 with US customary unit defaults
    * ACI318_08SI: ACI 318-08 with SI unit defaults
    * ACI318_11US: ACI 318-11 with US customary unit defaults
    * ACI318_11SI: ACI 318-11 with SI unit defaults
    * ACI318_14US: ACI 318-14 with US customary unit defaults
    * ACI318_14SI: ACI 318-14 with SI unit defaults
    * ACI318_19US: ACI 318-19 with US customary unit defaults
    * ACI318_19SI: ACI 318-19 with SI unit defaults
    * AS3600_2001: AS 3600-2001
    * AS3600_2009: AS 3600-2009
    * AS3600_2018: AS 3600-2018
    * BS8110_1997: BS 8110 : 1997 (Amd. #1 & #2)
    * BS8110_1997_Amd3: BS 8110 : 1997 (Amd. #1 - #3)
    * CAN_2004: CSA A23.3-04
    * EC2_2004UK:  Eurocode 2-2004 (UK Annex)
    * EC2_2004: Eurocode 2-2004
    * IS456_2000: IS 456-2000    
    """
    ACI318_99US = "ACI318_99US"
    ACI318_99SI = "ACI318_99SI"
    ACI318_02US = "ACI318_02US"
    ACI318_02SI = "ACI318_02SI"
    ACI318_05US = "ACI318_05US"
    ACI318_05SI = "ACI318_05SI"
    ACI318_08US = "ACI318_08US"
    ACI318_08SI = "ACI318_08SI"
    ACI318_11US = "ACI318_11US"
    ACI318_11SI = "ACI318_11SI"
    ACI318_14US = "ACI318_14US"
    ACI318_14SI = "ACI318_14SI"
    ACI318_19US = "ACI318_19US"
    ACI318_19SI = "ACI318_19SI"
    AS3600_2001 = "AS3600_2001"
    AS3600_2009 = "AS3600_2009"
    AS3600_2018 = "AS3600_2018"
    BS8110_1997 = "BS8110_1997"
    BS8110_1997_Amd3 = "BS8110_1997_Amd3"
    CAN_2004   = "CAN_2004"
    EC2_2004UK = "EC2_2004UK"
    EC2_2004   = "EC2_2004"
    IS456_2000 = "IS456_2000"

    # INTERNAL OPERATIONS

    def _to_internal(self) -> str:
        """Convert the enum value into an internal string."""
        return self.value

# -------------------------------------------------------------------------------------------------

class StructureType(Enum):
    """For specifying structure type for new model setup.

    The available values are:

    * ELEVATED: Elevated slab
    * MAT: Mat/Raft foundation
    """
    ELEVATED = "ELEVATED"
    MAT = "MAT"
    
    # INTERNAL OPERATIONS

    def _to_internal(self) -> str:
        """Convert the enum value into an internal string."""
        return self.value

# -------------------------------------------------------------------------------------------------

class Model:
    """Model represents an in-memory (opened or never-saved) file in the RAM Concept process.

    Model is effectively a hierarchical container of :any:`Data` objects. Only the portions of the hierarchy
    that are available for scripting are exposed.

    There can be a maximum of 1 `Model` associated with any :any:`Concept` process at one time. There can be
    multiple :any:`Concept` processes, so multiple `Models` can exist simultaneously if there is a need.
    
    This class should never be be subclassed.

    `Models` should ONLY be constructed via the :any:`Concept` class. The methods to do that are:

    - :any:`Concept.new_model`
    - :any:`Concept.open_file`
    """

    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = [
        "_concept"
    ]

    def __init__(self, concept: Concept):
        """Initializes this to be associated with the given `Concept` process.

        This class is intended to be only constructed by the `Concept` class."""
        super().__init__()
        self._concept = concept

    # PUBLIC PROPERTIES

    cad_manager: CadManager = property(lambda self: self._get_data_from_key("$CAD_MANAGER"), None, None, "The singleton :any:`CadManager` which manages all the CadLayers")

    calc_options: CalcOptions = property(lambda self: self._get_data_from_key("$CALC_OPTIONS"), None, None, "The singleton :any:`CalcOptions` which manages most calculation options.")

    concretes: Concretes = property(lambda self: self._get_data_from_key("$CONCRETES"), None, None, "The singleton :any:`Concretes` which manages all the `Concrete` mixes.")
    
    strand_materials: StrandMaterials = property(lambda self: self._get_data_from_key("$STRAND_MATERIALS"), None, None, "The singleton :any:`StrandMaterials` which manages all the `StrandMaterial`.")

    anchor_systems: AnchorSystems = property(lambda self: self._get_data_from_key("$ANCHOR_SYSTEMS"), None, None, "The singleton :any:`AnchorSystems` which manages all the `AnchorSystem`.")

    duct_systems: DuctSystems = property(lambda self: self._get_data_from_key("$DUCT_SYSTEMS"), None, None, "The singleton :any:`DuctSystems` which manages all the `DuctSystem`.")

    pt_systems: PTSystems = property(lambda self: self._get_data_from_key("$PT_SYSTEMS"), None, None, "The singleton :any:`PTSystems` which manages all the `PTSystem`.")

    signs: Signs = property(lambda self: self._get_data_from_key("$SIGNS"), None, None, "The singleton :any:`Signs` which manages sign conventions.")

    units: Units = property(lambda self: self._get_data_from_key("$UNITS"), None, None, "The singleton :any:`Units` which manages unit settings.")
    
    # Access already enabled above
    # "$CAD_MANAGER"
    # "$CALC_OPTIONS"
    # "$CONCRETES"
    # "$STRAND_MATERIALS"
    # "$ANCOR_SYSTEMS"
    # "$DUCT_SYSTEMS"
    # "$PT_SYSTEMS"
    # "$SIGNS"
    # "$UNITS"   

    # Access enabled through CadManager
    # "$STRUCTURE_LAYER"
    # "$ELEMENT_LAYER"

    # Items we may want to add future access for
    # "$CALC_DATA"
    # "$MATERIALS"
    # "$REBARS"
    # "$SSR_SYSTEMS"
    # "$BANDED_TENDON_GROUPS"
    # "$DISTRIBUTED_TENDON_GROUPS"
    # "$PROFILE_POLYLINE_GROUPS"
    # "$DESIGN_RULES"
    # "$SPAN_DETAILERS"
    # "$DXF_LAYER"
    #  "$MASTER_DATA"
    # "$SELF_DEAD_LOADING_LAYER"
    # "$DIRECT_BALANCE_LOADING_LAYER"
    # "$HYPERSTATIC_LOADING_LAYER"
    # "$LOAD_PATTERN_LAYER"
    # "$DESIGN_SUMMARY_LAYER"
    # "$DESIGN_STRIP_LAYER"
    # "$DYNAMIC_RESULT_LAYER"
    # "$CALCULATIONS"
    # "$COVER"
    # "$TABLE_OF_CONTENTS"
    # "$ESTIMATOR"
    # "$PLANS_MANAGER"
    # "$PERSPECTIVES_MANAGER"
    # "$GRAPHIC_SPEC_MANAGER"
    # "$REPORT_MANAGER"
    # "$EC2ANNEX"

    # MODEL INITIALIZATION/SETUP OPERATIONS

    def setup_new_model(self, code: DesignCode, structure: StructureType)->None:
        """Set up a fresh/blank new model for the given code and structure type.

        This is intended to be called immediately after :any:`Concept.new_model` returns this `Model`.
        """
        self._command("[SETUP_NEW_MODEL][" + code._to_internal() + "][" + structure._to_internal() + "]")

    # MAJOR MODEL OPERATIONS

    def calc_all(self, timeout_seconds: int = None) -> None:
        """Calculate everything (except mesh, vibration and long-term deflections) in the Model.
        
        Parameters
        ----------
        timeout_seconds
            The number of seconds to wait for a response from the server (if None, a default value is used)
        """
        self._command("[CALC_ALL]", timeout_seconds)

    def generate_mesh(self) -> None:
        """Regenerate the mesh, using the Model's meshing parameters.
        The desired element size is a property of :any:`calc_options` which is accessable via :any:`Model.calc_options`"""

        self._command("[GENERATE_MESH]")

    # INTERNAL CORE COMMAND OPERATION

    def _command(self, cmd: str, timeout_seconds: int = None) -> str:
        """Send the command to the RAM Concept process.

        THIS METHOD IS FOR EXCLUSIVE USE BY THE FRAMEWORK.
        
        Parameters
        ----------
        cmd
            The command to execute. Must be in bracket string format.
        timeout_seconds
            The number of seconds to wait for a response before timing out (if None, default value is used)

        Returns
        -------
        str
            The response to the command.
        """
        return self._concept._command(cmd, timeout_seconds)

    # "FILE" OPERATIONS (close, save, etc.)

    def close_model(self) -> None:
        """Close this `Model` (file) in the RAM Concept process.

        The `Model`/file is not saved. This `Model` is not useful for anything after closing.
        """
        self._command('[CLOSE_MODEL]')
        self._concept._model_closed(self)
        self._concept = None

    def save_file(self, file_path: str) -> None:
        """Save this model to the given file.
        
        Parameters
        ----------
        file_path
            Full path to for the location to save the file.      
        """
        self._command("[SAVE_FILE][" + file_path + "]")

    # DATA CREATION/WRAPPING OPERATIONS

    def _get_data(self, uid_or_key: str) -> Data:
        """Get the Data (or more-specific subclass) for the given uid (integer string).

        If a Data already exists for the uid it is NOT reused.

        Parameters
        ----------
        uid
            The Data id, usually an integer string, but special key strings starting with $ are also accepted.
            If the string is empty, None is returned.
        
        Returns
        -------
        Data (or more specific subclass)
            The Data corresponding to the uid. None if uid = ""
        """
        if(len(uid_or_key) == 0):
            return None

        if(uid_or_key[0:1] == "$"):
            return self._get_data_from_key(uid_or_key)

        return self._get_data_from_uid(int(uid_or_key))

    def _get_datas(self, uids: List[str]) -> List[Data]:
        """Get the Datas (or more-specific subclasses) for the given uids.

        Parameters
        ----------
        uid
            The Data ids, usually an integer strings, but special key strings starting with $ are also accepted.
            If the string is empty, None is returned for that slot in the List
        
        Returns
        -------
        List[Data] (or List[more specific subclasses])
            The Datas corresponding to the uids. None for any uid = ""
        """
        return [self._get_data(uid) for uid in uids]

    def _get_datas_from_bracket_string(self, uid_bracket_string: str) -> List[Data]:
        """Get the Datas (or more specific subclasses) that correspond to the uids in the given bracket string."""
        uid_tokens: List[str] = BracketParser.parse(uid_bracket_string)
        return self._get_datas(uid_tokens)



    # INTERNAL DATA CREATION OPERATIONS

    def _get_data_from_uid(self, uid: int) -> Data:
        """Create the Data (or more-specific subclass) for the given uid (integer string).

        If a Data already exists for the uid it is NOT reused.

        THIS METHOD IS FOR EXCLUSIVE USE BY THE FRAMEWORK.

        Parameters
        ----------
        uid
            An an integer Data uid
        
        Returns
        -------
        Data (or more specific subclass)
            The Data corresponding to the uid.
        """
        # had problem with str sneaking through
        assert type(uid) is int

        # figure out the data type
        cmd = "[WITH_TARGET][" + str(uid) + "][[GET_TYPE]]"
        data_type = self._command(cmd)

        # Most classes have exactly the same internal type name as their Python class name.
        # For those classes we can use the module dictionary to find the class and create the instance.
        module_dict = globals() # module-globals, not package globals (so we still need to import the names at the top of the file
        if data_type in module_dict:
            class_to_instantiate = module_dict[data_type]
            return class_to_instantiate(uid, self)
            
        # Some classes have internal type names that vary from the Python class name, we need to special-case those

        if(  data_type == "AreaLoadForShrinkage"):          return ShrinkageAreaLoad(uid, self)
        elif(data_type == "AreaLoadForTemperature"):        return TemperatureAreaLoad(uid, self)
        elif(data_type == "DefaultAreaLoadForShrinkage"):   return DefaultShrinkageAreaLoad(uid, self)
        elif(data_type == "DefaultAreaLoadForTemperature"): return DefaultTemperatureAreaLoad(uid, self)
        elif(data_type == "DefaultTendon"):                 return DefaultTendonSegment(uid, self)
        elif(data_type == "LoadingLayer"):                  return ForceLoadingLayer(uid, self)
        elif(data_type == "Tendon"):                        return TendonSegment(uid, self)
        elif(data_type == "TriSlabElement"):                return SlabElement(uid, self)
        elif(data_type == "QuadSlabElement"):               return SlabElement(uid, self)
        else:
            # our formal API does not support using Data concretely, but someone going off-road could use it with private methods
            return Data(uid, self)

    def _get_data_from_key(self, key: str) -> Data:
        """Create the Data (or more-specific subclass) corresponding to the given special key value (usually starting with $).

        If a Data already exists for the uid (and key) it is NOT reused.

        THIS METHOD IS FOR EXCLUSIVE USE BY THE FRAMEWORK.
        
        Parameters
        ----------
        key
            A special string corresponding to a particular Data.
        
        Returns
        -------
        Data (or more specific subclass)
            The Data corresponding to the key.
        """
        cmd = "[GET_UID_FOR_KEY][" + key + "]"
        stringUid = self._command(cmd)
        uid = int(stringUid)
        return self._get_data_from_uid(uid)

       
