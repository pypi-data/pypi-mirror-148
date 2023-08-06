from .basics import *
from random import choices

class fixedBinaryChromo(basicChromo):

    __slots__ = ('num_genes', 'gene_size')

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        # Get number of genes
        self.num_genes = kargs.get('num_genes', None)
        if self.num_genes is None:
            self.num_genes = kargs.get('num_genes',\
                                self.config.get('num_genes', dtype=int, min=1))
        # Get gene size
        self.gene_size = kargs.get('gene_size', None)
        if self.gene_size is None:
            self.gene_size = kargs.get('gene_size',\
                                    self.config.get('gene_size', dtype=int, min=1))

        # Determine length
        length = self.num_genes*self.gene_size

        # If passed a lenmin or a lenmax raise errors
        if 'len_min' in kargs or 'len_max' in kargs:
            raise ValueError('Should not include len_min or len_max for '+\
                             'fixedBinaryChromo')

        # Determine length limit
        if self.lenLim is not None:
            if self.lenLim[0] != length and lenLim[1] != length:
                self.log.exception('lenLim should be equal to length')
        else:
            self.lenLim = (length, length)

        # These values are always true
        self.min, self.max, self.dtype = 0, 1, int

        if 'vals' not in kargs and kargs.get('generate', True):
            self.generate()

    # Returns a list of genes
    def get_split(self):
        return [self.vals[x:x+self.gene_size] for x in \
                    range(0, self.num_genes*self.gene_size, self.gene_size)]

    # Returns a copy of this chromosome
    def copy(self):
        return fixedBinaryChromo(vals = self.to_list(return_copy=True),\
                                    lenLim = self.lenLim, \
                                    fit = self.fit, \
                                    hsh = self.hsh, \
                                    num_genes = self.num_genes, \
                                    gene_size = self.gene_size)
    # Generate a chromosome
    def generate(self):
        self.set_chromo(choices((0,1), k=self.lenLim[0]))

    # List of functions we cannot do since fixed bianry size
    def append(self, item):
        self.log.exception('Cannot append to a fixedBinaryChromo',\
                           err=NotImplementedError)
    def extend(self, item):
        self.log.exception('Cannot extend to a fixedBinaryChromo',\
                           err=NotImplementedError)
    def insert(self, index, item):
        self.log.exception('Cannot insert to a fixedBinaryChromo',\
                           err=NotImplementedError)
    def pop(self, indx):
        self.log.exception('Cannot pop from a fixedBinaryChromo',\
                           err=NotImplementedError)

class binaryRepresentation(basicRepresentation):

    __slots__ = ('dtype', 'sign_bit')

    def __init__(self, *args, **kargs):
        super().__init__(*args, **kargs)

        self.dtype = kargs.get('dtype',\
                    self.config.get('dtype', int, options=(int, float, None)))

        if 'chromo' not in kargs:
            self.chromo = fixedBinaryChromo(*args, **kargs)

        # Figure out min/max producable by mapping function
        if self.dtype is int:
            self.sign_bit = self.config.get('sign_bit', True, dtype=bool)

            if self.sign_bit:
                self.val_min = self._cnvrt_to_int([1]*self.chromo.gene_size)
                self.val_max = self._cnvrt_to_int([0]+[1]*(self.chromo.gene_size-1))
            else:
                self.val_min, self.val_max = \
                    0, self._cnvrt_to_int([1]*self.chromo.gene_size)
        elif self.dtype is float:
            self.sign_bit = self.config.get('sign_bit', True, dtype=bool)
            if self.sign_bit:
                self.val_min, self.val_max = -1, 1
            else:
                self.val_min, self.val_max = 0, 1

        elif self.dtype is None:
            self.val_min, self.val_max, self.sign_bit = None, None, None
        else:
            self.log.exception('dtype must be int or float', err=ValueError)

    # Convert a list of 0s and 1s to a float value between 0 and 1
    def _cnvrt_to_float(self, lst):
        if self.sign_bit:
            if lst[0] == 0:
                return sum([1/(2**indx) if x==1 else 0 \
                                            for indx, x in enumerate(lst[1:], start=1)])
            elif lst[0] == 1:
                return -1*sum([1/(2**indx) if x==1 else 0 \
                                            for indx, x in enumerate(lst[1:], start=1)])
            else:
                raise ValueError('Sign_bit must be 0 or 1')
        else:
            return sum([1/(2**indx) if x==1 else 0 \
                            for indx, x in enumerate(lst, start=1)])
    # Convert a list of 0s and 1s to an int value between 0 and length of list
    #   raised to the second power (0 - len(lst)^2)
    def _cnvrt_to_int(self, lst):
        if self.sign_bit:
            if lst[0] == 0:
                return sum([(2**indx) if x==1 else 0 \
                                            for indx, x in enumerate(lst[1::-1], start=1)])
            elif lst[0] == 1:
                return -1*sum([(2**indx) if x==1 else 0 \
                                            for indx, x in enumerate(lst[1::-1], start=1)])
            else:
                raise ValueError('Sign-bit must be 0 or 1')
        else:
            return sum([(2**indx) if x==1 else 0 \
                                    for indx, x in enumerate(lst[::-1], start=1)])
    # Apply mapping function to convert binary values to either float, ints or
    #   just return the list of individual binary values
    def _map(self, chromo):
        if self.dtype is int:
            return [self._cnvrt_to_int(lst) for lst in chromo.get_split()]
        elif self.dtype is float:
            return [self._cnvrt_to_float(lst) for lst in chromo.get_split()]
        elif self.dtype is None:
            return chromo.to_list(return_copy=True)
    # Returns copy of the individual
    def copy(self, copy_ID=False):
        if copy_ID:
            return binaryRepresentation(logger=self.log,\
                                      chromo=self.get_chromo(return_copy=True),\
                                      fit=self.get_fit(),\
                                      attrs=self.get_attrs(return_copy=True),\
                                      ID=self.get_ID(),\
                                      val_min=self.get_valmin(),\
                                      val_max=self.get_valmax(),\
                                      dtype=self.dtype)
        return binaryRepresentation(logger=self.log,\
                                   chromo=self.get_chromo(return_copy=True),\
                                   fit=self.get_fit(),\
                                   attrs=self.get_attrs(return_copy=True),\
                                   val_min=self.get_valmin(),\
                                   val_max=self.get_valmax(),\
                                   dtype=self.dtype)
