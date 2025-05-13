#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------


from ram_concept.cad_manager import CadManager
from ram_concept.elements import ColumnElement
from ram_concept.elements import WallElementGroup
from ram_concept.element_layer import ElementLayer
from ram_concept.force_loading_layer import ForceLoadingLayer
from ram_concept.line_segment_2D import LineSegment2D
from ram_concept.loading_layer import LoadingCause
from ram_concept.loading_layer import LoadingType
from ram_concept.model import Model
from ram_concept.point_2D import Point2D
from ram_concept.point_3D import Point3D
from ram_concept.result_layers import ReactionContext

def get_reactions(model: Model):
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
    element_layer = cad_manager.element_layer
    
    # get all the loadings
    loadings = cad_manager.force_loading_layers

    # remove the hyperstatic loading
    for loading in loadings:
        if loading.loading_type.cause == LoadingCause.HYPERSTATIC:
            loadings.remove(loading)
            break

    # get all the load combos
    load_combos = cad_manager.load_combo_layers

    # combine the load combo layers and the loading layers, as we want reactions for both
    loadings_and_combos = loadings + load_combos

    # loop through all the loadings and combos and get their reactions
    for loading_or_combo in loadings_and_combos:
        # put a pleasant header
        header = loading_or_combo.name + " REACTIONS"
        print(header)
        print("*" * len(header))
        print()

        # handle column reactions
        print("Column Reactions")
        print("----------------")
        print("    x       y       Fx        Fy        Fz        Mx        My")
        print("------------------------------------------------------------------")
        for column_element in element_layer.column_elements_below:
            reaction = loading_or_combo.column_reaction(column_element, ReactionContext.STANDARD)
            location = column_element.location
            print("{0:7.2f} {1:7.2f} {2:9.2g} {3:9.2g} {4:9.2g} {5:9.2g} {6:9.2g}".format(location.x, location.y, reaction.x, reaction.y, reaction.z, reaction.rot_x, reaction.rot_y))

        # add a blank line between columns and walls
        print()

        # handle wall reactions
        print("Wall Reactions")
        print("--------------")
        print(" name      x       y       z    angle   length   area      Fx        Fy        Fz        Mx        My        Mz")
        print("----------------------------------------------------------------------------------------------------------------")
        for wall_element_group in element_layer.wall_element_groups_below:
            reaction = loading_or_combo.wall_group_reaction(wall_element_group, ReactionContext.STANDARD)
            name = wall_element_group.name
            centroid = wall_element_group.centroid
            angle = wall_element_group.reaction_angle
            length = wall_element_group.total_length
            area = wall_element_group.total_area
            print("{0:5} {1:7.2f} {2:7.2f} {3:7.2f} {4:7.2f} {5:7.2f} {6:7.2f} {7:9.2g} {8:9.2g} {9:9.2g} {10:9.2g} {11:9.2g} {12:9.2g}".format(
                name, centroid.x, centroid.y, centroid.z, angle, length, area, reaction.x, reaction.y, reaction.z, reaction.rot_x, reaction.rot_y, reaction.rot_z))

        # add a couple blank lines between loadings or combos
        print()
        print()
