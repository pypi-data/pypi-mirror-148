from ...other import basicComponent
from statistics import mean, stdev, median

import sys
try:
    from scipy.stats import pearsonr, spearmanr, kendalltau
except:
    pass

class allResults(basicComponent):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.runs = []

    def append_run(self, run):
        self.runs.append(run)

    def combine_runs(self, incl_corr=False):
        dct = {}
        for run_num, run_stats in [run.to_dict(incl_corr=incl_corr) for run \
                                                                  in self.runs]:
            length = None
            for key, val in run_stats.items():
                dct.setdefault(key, [None]*gen_num).extend(val)
                if length is None:
                    length = len(dct[key])
                else:
                    if length != len(dct[key]):
                        self.log.exception('Lengths did not match')

            dct['_run'].extend([run_num]*length)

class runResults(basicComponent):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.gens = []

    def __getitem__(self, key):
        return self.gens.__getitem__(key)

    def append(self, *args, **kargs):
        if len(args) == 1:
            if not isinstance(gen, genResults):
                self.log.exception('Can only append genResults to runResults',\
                                    err=TypeError)
            self.gens.append(gen)
        elif 'pop_stats' in kargs and 'indv_attrs' in kargs:
            self.gens.append(genResults(config=self.config,\
                                        log=self.log,\
                                        toolbox=self.toolbox,\
                                        indv_attrs=kargs.get('indv_attrs'),\
                                        pop_stats=kargs.get('pop_stats')))
        else:
            self.log.exception('Must either pass a genResults or the pop_stats'+\
                                ' and indv_attrs as kargs', err=TypeError)

    def to_dict(self, incl_corrs=False):
        dct = {'_gen':[]}

        gen_dcts = [gen.calc_stats(incl_corrs=incl_corrs) for gen in self.gens]

        for gen_num, gen_stats in enumerate(gen_dcts):
            dct['_gen'].append(gen_num)
            for key, val in gen_stats.items():
                dct.setdefault(key, [None]*gen_num).append(val)


    def to_df(self):
        return pd.DataFrame(self.to_dict())

    def get_gen_corr_over_run(self):
        dct = {}
        for gen_num, corr_stats in enumerate(\
                            [gen.calc_corr(flatten=True) for gen in self.gens]):
            dct['_gen'].append(gen_num)
            for key, val in corr_stats.items():
                dct.setdefault(key, [None]*gen_num).append(val)

    # Calculates correlations of aggregated gen vals
    def calc_corr(self):
        # Raise error if no scipy (since we get the corr fxns from them)
        if 'scipy' not in sys.modules:
            self.log.exception('Cannot perform correlations w/o scipy',\
                                    err=ModuleNotFoundError)

        # Gets aggregated stats as corr
        agg_stats = self.to_dict()

        # Get things we want to find correlations from
        if len(args) == 0:
            args = agg_stats.keys()

        # Determine correlation type
        corr_type = kargs.get('corr_type', 'pearson')
        corr_fxn = None
        if corr_type == 'pearson':
            corr_fxn = pearsronr
        elif corr_type == 'spearman':
            corr_fxn = spearmanr
        elif corr_type == 'kendalltau':
            corr_fxn = kendalltau
        else:
            self.log.exception('corr_type must be pearson, spearman, or '+\
                                    'kendalltau', err=ValueError)

        # Calculate the correlation between different variables
        if kargs.get('flatten', False): # If flattened, returns one layer dict
            corr_dct = {}
            for keyA in args:
                for keyB in args:
                    corr_dct[f'{keyA}.{keyB}'] = corr_fxn(agg_stats[keyA],\
                                                          agg_stats[keyB])
            return corr_dct
        else: # Otherwise first key points to a dict of all its related corrs
            corr_dct = {}
            for keyA in args:
                for keyB in args:
                    corr_dct.setdefault(keyA, {})[keyB] = corr_fxn(\
                                                            agg_stats[keyA],\
                                                            agg_stats[keyB])
            return corr_dct


class genResults(basicComponent):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.pop_dct = kargs.get('pop_dct', None)

    # Calculate statistics based off the pop dictionary
    def calc_stats(self, *args, incl_corrs=False, corr_type='pearson'):
        # Dictionary of stats
        stats = {}

        # If none, just go through all
        if len(args) == 0:
            args = self.pop_dct.keys()

        # Iterate through the keys provided and turn it into stats
        for key in args:

            # Get the list
            lst = self.pop_dct.get(key)

            # Skip if not an integer, float, or bool
            if isinstance(lst[0], (bool)):
                lst = [int(item) for item in lst]
            elif not isinstance(lst[0], (int, float)):
                continue

            try: # Find the mean
                stats[f'{key}.mean'] = mean(lst)
            except:
                pass

            try: # Find the median
                stats[f'{key}.median'] = median(lst)
            except:
                pass

            try: # Find the standard deviation
                stats[f'{key}.stdev'] = stdev(lst)
            except:
                pass

            try: # Find the minimum of the lst
                stats[f'{key}.min'] = min(lst)
            except:
                pass

            try: # Find the maximum of the lst
                stats[f'{key}.max'] = max(lst)
            except:
                pass

            try: # Find the range of the lst
                stats[f'{key}.range'] = \
                    stats[f'{key}.max'] - stats[f'{key}.min']
            except:
                pass

        # Adds correlation data if requested
        if incl_corrs:
            stats.update(self.calc_corr(flatten=True, corr_type=corr_type))

        return stats

    # Calculate correlations based off the pop dictionary
    def calc_corr(self, *args, **kargs):
        # Raise error if no scipy (since we get the corr fxns from them)
        if 'scipy' not in sys.modules:
            self.log.exception('Cannot perform correlations w/o scipy',\
                                    err=ModuleNotFoundError)

        # Get things we want to find correlations from
        if len(args) == 0:
            args = self.pop_dct.keys()

        # Determine correlation type
        corr_type = kargs.get('corr_type', 'pearson')
        corr_fxn = None
        if corr_type == 'pearson':
            corr_fxn = pearsronr
        elif corr_type == 'spearman':
            corr_fxn = spearmanr
        elif corr_type == 'kendalltau':
            corr_fxn = kendalltau
        else:
            self.log.exception('corr_type must be pearson, spearman, or '+\
                                    'kendalltau', err=ValueError)

        # Calculate the correlation between different variables
        if kargs.get('flatten', False): # If flattened, returns one layer dict
            corr_dct = {}
            for keyA in args:
                for keyB in args:
                    corr_dct[f'{keyA}.{keyB}'] = corr_fxn(self.pop_dct[keyA],\
                                                          self.pop_dct[keyB])
            return corr_dct
        else: # Otherwise first key points to a dict of all its related corrs
            corr_dct = {}
            for keyA in args:
                for keyB in args:
                    corr_dct.setdefault(keyA, {})[keyB] = corr_fxn(\
                                                            self.pop_dct[keyA],\
                                                            self.pop_dct[keyB])
            return corr_dct



    def to_df(self):
        return pd.DataFrame(self.pop_dct)

    # Generates a list of strings
    def get_gen_strs(self, *args, **kargs):
        rnd = kargs.get('round', 3)
        # If passed a gen, will add gen number to it
        if 'gen' in kargs:
            gen = kargs.get('gen')
            return f'Gen {gen}:' + '\t'.join([f'{key}:{round(item,rnd)}' \
                                    for key,item in calc_stats(*args).items()])
        return '\t'.join([f'{key}:{round(item,rnd)}' \
                                for key,item in calc_stats(*args).items()])
