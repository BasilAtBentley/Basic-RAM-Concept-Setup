#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------


from math import pi

from ram_concept.anchor_system import AnchorSystem
from ram_concept.anchor_system import AnchorType
from ram_concept.anchor_systems import AnchorSystems
from ram_concept.concrete import Concrete
from ram_concept.concretes import Concretes
from ram_concept.duct_system import DuctSystem
from ram_concept.duct_system import DuctType
from ram_concept.duct_system import DuctShape
from ram_concept.duct_systems import DuctSystems
from ram_concept.model import Model
from ram_concept.pt_system import PTSystem
from ram_concept.pt_systems import PTSystems
from ram_concept.duct_system import PTSystemType
from ram_concept.strand_material import StrandMaterial
from ram_concept.strand_materials import StrandMaterials


def add_materials(model: Model):
    """Adds materials required for the structure."""

    # CONCRETE MIXES

    # add a 45 MPa concrete mix
    # note: adding a concrete mix with the name of an existing concrete mix will raise an exception
    concretes = model.concretes
    concrete_mix = concretes.add_concrete("45 MPa")
    concrete_mix.fc_final = 45000000
    concrete_mix.fc_initial = 30000000
    concrete_mix.poissons_ratio = 0.2
    concrete_mix.unit_mass = 2450
    concrete_mix.unit_unit_mass_for_loads = 2500
    concrete_mix.use_code_Ec = True

    # you can optionally delete the materials that come by default that you don't want
    # but you must leave at least 1 (attempting to delete the last one will raise an exception)
    all_concretes = concretes.concretes
    for concrete in all_concretes:
        if concrete.name != "45 MPa":
            concrete.delete()

    # PT SYSTEMS

    # add a Strand Material
    # note: adding a Strand Material with the name of an existing Strand Material will raise an exception
    strand_materials = model.strand_materials
    strand_material = strand_materials.add_strand_material("13mm Strand")
    strand_material.Aps = 100e-6
    strand_material.Eps = 195000e6
    strand_material.Fpy = 1564e6
    strand_material.Fpu = 1840e6

    # add a Duct System
    # note: adding a Duct System with the name of an existing Duct System will raise an exception
    duct_systems = model.duct_systems
    duct_system = duct_systems.add_duct_system("4s Flat")
    duct_system.system_type = PTSystemType.BONDED
    duct_system.duct_width = 70e-3     
    duct_system.strands_per_duct = 4
    duct_system.wobble_friction = 0.005
    duct_system.angular_friction = 0.2 * (pi/180) # due to API consistent units this is per-degree, not per radian
    duct_system.duct_height = 35e-3
    duct_system.duct_shape = DuctShape.FLAT
    duct_system.duct_type = DuctType.CORRUGATED_STEEL

    # add a Anchor System
    # note: adding a Anchor System with the name of an existing Anchor System will raise an exception
    anchor_systems = model.anchor_systems
    anchor_system = anchor_systems.add_anchor_system("FA Multi")
    anchor_system.anchor_type = AnchorType.FLAT_MULTI_PLANE
    anchor_system.anchor_friction = 0.02
    anchor_system.jack_stress = 1564e6
    anchor_system.seating_distance = 6e-3

    # add a PT System
    # note: adding a PT System with the name of an existing PT System will raise an exception
    pt_systems = model.pt_systems
    pt_system = pt_systems.add_pt_system("13mm Bonded")
    pt_system.strand_material = strand_material
    pt_system.duct_system = duct_system
    pt_system.anchor_system = anchor_system
    pt_system.Fse = 1100e6
    pt_system.min_curvature_radius = 2
    pt_system.long_term_losses = 150e6

    # you can optionally delete the materials that come by default that you don't want
    # but you must leave at least 1 (attempting to delete the last one will raise an exception)
    all_strand_materials = strand_materials.strand_materials
    for strand_material in all_strand_materials:
        if strand_material.name != "13mm Strand":
            strand_material.delete()

    all_duct_systems = duct_systems.duct_systems
    for duct_system in all_duct_systems:
        if duct_system.name != "4s Flat":
            duct_system.delete()

    all_anchor_systems = anchor_systems.anchor_systems
    for anchor_system in all_anchor_systems:
        if anchor_system.name != "FA Multi":
            anchor_system.delete()

    all_pt_systems = pt_systems.pt_systems
    for pt_system in all_pt_systems:
        if pt_system.name != "13mm Bonded":
            pt_system.delete()

