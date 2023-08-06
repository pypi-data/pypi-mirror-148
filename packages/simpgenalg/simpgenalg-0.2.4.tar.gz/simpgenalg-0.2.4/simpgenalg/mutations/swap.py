from ..representations.basics import basicRepresentation
from .basics import basicMutation
import random

class swapMutation(basicMutation):

    __slots__ = ()

    def __init__(self, *args, **kargs):

        super().__init__(*args, **kargs)

    def mutate_indx(self, indv, indx=None, mut_rate=None):
        chromo = indv.get_chromo(return_copy=False)
        if random.random() < mut_rate if mut_rate is not None else self.mut_rate:
            indv.incr_attr('num_muts')
            if random.random() < 0.5 and indx+1 != len(chromo):
                chromo[indx], chromo[indx+1] = chromo[indx+1], chromo[indx]
            elif indx != 0:
                chromo[indx], chromo[indx-1] = chromo[indx-1], chromo[indx]
            else:
                if len(chromo) == 1:
                    return
        return

    def mutate_chromo(self, indv, mut_rate=None):
        mut_rate = mut_rate if mut_rate is not None else self.mut_rate
        chromo = indv.get_chromo(return_copy=False)
        random_chance = random.random
        num_muts = 0
        for indx, indv in enumerate(chromo.to_list()):
            if random_chance() < mut_rate:
                num_muts += 1
                if random.random() < 0.5 and indx+1 != len(chromo):
                    chromo[indx], chromo[indx+1] = chromo[indx+1], chromo[indx]
                elif indx != 0:
                    chromo[indx], chromo[indx-1] = chromo[indx-1], chromo[indx]
                else:
                    if len(chromo) == 1:
                        return
        indv.set_attr('num_muts',num_muts)

    def mutate_batch(self, btch, **kargs):
        mut_rate = kargs.get('mut_rate',self.mut_rate)
        random_chance = random.random

        for indv in btch:
            chromo = indv.get_chromo(return_copy=False)
            num_muts = 0
            for indx in range(len(chromo)):
                if random_chance() < mut_rate:
                    num_muts += 1
                    if random.random() < 0.5 and indx+1 != len(chromo):
                        chromo[indx], chromo[indx+1] = chromo[indx+1], chromo[indx]
                    elif indx != 0:
                        chromo[indx], chromo[indx-1] = chromo[indx-1], chromo[indx]
                    else:
                        if len(chromo) == 1:
                            return
            indv.set_attr('num_muts',num_muts)
