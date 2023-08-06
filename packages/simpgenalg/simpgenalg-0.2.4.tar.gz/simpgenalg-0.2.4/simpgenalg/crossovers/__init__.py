#__name__ = 'simpgenalg.crossovers'

from .onept import onePointCrossover
from .twopt import twoPointCrossover
from .vartwopt import variableTwoPointCrossover
from .uniform import uniformCrossover
from .homoonept import homologousOnePointCrossover

crossovers_dct = {'onept':onePointCrossover,\
                  'twopt':twoPointCrossover,\
                  'vartwopt':variableTwoPointCrossover,\
                  'uniform_crossover':uniformCrossover,\
                  'homologous_onept':homologousOnePointCrossover}
