#--------------------------------------------------------------------------------------
#
#  Copyright: (c) 2020 Bentley Systems, Incorporated. All rights reserved. 
#
#--------------------------------------------------------------------------------------

from ram_concept.concept import Concept

concept = Concept.start_concept(headless=True)

response = concept.ping()
print("RAM Concept responded: " + response)

concept.shut_down()

