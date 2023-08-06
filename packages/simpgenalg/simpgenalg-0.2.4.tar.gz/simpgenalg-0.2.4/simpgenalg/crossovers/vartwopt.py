from .basics import basicCrossover
from ..populations.basics import basicPopulation
import random

class variableTwoPointCrossover(basicCrossover):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        self.track_xov = kargs.get('track_xov', \
                                    self.config.get('track_xov',True,dtype=bool))

        self.track_split_pt = kargs.get('track_split_pt', \
                                        self.config.get('track_split_pt',True,\
                                                            dtype=bool))


    def cross_parents(self, parents=None, children=None, **kargs):

        # Get params
        track_xov = kargs.get('track_xov', self.track_xov)
        track_split_pt = kargs.get('track_split_pt', self.track_split_pt)

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
            # Decide on initial split points
            pt1A = random.randint(0, len(p1))
            pt2A = random.randint(0, len(p2))

            # Select two that would still make it valid length
            lenrng1, lenrng2 = p1c.get_lenrange(), p2c.get_lenrange()
            pt1B = random.randint(max(0,len(p1)-lenrng1),\
                                            min(len(p1),pt1A+lenrng1))
            pt2B = random.randint(max(0,len(p2)-lenrng2),\
                                            min(len(p2),pt2A+lenrng2))

            if pt1A > pt1B:
                pt1A, pt1B = pt1B, pt1A
            if pt2A > pt2B:
                pt2A, pt2B = pt2B, pt2A

            children[0].inherit(p1c[:pt1A] + p2c[pt2A:pt2B] + p1c[pt1B:], \
                                    parents[0], parents[1])
            children[1].inherit(p2c[:pt2A] + p1c[pt1A:pt1B] + p2c[pt2B:], \
                                    parents[0], parents[1])

            if track_xov:
                children[0].set_attr('xov', True)
                children[1].set_attr('xov', True)
            if track_split_pt:
                children[0].set_attr('p1_pct', pt1A+(len(children[0])-pt1B))
                children[0].set_attr('p2_pct', pt2B-pt2A)
                children[1].set_attr('p1_pct', pt2A+(len(children[0])-pt2B))
                children[1].set_attr('p2_pct', pt1B-pt1A)

        else: # Otherwise we are directly inheriting
            children[0].inherit(p1c, parent[0])
            children[1].inherit(p2c, parent[1])

            if track_xov:
                children[0].set_attr('xov', False)
                children[1].set_attr('xov', False)
            if track_split_pt:
                children[0].set_attr('p1_pct', 1)
                children[0].set_attr('p2_pct', 0)
                children[1].set_attr('p1_pct', 0)
                children[1].set_attr('p2_pct', 1)

    def cross_batch(self, parents=None, children=None, **kargs):

        # Get params
        track_xov = kargs.get('track_xov', self.track_xov)
        track_split_pt = kargs.get('track_split_pt', self.track_split_pt)

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

                # Decide on initial split points
                pt1A = random.randint(0, len(p1))
                pt2A = random.randint(0, len(p2))

                # Select two that would still make it valid length
                lenrng1, lenrng2 = p1c.get_lenrange(), p2c.get_lenrange()
                pt1B = random.randint(max(0,len(p1)-lenrng1),\
                                                min(len(p1),pt1A+lenrng1))
                pt2B = random.randint(max(0,len(p2)-lenrng2),\
                                                min(len(p2),pt2A+lenrng2))

                if pt1A > pt1B:
                    pt1A, pt1B = pt1B, pt1A
                if pt2A > pt2B:
                    pt2A, pt2B = pt2B, pt2A

                print(pt1A, pt1B)
                print(len(p1c[:pt1A] + p2c[pt2A:pt2B] + p1c[pt1B:]))
                print(len(p2c[:pt2A] + p1c[pt1A:pt1B] + p2c[pt2B:]))
                c1.inherit(p1c[:pt1A] + p2c[pt2A:pt2B] + p1c[pt1B:], p1, p2)
                c2.inherit(p2c[:pt2A] + p1c[pt1A:pt1B] + p2c[pt2B:], p1, p2)


                if track_xov:
                    c1.set_attr('xov', True)
                    c2.set_attr('xov', True)
                if track_split_pt:
                    c1.set_attr('p1_pct', pt1A+(len(children[0])-pt1B))
                    c1.set_attr('p2_pct', pt2B-pt2A)
                    c2.set_attr('p1_pct', pt2A+(len(children[0])-pt2B))
                    c2.set_attr('p2_pct', pt1B-pt1A)

            else:

                c1.inherit(p1.get_chromo(), p1)
                c2.inherit(p2.get_chromo(), p2)

                if track_xov:
                    c1.set_attr('xov', False)
                    c2.set_attr('xov', False)
                if track_split_pt:
                    c1.set_attr('p1_pct', 1)
                    c1.set_attr('p2_pct', 0)
                    c2.set_attr('p1_pct', 0)
                    c2.set_attr('p2_pct', 1)
