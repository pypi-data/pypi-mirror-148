from .gen_rslts import allResults, runResults, genResults
from .op_app import operatorApplicator
from ..basics import basicStructure
from ...selectors.basics import basicSelector
from ...other import basicComponent

class generationStructure(basicStructure):

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        self.log.debug('Initializing generationStructure')


    # Runs this generation structure
    def run(self, **kargs):

        # Creating an object to contain all results gathered from all runs
        all_results = allResults(log=self.log,\
                                config=self.config,\
                                toolbox=self.toolbox)

        # Basic parameters
        n_runs = kargs.get('n_runs',kargs.get('n', \
                                self.config.get('n_runs',1,dtype=int, mineq=1)))
        n_gens = self.config.get('n_gens',200,dtype=int,mineq=1)
        cmpr_map_dist = self.config.get('cmpr_map_dist', False, dtype=bool)

        # Figure out what variables we are tracking and printing
        tracking_vars = self.config.get('tracking_vars',\
                                ('fit.max', 'fit.min', 'fit.mean','fit.stdev'))
        if isinstance(tracking_vars, str): # If just single str, turn into tuple
            tracking_vars = (tracking_vars)

        self.log.info(f'Starting generationStructure for {n_runs} runs')

        # Get selectors / evaluators / populations
        selector, evaluator, parents, children = self._setup_components()

        # Genetic Operators
        operator_applicator = operatorApplicator(log=self.log,\
                                                 toolbox=self.toolbox,\
                                                 config=self.config)

        # Clears those objects
        def clear():
            self.log.debug('Clearing the selector, evaluator, and populations')
            selector.clear(), evaluator.clear(), parents.clear(), children.clear()
            return

        # Iterate through number of runs
        for run in range(n_runs):
            self.log.info(f'Starting run #{run+1}/{n_runs}')

            # Creates object to store resutls for the current run
            run_results = runResults(log=self.log,\
                                     config=self.config,\
                                     toolbox=self.toolbox)

            # Generate the parent population
            self.log.info('Initializing first population')
            parents.generate()
            children.generate()

            # Iterate through generations
            for gen in range(0, n_gens):

                # Evaluate the parents
                evaluator.evaluate_batch(parents)

                # Check for similarity (if enabled)
                if cmpr_map_dist:
                    parents.compare_mapped_distance()

                # Select parents to reproduce
                selected = selector.select(parents)

                # Store current results
                run_results.append(pop_dct=parents.pop_to_dict_of_lists(),\
                                        pop_stat_dct=parents.get_popstats(\
                                                        return_copy=True,\
                                                        compile_indv_attrs=False))
                self.log.info(f'Gen:{gen+1}   ' + \
                        run_results[-1].get_gen_strs(*tracking_vars,round=2))

                # Crete next generation (if not last generation)
                if gen != n_gens:
                    # Create new batch using selected parents and children
                    operator_applicator.apply_operators(selected,children)

                    # Swap the children and parents
                    parents, children = children, parents

            # Adds last runs' results
            all_results.append(run_results)

            # Clear objects for restart
            clear()

        self.log.info('Completed run, returning results')

        del selector
        del evaluator
        del parents
        del children

        return all_results


    def _setup_components(self):
        # Convert
        def convert(val, *args, **kargs):
            if isinstance(val, str):
                return self.toolbox[val](log=self.log,\
                                         config=self.config,\
                                         toolbox=self.toolbox)
            else:
                return val(*args, log=self.log,\
                           config=self.config,\
                           toolbox=self.toolbox,\
                           **kargs)

        evaluator = convert(self.config.get('evaluator','custom'))
        selector = convert(self.config.get('selector','tournament'))
        parents = convert(self.config.get('population','fixed'), \
                                        generate=False)
        children = convert(self.config.get('population','fixed'), \
                                        generate=False)

        return selector, evaluator, parents, children
