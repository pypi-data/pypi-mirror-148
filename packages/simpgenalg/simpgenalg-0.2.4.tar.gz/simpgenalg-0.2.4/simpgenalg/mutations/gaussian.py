from ..representations.basics import basicRepresentation
from .basics import basicMutation
import random

class gaussianMutation(basicMutation):

    __slots__ = ('dtype','generate_value','sigma')

    def __init__(self, *args, **kargs):

        super().__init__(*args, **kargs)

        self.dtype = self.config.get('dtype',int)
        self.sigma = self.config.get('mut_sigma', 1.0, dtype=float, min=0)

        if self.dtype is int:
            self.generate_value = self._generate_int
        elif self.dtype is float:
            self.generate_value = self._generate_float

    def _generate_int(self, val, min, max):
        val = round(random.gauss(val, self.sigma))
        if val < min:
            return min
        elif val > max:
            return max
        return val

    def _generate_float(self, val, min, max):
        val = random.gauss(val, self.sigma)
        if val < min:
            return min
        elif val > max:
            return max
        return val


    def mutate_indx(self, indv, indx=None, mut_rate=None):
        chromo = indv.get_chromo(return_copy=False)
        if random.random() < mut_rate if mut_rate is not None else self.mut_rate:
            indv.incr_attr('num_muts')
            chromo[indx] = self.generate_value(chromo[indx], chromo.get_min(indx),
                                                            chromo.get_max(indx))
        return

    def mutate_chromo(self, indv, mut_rate=None):
        mut_rate = mut_rate if mut_rate is not None else self.mut_rate
        chromo = indv.get_chromo(return_copy=False)
        random_chance = random.random
        num_muts = 0
        for indx, indv in enumerate(chromo.to_list()):
            if random_chance() < mut_rate:
                num_muts += 1
                chromo[indx] = self.generate_value(chromo[indx],
                                                   chromo.get_min(indx),
                                                   chromo.get_max(indx))
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
                    chromo[indx] = self.generate_value(chromo[indx],
                                                       chromo.get_min(indx),
                                                       chromo.get_max(indx))
            indv.set_attr('num_muts',num_muts)


    def _mutate_indx(self, chromo, indx=None):
        indv.get_chromo()[mut_rate] = self.generate_value(chromo[indx],
                                                          chromo.get_min(indx),
                                                          chromo.get_max(indx))
