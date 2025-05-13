#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------


from ram_concept.cad_manager import CadManager
from ram_concept.enums import GeneratedBy
from ram_concept.line_segment_2D import LineSegment2D
from ram_concept.tendon_layer import TendonLayer
from ram_concept.tendon_segment import TendonSegment
from ram_concept.model import Model
from ram_concept.point_2D import Point2D

def get_tendon_profiles(model: Model):
    """Determine the reactions for the 16m x 16m structure """

    # The structure created is a simple 16m x 16m square, with 8m spans:

    #  cbbbbbbbcbbbbbbbc
    #  |               |
    #  |               |
    #  w       c       w
    #  w               w
    #  w               w
    #  wwwwwwwwwwwwwwwww

    cad_manager = model.cad_manager
    
    # get all the tendon_layers
    tendon_layers = cad_manager.tendon_layers

    # we'll report tendons at 10th points
    fractional_locations = [i * 0.1 for i in range(11)]

    # report on all the tendon layers
    for tendon_layer in tendon_layers:
        if tendon_layer.generated_by == GeneratedBy.PROGRAM:
            continue
        
        # report header
        header = tendon_layer.name + "  TENDON SEGMENT POSITIONS"
        print(header)
        print("*" * len(header))
        print(" #    ratio     x       y        z   ")
        print("-------------------------------------")

        tendon_segments = tendon_layer.tendon_segments
        for tendon_segment in tendon_segments:
            number = tendon_segment.number
            location = tendon_segment.location
            elevations = tendon_segment.elevations_along_segment(fractional_locations)
            for index in range(11):
                fraction = fractional_locations[index]
                point_location = location.point_along_segment(fraction)
                elevation = elevations[index]
                print("{0:>3}   {1:4.2f}  {2:7.3g} {3:7.3g} {4:7.3g}".format(number, fraction, point_location.x, point_location.y, elevation))
            print() # space between tendon segments

        # space between tendon layers
        print()
        print()