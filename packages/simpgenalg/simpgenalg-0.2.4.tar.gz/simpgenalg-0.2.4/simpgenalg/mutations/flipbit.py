from ..representations.basics import basicRepresentation
from .basics import basicMutation
import random

class flipbitMutation(basicMutation):

    __slots__ = ()

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def mutate_indx(self, indv, indx=None, mut_rate=None):
        chromo = indv.get_chromo(return_copy=False)
        if random.random() < mut_rate if mut_rate is not None else self.mut_rate:
            indv.incr_attr('num_muts')
            if chromo[indx] == 1:
                indv.incr_attr('downflip')
                chromo[indx] = 0
            elif chromo[indx] == 0:
                indv.incr_attr('upflip')
                chromo[indx] = 1
            else:
                self.log.exception(f'flipbitMutation received {chromo[indx]} '+\
                                    'instead of 0 or 1', err=ValueError)

    def mutate_chromo(self, indv, mut_rate=None):
        mut_rate = mut_rate if mut_rate is not None else self.mut_rate
        num_mut, upflips, downflips = 0,0,0
        chromo = indv.get_chromo(return_copy=False)
        random_chance = random.random
        for indx, val in enumerate(chromo.to_list()):
            if random_chance() < mut_rate:
                num_mut += 1
                if val == 1:
                    downflips += 1
                    chromo[indx] = 0
                elif val == 0:
                    upflips += 1
                    chromo[indx] = 1
                else:
                    self.log.exception(f'flipbitMutation received {val} '+\
                                        'instead of 0 or 1', err=ValueError)
        indv.set_attr('num_muts', num_mut)
        indv.set_attr('downflips', downflips)
        indv.set_attr('upflips', upflips)
