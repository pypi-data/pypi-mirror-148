from .basics import basicEvaluator

class functionEvaluator(basicEvaluator):

    __slots__ = ('function', 'send_list')

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)
        self.log.info('Initializing functionEvaluator')
        # Get evaluation function
        self.function = self.config.get('function', callable=True)
        self.send_list = self.config.get('send_list',True, dtype=bool)

    def __del__(self):
        self.function = None
        super().__del__()

    def evaluate(self, indv, **kargs):

        # Try reading the cache
        fit = self.get_cache(tuple(indv.get_mapped()))

        # If fit is none, apply to function
        if fit is None:
            # send list or indv depending on confing
            if self.send_list:
                fit = self.function(indv.get_mapped())
            else:
                fit = self.function(indv)
            # Save in cache
            self.set_cache(tuple(indv.get_mapped()), fit)
        # Set fitness in individual
        indv.set_fit(fit)
        # Replace the current tracked best if so
        self._replace_if_best(indv)
        return

    def evaluate_batch(self, btch, **kargs):
        for indv in btch:
            self.evaluate(indv)
