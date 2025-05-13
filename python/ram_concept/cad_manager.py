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
from .add_property import _data_child_list_property
from .add_property import _key_data_property
from .add_property import _cad_default_property

# IMPORTS ONLY FOR TYPE CHECKING (may cause circular references if used otherwise)
if TYPE_CHECKING:
    from .area_load import DefaultAreaLoad
    from .area_spring import DefaultAreaSpring
    from .Beam import DefaultBeam
    from .cad_layer import CadLayer
    from .column import DefaultColumn
    from .element_layer import ElementLayer
    from .enums import GeneratedBy
    from .enums import SpanSet
    from .force_loading_layer import ForceLoadingLayer
    from .jack import DefaultJack
    from .line_load import DefaultLineLoad
    from .line_spring import DefaultLineSpring
    from .line_support import DefaultLineSupport
    from .loading_layer import LoadingLayer
    from .load_combo_layer import LoadComboLayer
    from .model import Model
    from .point_load import DefaultPointLoad
    from .point_spring import DefaultPointSpring
    from .point_support import DefaultPointSupport
    from .shrinkage_area_load import DefaultShrinkageAreaLoad
    from .shrinkage_loading_layer import ShrinkageLoadingLayer
    from .slab_area import DefaultSlabArea
    from .slab_opening import DefaultSlabOpening
    from .structure_layer import StructureLayer
    from .temperature_area_load import DefaultTemperatureAreaLoad
    from .temperature_loading_layer import TemperatureLoadingLayer
    from .tendon_layer import TendonLayer
    from .tendon_segment import DefaultTendonSegment
    from .wall import DefaultWall
    from typing import List

# -------------------------------------------------------------------------------------------------

class CadManager(Data):
    """`CadManager` coordinates and contains all the information in the CAD system.
    
    There  is a single `CadManager` that is accessible through :any:`Model.cad_manager`.
    """
    
    # using __slots__ adds efficiency, but mostly it prevents accidentally adding attributes (misspellings, etc.)
    __slots__ = []

    # Internally this encapsulates the behavior of both ACadManager and CadManager
    
    def __init__(self, uid: int, model: Model):
        """This constructor should only be called by Model."""

        super().__init__(uid, model)

    # INTERNAL SUPPORT FOR some combined layer lists

    def _get_all_loading_layers(self) -> List[LoadingLayer]:
        """Get all the LoadingLayers."""
        return self.force_loading_layers + self.temperature_loading_layers + self.shrinkage_loading_layers

    def _get_all_layers(self) -> List[LoadingLayer]:
        """Get all the CadLayers."""

        cmd = "[GET_LAYERS]"
        uids = self._command(cmd)
        layers: List[Data] = self.model._get_datas_from_bracket_string(uids)

        # post-process the list, removing the ones that we don't have type-specific wrappers for
        return [layer for layer in layers if type(layer) != Data]

    # PUBLIC PROPERTIES

    # singleton layers
    
    element_layer: ElementLayer = _key_data_property("$ELEMENT_LAYER", "The singleton :any:`ElementLayer` which contains the finite elements")

    structure_layer: StructureLayer = _key_data_property("$STRUCTURE_LAYER", "The singleton :any:`StructureLayer` which manages mesh-generation CadEntities")

    # non-singleton layer types

    force_loading_layers:       List[ForceLoadingLayer]       = _data_child_list_property("LoadingLayer",            "All of the :any:`ForceLoadingLayer` in the `Model`")
    temperature_loading_layers: List[TemperatureLoadingLayer] = _data_child_list_property("TemperatureLoadingLayer", "All of the :any:`TemperatureLoadingLayer` in the `Model`")
    shrinkage_loading_layers:   List[ShrinkageLoadingLayer]   = _data_child_list_property("ShrinkageLoadingLayer",   "All of the :any:`ShrinkageLoadingLayer` in the `Model`")

    load_combo_layers:          List[LoadComboLayer]          = _data_child_list_property("LoadComboLayer",          "All of the :any:`LoadComboLayer` in the `Model`")   

    tendon_layers:              List[TendonLayer]             = _data_child_list_property("TendonLayer",             "All of the :any:`TendonLayer` in the `Model`")   
    # combinations of layers

    all_loading_layers : List[LoadingLayer] = property(_get_all_loading_layers, None, None, "All the :any:`LoadingLayer` in the `Model`.")
    all_layers         : List[LoadingLayer] = property(_get_all_layers,         None, None, "All the :any:`CadLayer` in the `Model` (this does not return layers that are not exposed in the API).")

    # StructureLayer default objects

    default_point_spring: DefaultPointSpring = _cad_default_property("PointSpring", "The singleton :any:`DefaultPointSpring` that contains the property settings of :any:`PointSpring` that will be created.")
    default_line_spring:  DefaultLineSpring  = _cad_default_property("LineSpring",  "The singleton :any:`DefaultLineSpring` that contains the property settings of :any:`LineSpring` that will be created.")
    default_area_spring:  DefaultAreaSpring  = _cad_default_property("AreaSpring",  "The singleton :any:`DefaultAreaSpring` that contains the property settings of :any:`AreaSpring` that will be created.")

    default_point_support: DefaultPointSupport = _cad_default_property("PointSupport", "The singleton :any:`DefaultPointSupport` that contains the property settings of :any:`PointSupport` that will be created.")
    default_line_support:  DefaultLineSupport  = _cad_default_property("LineSupport",  "The singleton :any:`DefaultLineSupport` that contains the property settings of :any:`LineSupport` that will be created.")

    default_beam:   DefaultBeam   = _cad_default_property("Beam",   "The singleton :any:`DefaultBeam` that contains the property settings of :any:`Beam` that will be created.")
    default_column: DefaultColumn = _cad_default_property("Column", "The singleton :any:`DefaultColumn` that contains the property settings of :any:`Column` that will be created.")
    default_wall:   DefaultWall   = _cad_default_property("Wall",   "The singleton :any:`DefaultWall` that contains the property settings of :any:`Wall` that will be created.")

    default_slab_area:    DefaultSlabArea    = _cad_default_property("SlabArea",    "The singleton :any:`DefaultSlabArea` that contains the property settings of :any:`SlabArea` that will be created.")
    default_slab_opening: DefaultSlabOpening = _cad_default_property("SlabOpening", "The singleton :any:`DefaultSlabOpening` that contains the property settings of :any:`SlabOpening` that will be created.")

    # ForceLoadingLayer default objects

    default_point_load: DefaultPointLoad = _cad_default_property("PointLoad", "The singleton :any:`DefaultPointLoad` that contains the property settings of :any:`PointLoad` that will be created.")
    default_line_load:  DefaultLineLoad  = _cad_default_property("LineLoad",  "The singleton :any:`DefaultLineLoad` that contains the property settings of :any:`LineLoad` that will be created.")
    default_area_load:  DefaultAreaLoad  = _cad_default_property("AreaLoad",  "The singleton :any:`DefaultAreaLoad` that contains the property settings of :any:`AreaLoad` that will be created.")

    # ShrinkageLoadingLayer default objects

    default_shrinkage_area_load:  DefaultShrinkageAreaLoad  = _cad_default_property("AreaLoadForShrinkage",  "The singleton :any:`DefaultShrinkageAreaLoad` that contains the property settings of :any:`ShrinkageAreaLoad` that will be created.")

    # TemperatureLoadingLayer default objects

    default_temperature_area_load:  DefaultTemperatureAreaLoad  = _cad_default_property("AreaLoadForTemperature",  "The singleton :any:`DefaultTemperatureAreaLoad` that contains the property settings of :any:`TemperatureAreaLoad` that will be created.")

    # TendonLayer default objects

    default_tendon_segment: DefaultTendonSegment = _cad_default_property("Tendon", "The singleton :any:`DefaultTendonSegment` that contains the property settings of :any:`TendonSegment` that will be created.")
    default_jack:           DefaultJack          = _cad_default_property("Jack",   "The singleton :any:`DefaultJack` that contains the property settings of :any:`Jack` that will be created.")


    # CHILD ACCESS OPERATIONS

    def force_loading_layer(self, name: str) -> ForceLoadingLayer:
        """Find and return the :any:`ForceLoadingLayer` with the given name."""

        return self._get_named_child_of_type(name, "LoadingLayer")

    def shrinkage_loading_layer(self, name: str) -> ShrinkageLoadingLayer:
        """Find and return the :any:`ShrinkageLoadingLayer` with the given name."""

        return self._get_named_child_of_type(name, "ShrinkageLoadingLayer")

    def temperature_loading_layer(self, name: str) -> TemperatureLoadingLayer:
        """Find and return the :any:`TemperatureLoadingLayer` with the given name."""

        return self._get_named_child_of_type(name, "TemperatureLoadingLayer")

    def load_combo_layer(self, name: str) -> LoadComboLayer:
        """Find and return the :any:`LoadComboLayer` with the given name."""

        return self._get_named_child_of_type(name, "LoadComboLayer")

    def tendon_layer(self, span_set: SpanSet, generated_by: GeneratedBy) -> TendonLayer:
        """Find and return the :any:`TendonLayer` of the given SpanSet with the given generator (user or program)."""
        tendon_layers = self.tendon_layers
        for tendon_layer in tendon_layers:
            if ((tendon_layer.span_set == span_set) and (tendon_layer.generated_by == generated_by)):
                return tendon_layer

        raise Exception("No TendonLayer of span_set " + str(span_set) + " and generated_by " + str(generated_by))

    # INTERNAL LAYER ADDITION OPERATIONS

    def _add_layer(self, layer_type: str, layer_name: str) -> CadLayer:
        """Add and return a layer with the given type and name."""
        return self._add_unique_named_child(layer_type, layer_name)

    # PUBLIC LAYER ADDITION OPERATIONS

    def add_force_loading_layer(self, name: str) -> ForceLoadingLayer:
        """Add a :any:`ForceLoadingLayer` with the given name, and return it."""
        return self._add_layer("LoadingLayer", name)

    def add_temperature_loading_layer(self, name: str) -> TemperatureLoadingLayer:
        """Add a :any:`TemperatureLoadingLayer` with the given name, and return it."""
        return self._add_layer("TemperatureLoadingLayer", name)

    def add_shrinkage_loading_layer(self, name: str) -> ShrinkageLoadingLayer:
        """Add a :any:`ShrinkageLoadingLayer` with the given name, and return it."""
        return self._add_layer("ShrinkageLoadingLayer", name)
    
    def add_load_combo_layer(self, name: str) -> ShrinkageLoadingLayer:
        """Add a :any:`LoadComboLayer` with the given name, and return it."""
        return self._add_layer("LoadComboLayer", name)
        