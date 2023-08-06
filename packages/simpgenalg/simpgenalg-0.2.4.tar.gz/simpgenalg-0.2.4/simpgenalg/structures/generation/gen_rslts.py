from ...other import basicComponent
from statistics import mean, stdev, median
from math import sqrt

import sys

try:
    import pandas as pd
except:
    pass

class allResults(basicComponent):

    __slots__ = ('runs', 'maximize', 'best', 'gen_fnd')

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.runs = []
        self.best = None
        self.gen_fnd = None
        self.maximize = kargs.get('maximize', self.config.get('maximize',True,\
                                                    dtype=bool))

    def __getitem__(self, key):
        return self.runs.__getitem__(key)

    def append(self, run):

        if not isinstance(run, runResults):
            self.log.exception('Expected runresults', err=TypeError)

        self.runs.append(run)

        cur_bst = run.get_best()
        if self.best is None:
            self.best = cur_bst.copy()
            self.gen_fnd = run.get_best_fnd_gen()
        elif self.maximize:
            if self.best['fit'] < cur_bst['fit']:
                self.best = cur_bst.copy()
                self.gen_fnd = run.get_best_fnd_gen()
        else:
            if self.best['fit'] > cur_bst['fit']:
                self.best = cur_bst.copy()
                self.gen_fnd = run.get_best_fnd_gen()

    def to_dict(self, *args, **kargs):
        if len(args) == 0:
            pop_dct = {'_run':[]}
            pop_stats_dct = {'_run':[]}
            # Tracks number of entries (so if new variable shows up we stay consist)
            entries = 0
            # Iterate through generations
            for run_num, run in enumerate(self.runs):
                # Add gen number, one per population
                run_dct = run.to_dict()
                # Extend the lists
                for key, lst in run_dct['pop_dct'].items():
                    pop_dct.setdefault(key, [None]*entries).extend(lst)
                for key, item in run_dct['pop_stats'].items():
                    pop_stats_dct.setdefault(key, \
                                [None]*len(pop_stats_dct['_run'])).extend(item)
                # Stores runbest at each generation throughout
                for key, item in self.get_best().items():
                    pop_stats_dct.setdefault(f'{key}.allbest', \
                            [None]*len(pop_stats_dct['_run'])).extend([item]*len(run))
                pop_dct['_run'].extend([run_num]*run.get_num_entries())
                pop_stats_dct['_run'].extend([run_num]*len(run))
                # Add num of generations to number of entries
                entries += len(run)
            return {'pop_dct':pop_dct, 'pop_stats':pop_stats_dct}
        elif len(args) == 1 and isinstance(args[0], (list, tuple)):
                if len(args[0]) == 1 and isinstance(args[0][0], int):
                    return self.__getitem__(args[0][0]).to_dict()
                elif len(args[0]) == 2 and isinstance(args[0][0], int) and \
                                                isinstance(args[0][1], int):
                    return self.__getitem__(args[0][0])\
                                    .__getitem__(args[0][1]).to_dict()
                else:
                    self.log.exception('If passed a tuple should have 1-2 ints')
        elif len(args) == 1 and isinstance(args[0], (int)):
            return self.__getitem__(args[0]).to_dict()
        elif len(args) == 2 and isinstance(args[0], (int)) and isinstance(args[1], (int)):
            return self.__getitem__(args[0]).__getitem__(args[1]).to_dict()

    def to_df(self):
        if 'pandas' not in sys.modules:
            self.log.exception('Pandas needs to be installed to get dataframe',\
                                    err=ModuleNotFoundError)
        dct = self.to_dict()
        return pd.DataFrame(dct['pop_dct']), pd.DataFrame(dct['pop_stats'])

    def get_best(self):
        return self.best

    def get_best_fnd_gen(self):
        return self.gen_fnd


class runResults(basicComponent):

    __slots__ = ('gens', 'entries', 'maximize', 'best', 'gen_fnd')

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.gens = []
        self.entries = 0

        self.maximize = kargs.get('maximize', \
                    self.config.get('maximize',True, dtype=bool))

        self.best = None
        self.gen_fnd = None

    def __getitem__(self, key):
        return self.gens.__getitem__(key)

    def append(self, *args, **kargs):
        if len(args) == 1:
            if not isinstance(gen, genResults):
                self.log.exception('Can only append genResults to runResults',\
                                    err=TypeError)
            self.gens.append(gen)
        elif 'pop_dct' in kargs:
            self.gens.append(genResults(config=self.config,\
                                        log=self.log,\
                                        toolbox=self.toolbox,\
                                        pop_dct=kargs.get('pop_dct')))
        else:
            self.log.exception('Must either pass a genResults or the pop_stats'+\
                                ' and indv_attrs as kargs', err=TypeError)
        self.entries += self.gens[-1].get_size()

        cur_bst = self.gens[-1].get_best()

        if self.best is None:
            self.best = self.gens[-1].get_best()
            self.gen_fnd = len(self.gens)-1
        elif self.maximize:
            if self.best['fit'] < cur_bst['fit']:
                self.best = cur_bst.copy()
                self.gen_fnd = len(self.gens)-1
        else:
            if self.best['fit'] > cur_bst['fit']:
                self.best = cur_bst.copy()
                self.gen_fnd = len(self.gens)-1


    def to_dict(self, **kargs):
        pop_dct, pop_stats = {'_gen':[]}, {'_gen':[]}
        # Tracks number of entries (so if new variable shows up we stay consist)
        entries = 0
        # Iterate through generations
        for gen_num, gen in enumerate(self.gens):
            gen_dct = gen.to_dict()
            # Extend the lists
            for key, lst in gen_dct['pop_dct'].items():
                pop_dct.setdefault(key, [None]*entries).extend(lst)
            # Appends the lists
            for key, item in gen_dct['pop_stats'].items():
                pop_stats.setdefault(key, [None]*len(pop_stats['_gen'])).append(item)
            # Stores runbest at each generation throughout
            for key, item in self.get_best().items():
                pop_stats.setdefault(f'{key}.runbest', \
                                    [None]*len(pop_stats['_gen'])).append(item)

            # Add gen number, one per population
            pop_dct['_gen'].extend([gen_num]*gen.get_size())
            pop_stats['_gen'].append(gen_num)

            # Add pop size to number of entries
            entries += gen.get_size()

        return {'pop_dct':pop_dct, 'pop_stats':pop_stats}


    def to_df(self):
        if 'pandas' not in sys.modules:
            self.log.exception('Pandas needs to be installed to get dataframe',\
                                    err=ModuleNotFoundError)
        dct = self.to_dict()
        return pd.DataFrame(dct['pop_dct']), pd.DataFrame(dct['pop_stats'])

    def get_num_gens(self):
        return len(self.gens)

    def __len__(self):
        return len(self.gens)

    def get_num_entries(self):
        return self.entries

    def get_best(self):
        return self.best

    def get_best_fnd_gen(self):
        return self.gen_fnd

class genResults(basicComponent):

    __slots__ = ('pop_dct', 'pop_stat_dct', 'size', 'best', 'maximize')

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.pop_dct = kargs.get('pop_dct', None)
        self.pop_stat_dct = kargs.get('pop_stat_dct', {})

        # Verify all lengths are the same
        length = None
        for key, lst in self.pop_dct.items():
            if length is None:
                length = len(lst)
            elif len(lst) != length:
                self.log.exception(f'Inconsistent lengths ({key}):\n' + \
                    '\n'.join([f'{key}:{len(lst)}' \
                            for key, lst in self.pop_dct.items()]),\
                    err=ValueError)

        self.size = length
        self.maximize = kargs.get('maximize', \
                    self.config.get('maximize',True, dtype=bool))

        self.best = {}

        if self.maximize:
            bst_indx = self.pop_dct['fit'].index(max(self.pop_dct['fit']))
        else:
            bst_indx = self.pop_dct['fit'].index(min(self.pop_dct['fit']))

        for key, lst in self.pop_dct.items():
            self.best[key] = lst[bst_indx]

    # Calculate statistics based off the pop dictionary
    def calc_stats(self, *args, incl_corrs=False, corr_type='pearson', **kargs):

        # Dictionary of stats
        stats = {}

        # If none, just go through all
        if len(args) == 0:
            args = self.pop_dct.keys()

        # Iterate through the keys provided and turn it into stats
        for key in args:

            # Get the list
            lst = self.pop_dct.get(key)
            # Remove any Nones
            if None in lst:
                lst = [val for val in lst if val is not None]

            # Skip if not an integer, float, or bool
            if isinstance(lst[0], (bool)):
                lst = [1 if item else 0 for item in lst]
            elif not isinstance(lst[0], (int, float)):
                continue


            try: # Find the mean
                stats[f'{key}.mean'] = mean(lst)
            except:
                stats[f'{key}.mean'] = None

            try: # Find the median
                stats[f'{key}.median'] = median(lst)
            except:
                stats[f'{key}.median'] = None


            try: # Find the standard deviation
                stats[f'{key}.stdev'] = stdev(lst)
            except:
                stats[f'{key}.stdev'] = None

            try: # Returns count of item
                stats[f'{key}.count'] = len(lst)
            except:
                stats[f'{key}.count'] = None

            try: # Find the 95 CI
                stats[f'{key}.95CI'] = \
                    1.96*(stats[f'{key}.stdev'] / sqrt(stats[f'{key}.count']))
                stats[f'{key}.95CI_upper'] = \
                    stats[f'{key}.mean']+stats[f'{key}.95CI']
                stats[f'{key}.95CI_lower'] = \
                    stats[f'{key}.mean']-stats[f'{key}.95CI']
            except:
                stats[f'{key}.95CI'] = None
                stats[f'{key}.95CI_upper'] = None
                stats[f'{key}.95CI_lower'] = None

            try: # Find the minimum of the lst
                stats[f'{key}.min'] = min(lst)
            except:
                stats[f'{key}.min'] = None

            try: # Find the maximum of the lst
                stats[f'{key}.max'] = max(lst)
            except:
                stats[f'{key}.max'] = None

            try: # Find the range of the lst
                stats[f'{key}.range'] = \
                    stats[f'{key}.max'] - stats[f'{key}.min']
            except:
                stats[f'{key}.range'] = None

        for key, item in self.get_best().items():
            try:
                stats[f'{key}.genbest'] = item
            except:
                stats[f'{key}.genbest'] = None

        # Adds correlation data if requested
        if incl_corrs:
            stats.update(self.calc_corr(flatten=True, corr_type=corr_type))

        self.pop_stat_dct.update(stats)

        return self.pop_stat_dct

    # Generates a list of strings
    def get_gen_strs(self, *args, **kargs):
        rnd = kargs.get('round', 3)
        # If passed a gen, will add gen number to it
        stats = self.calc_stats()
        return '\t'.join([f'{key}:{round(item,rnd)}' \
                                for key,item in self.calc_stats().items() \
                                if key in args])

    def to_dict(self):
        return {'pop_dct':self.pop_dct.copy(), 'pop_stats':self.pop_stat_dct.copy()}

    def to_df(self):
        if 'pandas' not in sys.modules:
            self.log.exception('Pandas needs to be installed to get dataframe',\
                                    err=ModuleNotFoundError)
        return pd.DataFrame(self.pop_dct), pd.DataFrame(self.pop_stat_dct)

    def __getitem__(self, key):
        return self.pop_dct.__getitem__(key)

    def get_size(self):
        return self.size

    def get_best(self):
        return self.best
