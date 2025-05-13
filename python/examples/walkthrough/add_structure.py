#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------


from ram_concept.beam import Beam
from ram_concept.beam import DefaultBeam
from ram_concept.beam import BeamBehavior
from ram_concept.column import Column
from ram_concept.column import DefaultColumn
from ram_concept.concrete import Concrete
from ram_concept.concretes import Concretes
from ram_concept.line_segment_2D import LineSegment2D
from ram_concept.model import DesignCode
from ram_concept.model import Model
from ram_concept.point_2D import Point2D
from ram_concept.polygon_2D import Polygon2D
from ram_concept.slab_area import SlabArea
from ram_concept.slab_area import DefaultSlabArea
from ram_concept.slab_area import SlabAreaBehavior
from ram_concept.wall import Wall
from ram_concept.wall import DefaultWall

def add_structure(model: Model):
    """Adds a 16m x 16m structure with 8m spans."""

    # The structure created is a simple 16m x 16m square, with 8m spans:

    #  cbbbbbbbcbbbbbbbc
    #  |               |
    #  |               |
    #  w       c       w
    #  w               w
    #  w               w
    #  wwwwwwwwwwwwwwwww

    # for convenience we'll use the concrete mix we defined earlier
    concretes = model.concretes
    concrete_45 = concretes.concrete("45 MPa") 

    # get the StructureLayer (called "Mesh Input" in the RAM Concept UI)
    cad_manager = model.cad_manager
    structure_layer = cad_manager.structure_layer

    # CREATING THE SLAB

    # we can create the slab and then set the properties, or set the properties of the default slab and then create the slab

    # set the values for SlabAreas to be added
    default_slab_area = cad_manager.default_slab_area
    default_slab_area.thickness = 0.2
    default_slab_area.toc = 0.0
    default_slab_area.behavior = SlabAreaBehavior.TWO_WAY_SLAB
    default_slab_area.concrete = concrete_45
    default_slab_area.priority = 1
    default_slab_area.r_axis = 0.0

    slab_location = Polygon2D([Point2D(0,0), Point2D(16,0), Point2D(16,16), Point2D(0,16)])
    slab_area = structure_layer.add_slab_area(slab_location)

    # if we had wanted to set the properties of the slab after creation, it would look like this:
    # slab_area.thickness = 0.2
    # slab_area.toc = 0.0
    # slab_area.behavior = SlabAreaBehavior.TWO_WAY_SLAB
    # slab_area.concrete = concrete_45
    # slab_area.priority = 1
    # slab_area.r_axis = 0.0

    # CREATE WALLS HALF-WAY AROUND THE SLAB

    # similar to SlabAreas (and almost all CadEntities) we can set the properties for the walls before (using the default) or after creation

      # set the values for walls to be added
    default_wall = cad_manager.default_wall
    default_wall.below_slab = True
    default_wall.compressible = True
    default_wall.concrete = concrete_45
    default_wall.height = 3
    default_wall.fixed_near = False
    default_wall.fixed_far = False
    default_wall.shear_wall = True
    default_wall.thickness = 0.2
    default_wall.use_specified_LLR_parameters = False

    wall_pt1 = Point2D( 0 + .1, 8)
    wall_pt2 = Point2D( 0 + .1, 0 + .1)
    wall_pt3 = Point2D(16 - .1, 0 + .1)
    wall_pt4 = Point2D(16 - .1, 8)
    structure_layer.add_wall(LineSegment2D(wall_pt1,wall_pt2))
    structure_layer.add_wall(LineSegment2D(wall_pt2,wall_pt3))
    structure_layer.add_wall(LineSegment2D(wall_pt3,wall_pt4))

    # CREATE 4 COLUMNS

    # similar to SlabAreas (and almost all CadEntities) we can set the properties for the columns before (using the default) or after creation

    # set the values for columns to be added
    default_column = cad_manager.default_column
    default_column.angle = 0.0
    default_column.below_slab = True
    default_column.compressible = True
    default_column.concrete = concrete_45
    default_column.b = 0.3
    default_column.d = 0.3
    default_column.height = 3.0
    default_column.i_factor = 1.0
    default_column.fixed_near = True
    default_column.fixed_far = True
    default_column.roller = False
    default_column.use_specified_LLR_parameters = False

    column_points = [Point2D(8,8), Point2D(0 + 0.15, 16 - 0.15), Point2D(8, 16 - 0.15), Point2D(16 - 0.15, 16 - 0.15)]
    for column_point in column_points:
        structure_layer.add_column(column_point)

    # ADD 1 BEAM

    # we could set the default_beam values before adding, but in this case we just add the beam and set the values

    beam = structure_layer.add_beam(LineSegment2D(Point2D(0, 16 - 0.25), Point2D(16, 16 - 0.25)))

    beam.thickness = 0.4
    beam.toc = 0.0
    beam.behavior = BeamBehavior.STANDARD_BEAM
    beam.concrete = concrete_45
    beam.priority = 2
    beam.mesh_as_slab = True
    beam.width = 0.5

    # DONE WITH STRUCTURE, SO MESH
    model.generate_mesh()


