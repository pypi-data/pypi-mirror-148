#__name__ = 'simpgenalg.representations'

from .vector import vectorRepresentation
from .binary import binaryRepresentation
from .proportional import proportionalRepresentation
from .floating import floatingRepresentation

representations_dct = {'vector':vectorRepresentation,\
                       'binary':binaryRepresentation,\
                       'proportional':proportionalRepresentation,\
                       'floating':floatingRepresentation}
