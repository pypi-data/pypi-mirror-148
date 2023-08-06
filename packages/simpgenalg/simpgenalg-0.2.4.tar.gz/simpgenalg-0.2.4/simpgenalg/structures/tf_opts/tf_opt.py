from ..basics import basicStructure
from ...other import basicComponent

class tfOptStructure(basicStructure):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

    def run(self, **kargs):

        n_runs = kargs.get('n_runs')
        if n_runs is None:
            n_runs = self.config.get('n_runs', 50, dtype=int, mineq=1)

        # Figure out what variables we are tracking and printing
        tracking_vars = kargs.get('tracking_vars')
        if tracking_vars is None:
            tracking_vars = self.config.get('tracking_vars',\
                                ('fit.max', 'fit.min', 'fit.mean','fit.stdev'))
        if isinstance(tracking_vars, str): # If just single str, turn into tuple
            tracking_vars = (tracking_vars)

        self.log.info(f'Starting tfOptStructure for {n_runs} runs')

        
