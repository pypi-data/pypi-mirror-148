from .basics import basicCrossover
from ..populations.basics import basicPopulation
import random

class homologousOnePointCrossover(basicCrossover):

    __slots__ = ('track_split', 'track_xov', 'track_matches', 'homo_thresh',\
                    'window_size')

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        self.track_xov = kargs.get('track_xov', \
                                    self.config.get('track_xov',True,dtype=bool))
        self.track_split = kargs.get('track_split', \
                                        self.config.get('track_split',True,\
                                                            dtype=bool))
        self.track_matches = kargs.get('track_matches',\
                                        self.config.get('track_matches',True,\
                                                            dtype=bool))

        self.window_size = kargs.get('window_size', \
                            self.config.get('window_size', 5, dtype=int, mineq=2))

        self.homo_thresh = kargs.get('homology_threshold', \
                            self.config.get('homology_threshold', type=float,
                                                                    mineq=0,
                                                                    maxeq=1))


    def cross_parents(self, parents=None, children=None, **kargs):
        raise NotImplementedError
        # Get params
        track_split = kargs.get('track_split', self.track_split)
        track_xov = kargs.get('track_xov', self.track_xov)
        track_matches = kargs.get('track_matches', self.track_matches)
        w_size = kargs.get('window_size', self.window_size)
        h_thrsh = kargs.get('homology_threshold', self.homo_thresh)

        # Get chromosomes, don't return copy since we are not editing
        p1c, p2c = parents[0].get_chromo(return_copy=False), \
        parents[1].get_chromo(return_copy=False)


        if random.random() < kargs.get('xov_rate',self.xov_rate):

            p1_start = random.randint(0, len(p1c))

            best_sum, p2_start = 0, None
            for i in range(len(p2c)):
                sum = 0
                for j in range(w_size):
                    if j+i >= len(p2c):
                        break
                    if p1c[p1_start+j] == p2c[i+j]:
                        sum += 1
                if sum > best_sum:
                    best_sum, p2_start = sum, i

            match_frac = best_sum / w_size
            if h_thrsh <= match_frac and \
                    random.random() < max(0, (match_frac-h_thrsh)/(1-h_thrsh)):

                split_pt1 = random.randint(p1_start,\
                                        max(p1_start+w_size, len(p1c)))

                split_pt2 = random.randint(p2_start,
                                        max(p2_start+w_size, len(p2c)))


                # Create chromosomes and inherit information from parents
                children[0].inherit(p1c[:split_pt1]+p2c[split_pt2:],\
                                        parents[0],parents[1])

                children[1].inherit(p2c[:split_pt2]+p1c[split_pt1:],\
                                    parents[0],parents[1])

                if track_matches:
                    children[0].set_attr('homo_match%', match_frac)
                    children[1].set_attr('homo_match%', match_frac)
                if track_xov:
                    children[0].set_attr('xov', True)
                    children[1].set_attr('xov', True)
                if track_split:
                    cnt = [1 for x in split if x]
                    children[0].set_attr('p1%', split_pt1/len(children[0]))
                    children[1].set_attr('p1%', 1-(split_pt2/len(children[1])))

            else: # Otherwise we are directly inheriting
                children[0].inherit(p1c, parent[0])
                children[1].inherit(p2c, parent[1])

                if track_matches:
                    children[0].set_attr('homo_match%', match_frac)
                    children[1].set_attr('homo_match%', match_frac)
                if track_xov:
                    children[0].set_attr('xov', False)
                    children[1].set_attr('xov', False)
                if track_split:
                    children[0].set_attr('p1%', 1)
                    children[1].set_attr('p1%', 0)

        else: # Otherwise we are directly inheriting
            children[0].inherit(p1c, parent[0])
            children[1].inherit(p2c, parent[1])

            if track_xov:
                children[0].set_attr('xov', False)
                children[1].set_attr('xov', False)
            if track_split:
                children[0].set_attr('p1%', 1)
                children[1].set_attr('p1%', 0)
            if track_matches:
                children[0].set_attr('homo_match%', None)
                children[1].set_attr('homo_match%', None)

    def cross_batch(self, parents=None, children=None, **kargs):

        # Get params
        track_split = kargs.get('track_split', self.track_split)
        track_xov = kargs.get('track_xov', self.track_xov)
        track_matches = kargs.get('track_matches', self.track_matches)
        tru_w_size = kargs.get('window_size', self.window_size)
        h_thrsh = kargs.get('homology_threshold', self.homo_thresh)
        xov_rate = kargs.get('xov_rate', self.xov_rate)

        rand_chance, rand_int = random.random, random.randint

        for p1, p2, c1, c2 in zip(parents[::2], parents[1::2], \
                                        children[::2], children[1::2]):
            if rand_chance() < xov_rate:

                p1c, p2c = p1.get_chromo(return_copy=False), \
                                    p2.get_chromo(return_copy=False)

                if len(p1c)-tru_w_size <= 0:
                    w_size = len(p1c)
                else:
                    w_size = tru_w_size
                    p1_start = rand_int(0, len(p1c)-w_size)

                best_sum, p2_start = 0, None
                for i in range(0, len(p2c)-w_size):
                    sum = 0
                    for j in range(w_size):
                        if j+i >= len(p2c):
                            break
                        if p1c[p1_start+j] == p2c[i+j]:
                            sum += 1
                    if sum > best_sum:
                        best_sum, p2_start = sum, i

                match_frac = best_sum / w_size
                if h_thrsh <= match_frac and \
                        rand_chance() < max(0, (match_frac-h_thrsh)/(1-h_thrsh)):

                    split_pt1 = rand_int(p1_start,min(p1_start+w_size, len(p1c)))

                    minlen, maxlen = p1c.get_lenmin(), p1c.get_lenmax()

                    # Determine split_pt2 min and max that will allow both chromosomes
                    #   to remain within bounds
                    split_pt2_min = max(split_pt1+len(p2)-maxlen,\
                                        split_pt1-len(p1)+minlen,\
                                        0, p2_start)
                    split_pt2_max = min(split_pt1+len(p2)-minlen,\
                                        split_pt1-len(p1)+maxlen,\
                                        len(p2), p2_start+w_size)

                    if split_pt2_min < split_pt2_max:
                        split_pt2 = rand_int(split_pt2_min, split_pt2_max)
                        
                        c1.inherit(p1c[:split_pt1]+p2c[split_pt2:], p1, p2)
                        c2.inherit(p2c[:split_pt2]+p1c[split_pt1:], p1, p2)

                        if track_xov:
                            c1.set_attr('xov', True)
                            c2.set_attr('xov', True)
                        if track_split:
                            c1.set_attr('p1%', split_pt1/len(c1))
                            c2.set_attr('p1%', 1-(split_pt2/len(c2)))
                        if track_matches:
                            c1.set_attr('homo_match%', match_frac)
                            c2.set_attr('homo_match%', match_frac)
                    else:
                        c1.inherit(p1.get_chromo(), p1)
                        c2.inherit(p2.get_chromo(), p2)

                        if track_xov:
                            c1.set_attr('xov', False)
                            c2.set_attr('xov', False)
                        if track_split:
                            c1.set_attr('p1%', 1)
                            c2.set_attr('p1%', 0)
                        if track_matches:
                            c1.set_attr('homo_match%', match_frac)
                            c2.set_attr('homo_match%', match_frac)

                else:

                    c1.inherit(p1.get_chromo(), p1)
                    c2.inherit(p2.get_chromo(), p2)

                    if track_xov:
                        c1.set_attr('xov', False)
                        c2.set_attr('xov', False)
                    if track_split:
                        c1.set_attr('p1%', 1)
                        c2.set_attr('p1%', 0)
                    if track_matches:
                        c1.set_attr('homo_match%', match_frac)
                        c2.set_attr('homo_match%', match_frac)
            else:
                c1.inherit(p1.get_chromo(), p1)
                c2.inherit(p2.get_chromo(), p2)

                if track_xov:
                    c1.set_attr('xov', False)
                    c2.set_attr('xov', False)
                if track_split:
                    c1.set_attr('p1%', 1)
                    c2.set_attr('p1%', 0)
                if track_matches:
                    c1.set_attr('homo_match%', None)
                    c2.set_attr('homo_match%', None)
