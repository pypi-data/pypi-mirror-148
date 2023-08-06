from .basics import *
import unittest, random, logging

class fixedVectorChromo(basicChromo):

    __slots__ = ()

    def __init__(self, *args, **kargs):

        super().__init__(self, *args, **kargs)
        if 'len_min' in kargs or 'len_max' in kargs:
            raise ValueError('Should not include len_min or len_max for '+\
                             'fixedVectorChromo')

        # if values are none from basicChromo init than use config
        if self.lenLim is None:
            num_genes = self.config.get('num_genes')
            self.lenLim = (num_genes, num_genes)
        self.dtype = self.dtype if self.dtype is not None else \
                        self.config.get('dtype', options=(int, float))
        self.max = self.max if self.max is not None else \
                        self.config.get('max')
        self.min = self.min if self.min is not None else \
                        self.config.get('min')

        if self.max is not None and self.min is not None:
            if self.max <= self.min:
                self.log.exception('Max cannot be <= min', err=ValueError)

        if 'vals' not in kargs and kargs.get('generate', True):
            self.generate()

    def append(self, item):
        self.log.exception('Cannot append to a fixedVectorChromo',\
                           err=NotImplementedError)

    def extend(self, item):
        self.log.exception('Cannot extend to a fixedVectorChromo',\
                           err=NotImplementedError)

    def insert(self, item):
        self.log.exception('Cannot insert to a fixedVectorChromo',\
                           err=NotImplementedError)

    def pop(self, indx):
        self.log.exception('Cannot pop from a fixedVectorChromo',\
                           err=NotImplementedError)

    # Returns a copy of this chromosome
    def copy(self):
        return fixedVectorChromo(vals = self.to_list(return_copy=True),\
                                    max = self.max,\
                                    min = self.min,\
                                    dtype = self.dtype, \
                                    lenLim = self.lenLim, \
                                    fit = self.fit, \
                                    hsh = self.hsh)

class vectorRepresentation(basicRepresentation):

    __slots__ = ()

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        # If no chromosome provided, generate one
        if 'chromo' not in kargs:
            self.chromo = fixedVectorChromo(*args, **kargs)

        # Figure out the max/min value
        self.val_min = self.config.get('min', \
                                dtype=self.get_chromo(return_copy=False).dtype)
        self.val_max = self.config.get('max', \
                                dtype=self.get_chromo(return_copy=False).dtype)
        if self.val_max <= self.val_min:
            self.log.exception('val_min must be greater than val_max')

    def _map(self, chromo):
        return chromo.to_list(return_copy=True)

    def get_mapped(self, return_copy=True):
        return self.get_chromo(return_copy=False).to_list(return_copy=return_copy)

    def copy(self, copy_ID=False):
        chromo_copy = self.get_chromo(return_copy=True)
        if copy_ID:
            test = vectorRepresentation(logger=self.log,\
                                    chromo=self.get_chromo(return_copy=True),\
                                    fit=self.get_fit(),\
                                    attrs=self.get_attrs(return_copy=True),\
                                    len=self.get_chromo().__len__(),\
                                    ID=self.get_ID(),\
                                    val_min=self.get_valmin(),\
                                    val_max=self.get_valmax())
        test = vectorRepresentation(logger=self.log,\
                                chromo=self.get_chromo(return_copy=True),\
                                fit=self.get_fit(),\
                                attrs=self.get_attrs(return_copy=True),\
                                len=self.get_chromo().__len__(),\
                                val_min=self.get_valmin(),\
                                val_max=self.get_valmax())
        return test


class fixedVectorChromo_unittest(unittest.TestCase):

    def test_AAA_raises_error(self):

        fvc = fixedVectorChromo(len=10, min=0, max=10, dtype=int)
        logging.disable()
        self.assertRaises(NotImplementedError, fvc.append, 1)
        self.assertRaises(NotImplementedError, fvc.extend,[1])
        self.assertRaises(NotImplementedError, fvc.insert,[1])
        self.assertRaises(NotImplementedError, fvc.pop,1)
        logging.disable(logging.NOTSET)

class vectorRepresentation_unittest(unittest.TestCase):

    def make_indv(self):
        return vectorRepresentation(max=10, \
                                    min=0, \
                                    dtype=int,\
                                    len=10)

    def test_AAA_init(self):
        indv = self.make_indv()

    def test_AAB_map(self):
        indv = vectorRepresentation(max=10, \
                                    min=0, \
                                    dtype=int,\
                                    len=10)

        lst = indv.get_chromo().to_list()

        self.assertEqual(lst, indv.get_mapped(), msg='get_mapped failed')
        self.assertEqual(lst, indv._map(indv.get_chromo()), msg='_map failed')

if __name__ == '__main__':
    unittest.main()
