#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

# WALKTHROUGH EXAMPLE
# THIS SAMPLE SHOWS WALKS THROUGH ALL THE PARTS OF THE API.

# RAM Concept developers (working in dev setup) need to find the (non-installed) API using a path relative to this file location.
import os
if(os.environ.get("RAM_CONCEPT_DEVELOPER") != None):
    # this claptrap is just to reference code in a non-path, non-child directory.
    import sys
    dev_api_directory = os.path.dirname(os.path.realpath(__file__)) + '\\..\\..'
    sys.path.insert(1, dev_api_directory) # must insert at 1; 0 is the script path (or '' in REPL)

# Python Imports
from pathlib import Path

# RAM Concept API imports
from ram_concept.concept import Concept
from ram_concept.model import DesignCode
from ram_concept.model import Model
from ram_concept.model import StructureType

# Walkthrough imports
from add_loads import add_loads
from add_materials import add_materials
from add_pt import add_pt
from add_structure import add_structure
from get_reactions import get_reactions
from get_tendon_profiles import get_tendon_profiles

user_directory = str(Path.home())
file_path = os.path.join(user_directory, "Walkthrough.cpt")

# STARTUP RAM CONCEPT AND CREATE A FILE

# The first thing to do is always to start a RAM Concept process to act as a server.
# In production, you will normally want to use a headless server, but for debugging you might want to run RAM Concept with a GUI.
concept = Concept.start_concept(headless=True)
#concept = Concept.start_concept(headless=False)

# You'll either want to open a file or create a new one.
model = concept.new_model()
#model = concept.open_file(file_path)

# If this is a new file/model, you will want to initialize it for the desired code, structure type and unit system.
# The bare-bones file/model created by new_model() is extremely minimal (almost useless)
model.setup_new_model(DesignCode.ACI318_14SI, StructureType.ELEVATED)

# SETUP / SAVE UNITS AND SIGNS

# Set the units to something appropriate for the user (if this was an existing file you would assume the units are ok)
units = model.units
units.set_SI_user_units()

# Save the units, as you are about to change them and want to restore them before saving the file
saved_units = units.get_units() 

# Set the units to something predictable for the API (the API uses the same units as the UI)
units.set_SI_API_units() # meters, degrees, Newtons, kilograms, seconds, Celsius

# Set the signs to something appropriate for the user (if this was an existing file you would assume the units are ok)
signs = model.signs
signs.set_standard_signs()

# Save the signs, as you are about to change them and want to restore them before saving the file
saved_signs = signs.get_signs()

# Set the signs to somethign predictable for the API (the API uses the same units as the UI)
signs.set_positive_signs()

# XXXXXXXXXXXX INTERESTING WORK STARTS HERE XXXXXXXXXXXXXXXX

# The structure created is a simple 16m x 16m square, with 8m spans:

#  cbbbbbbbcbbbbbbbc
#  |               |
#  |               |
#  w       c       w
#  w               w
#  w               w
#  wwwwwwwwwwwwwwwww

add_materials(model)
add_structure(model)
add_loads(model)
add_pt(model)

model.calc_all()

get_reactions(model)
get_tendon_profiles(model)

# XXXXXXXXXXXX INTERESTING WORK ENDS HERE XXXXXXXXXXXXXXXX

# RESTORE THE UNITS AND SIGNS

# restore the units to the initial user-friendly units
units.set_units(saved_units)

# restore the signs to the initial user-friendly signs
signs.set_signs(saved_signs)

# SAVE THE FILE

model.save_file(file_path)

# SHUT DOWN RAM CONCEPT

concept.shut_down()

