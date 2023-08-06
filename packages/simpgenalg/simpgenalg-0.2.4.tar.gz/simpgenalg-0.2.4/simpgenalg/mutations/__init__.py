#__name__ = 'simpgenalg.mutations'

from .flipbit import flipbitMutation
from .uniform import uniformRandomMutation
from .gaussian import gaussianMutation
from .swap import swapMutation

mutations_dct = {'flipbit':flipbitMutation,\
                 'uniform_mutation':uniformRandomMutation,\
                 'gaussian_mutation':gaussianMutation,\
                 'swap_mutation':swapMutation}
