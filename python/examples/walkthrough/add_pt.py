#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------


from ram_concept.enums import ElevationReference
from ram_concept.enums import GeneratedBy
from ram_concept.enums import SpanSet
from ram_concept.jack import DefaultJack
from ram_concept.jack import Jack
from ram_concept.line_segment_2D import LineSegment2D
from ram_concept.model import Model
from ram_concept.point_2D import Point2D
from ram_concept.pt_system import PTSystem
from ram_concept.pt_systems import PTSystems
from ram_concept.tendon_layer import TendonLayer
from ram_concept.tendon_segment import DefaultTendonSegment
from ram_concept.tendon_segment import TendonSegment


def add_pt(model: Model):
    """Adds post-tensioning to the 16m x 16m structure """

    # The structure created is a simple 16m x 16m square, with 8m spans:

    #  cbbbbbbbcbbbbbbbc
    #  |               |
    #  |               |
    #  w       c       w
    #  w               w
    #  w               w
    #  wwwwwwwwwwwwwwwww

    # use a banded- uniform system
    #   banded from left-to-right
    #   uniform from bottom-to-top

    cad_manager = model.cad_manager

    # for convenience we'll use the PTSystem we defined earlier
    pt_systems = model.pt_systems
    pt_13mm = pt_systems.pt_system("13mm Bonded")

    # SET ALL THE PROPERTIES THAT WILL BE IDENTICAL FOR ALL TENDON SEGMENTS
    default_tendon_segment = cad_manager.default_tendon_segment
    default_tendon_segment.pt_system = pt_13mm
    default_tendon_segment.auto_locate_profile_2 = False
    default_tendon_segment.elevation_reference_1 = ElevationReference.ABOVE_SOFFIT
    default_tendon_segment.elevation_reference_2 = ElevationReference.ABOVE_SOFFIT
    default_tendon_segment.harped = False
    default_tendon_segment.inflection_ratio = 0.1
    default_tendon_segment.strand_to_duct_offset = 11e-3

    # SET ALL THE PROPERTIES THAT WILL BE IDENTICAL FOR ALL JACKS
    default_jack = cad_manager.default_jack
    default_jack.use_pt_system_defaults = True

    # BANDED "LONGITUDE" TENDONS
    longitude_tendon_layer = cad_manager.tendon_layer(SpanSet.LONGITUDE, GeneratedBy.USER)
    x_coords = [0.1, 4, 8, 12, 16 - 0.1]  # x-coordinates for the profile points

    # CENTER LONGITUDE TENDONS
    default_tendon_segment.strand_count = 20
    profiles = [0.1, 0.04, .140, 0.04, 0.1]  # profile values for the profile points

    for i_segment in range(0,4):
        # this logic just for ensuring tendons go high to low
        even = (i_segment % 2) == 0
        if even:
            i = i_segment
            j = i_segment + 1
        else: # odd
            i = i_segment + 1
            j = i_segment

        x0 = x_coords[i]
        x1 = x_coords[j]
        y = 8
        tendon_segment = longitude_tendon_layer.add_tendon_segment(LineSegment2D(Point2D(x0,y),Point2D(x1,y)))
        tendon_segment.elevation_value_1 = profiles[i]
        tendon_segment.elevation_value_2 = profiles[j]

    # jack
    jack = longitude_tendon_layer.add_jack(Point2D(0.1,8))

    # TOP LONGITUDE TENDONS
    default_tendon_segment.strand_count = 10
    profiles = [0.3, 0.04, .360, 0.04, 0.3]  # profile values for the profile points

    for i_segment in range(0,4):
        # this logic just for ensuring tendons go high to low
        even = (i_segment % 2) == 0
        if even:
            i = i_segment
            j = i_segment + 1
        else: # odd
            i = i_segment + 1
            j = i_segment

        x0 = x_coords[i]
        x1 = x_coords[j]
        y = 15.75
        tendon_segment = longitude_tendon_layer.add_tendon_segment(LineSegment2D(Point2D(x0,y),Point2D(x1,y)))
        tendon_segment.elevation_value_1 = profiles[i]
        tendon_segment.elevation_value_2 = profiles[j]

    # jack
    jack = longitude_tendon_layer.add_jack(Point2D(0.1,15.75))

    # UNIFORM "LATITUDE" TENDONS
    latitude_tendon_layer = cad_manager.tendon_layer(SpanSet.LATITUDE, GeneratedBy.USER)
    y_coords = [0.1, 4, 8, 12, 16 - 0.1]  # y-coordinates for the profile points
    profiles = [0.1, 0.04, .160, 0.04, 0.3]  # profile values for the profile points

    default_tendon_segment.strand_count = 3

    # loop over tendons
    x = 0.5
    while x < 16:
        # loop over tendon segments
        for i_segment in range(0,4):
            # this logic just for ensuring tendons go high to low
            even = (i_segment % 2) == 0
            if even:
                i = i_segment
                j = i_segment + 1
            else: # odd
                i = i_segment + 1
                j = i_segment

            y0 = y_coords[i]
            y1 = y_coords[j]
            tendon_segment = latitude_tendon_layer.add_tendon_segment(LineSegment2D(Point2D(x,y0),Point2D(x,y1)))
            tendon_segment.elevation_value_1 = profiles[i]
            tendon_segment.elevation_value_2 = profiles[j]

        jack = latitude_tendon_layer.add_jack(Point2D(x, 0.1))
        
        # onto next tendon
        x += 1
    
