from .basics import basicCrossover
from ..populations.basics import basicPopulation
import random

class uniformCrossover(basicCrossover):

    __slots__ = ('track_split', 'track_xov')

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        self.track_xov = kargs.get('track_xov', \
                                    self.config.get('track_xov',True,dtype=bool))
        self.track_split = kargs.get('track_split', \
                                        self.config.get('track_split',True,\
                                                            dtype=bool))


    def cross_parents(self, parents=None, children=None, **kargs):

        # Get params
        track_split = kargs.get('track_split', self.track_split)

        # Verify correct input
        if not isinstance(parents, (tuple, list)) or len(parents) != 2:
            self.log.exception('Expected two parents as a tuple or list',\
                                err=TypeError)
        if not isinstance(children, (tuple, list)) or len(children) != 2:
            self.log.exception('Expected two children as a tuple or list',\
                                err=TypeError)

        # Get chromosomes, don't return copy since we are not editing
        p1c, p2c = parents[0].get_chromo(return_copy=False), \
        parents[1].get_chromo(return_copy=False)


        if random.random() < kargs.get('xov_rate',self.xov_rate):

            # Verify chromosomes are same length (fixed len 1pt not var)
            if len(p1) != len(p2):
                self.log.exception('Lengths did not match', err=ValueError)

            # Decide on split point
            split = [random.random()>0.5 for x in range(len(p1c))]



            # Create chromosomes and inherit information from parents
            children[0].inherit([p1c[i] if split[i] else p2c[i]
                                    for i in range(len(p1c))],\
                                    parents[0],parents[1])

            children[1].inherit([p2c[i] if split[i] else p1c[i]
                                    for i in range(len(p1c))],\
                                parents[0],parents[1])

            if track_xov:
                children[0].set_attr('xov', True)
                children[1].set_attr('xov', True)
            if track_split:
                cnt = [1 for x in split if x]
                children[0].set_attr('p1%', sum(cnt)/len(split))
                children[1].set_attr('p1%', 1-(sum(cnt)/len(split)))

        else: # Otherwise we are directly inheriting
            children[0].inherit(p1c, parent[0])
            children[1].inherit(p2c, parent[1])

            if track_xov:
                children[0].set_attr('xov', False)
                children[1].set_attr('xov', False)
            if track_split:
                children[0].set_attr('p1%', 1)
                children[1].set_attr('p1%', 0)

    def cross_batch(self, parents=None, children=None, **kargs):

        # Get params
        track_xov = kargs.get('track_xov', self.track_xov)
        track_split = kargs.get('track_split', self.track_split)

        # Verify correct input
        if not isinstance(parents, (tuple, list, basicPopulation)) or  \
                len(parents) < 2 or len(parents) % 2 != 0:
            self.log.exception('Expected at least one pair of parents as a '+\
                                'tuple, list, or pop obj', err=TypeError)
        if not isinstance(children, (tuple, list, basicPopulation)) or  \
                len(children) < 2 or len(children) % 2 != 0:
            self.log.exception('Expected at least one pair of children as a '+\
                                'tuple, list, or pop obj', err=TypeError)
        if len(children) != len(parents):
            self.log.exception('Should be the same amount of parents'+\
                            f'({len(parents)}) as children({len(children)})',\
                            err=ValueError)

        xov_rate = kargs.get('xov_rate', self.xov_rate)
        rand_chance = random.random
        for p1, p2, c1, c2 in zip(parents[::2], parents[1::2], \
                                        children[::2], children[1::2]):
            if rand_chance() < xov_rate:
                p1c, p2c = parents[0].get_chromo(return_copy=False), \
                           parents[1].get_chromo(return_copy=False)

                if len(p1c) != len(p2c):
                    self.log.exception('Should be the same length', \
                                            err=ValueError)

                # Decide on split point
                split = [random.random()>0.5 for x in range(len(p1c))]

                split_pt = random.randint(0,len(p1c))
                c1.inherit([p1c[i] if split[i] else p2c[i]
                                        for i in range(len(p1c))], p1, p2)
                c2.inherit([p2c[i] if split[i] else p1c[i]
                                        for i in range(len(p1c))], p1, p2)

                if track_xov:
                    c1.set_attr('xov', True)
                    c2.set_attr('xov', True)
                if track_split:
                    cnt = [1 for x in split if x]
                    c1.set_attr('p1%', (sum(cnt)/len(split)))
                    c2.set_attr('p1%', 1-(sum(cnt)/len(split)))

            else:

                c1.inherit(p1.get_chromo(), p1)
                c2.inherit(p2.get_chromo(), p2)

                if track_xov:
                    c1.set_attr('xov', False)
                    c2.set_attr('xov', False)
                if track_split:
                    c1.set_attr('p1%', 1)
                    c2.set_attr('p1%', 0)
