from .basics import *
from random import choice, randint

class messyChromo(basicChromo):

    messy_template = None

    __slots__ = ()

    def __init__(self, *args, **kargs):

        super().__init__(*args, **kargs)

        self.num_genes = kargs.get('num_genes', None)
        if self.num_genes is None:
            self.num_genes = kargs.get('num_genes',\
                                self.config.get('num_genes', dtype=int, min=1))

        self.gene_size = kargs.get('gene_size', None)
        if self.gene_size is None:
            self.gene_size = kargs.get('gene_size',\
                                self.config.get('gene_size', dtype=int, min=1))

        self.bin_len = self.num_genes*self.gene_size

        self.lenLim = kargs.get('lenLim', None)
        if self.lenLim is None:
            self.lenLim = (self.config.get('len_min', dtype=int, min=0),\
                           self.config.get('len_max', dtype=int, min=0))

        self.dtype = int

        self.template = kargs.get('template', messyChromo.template)

        if 'vals' not in kargs and kargs.get('generate', True):
            self.generate()

    # Returns a copy of this chromosome
    def copy(self):
        return messyChromo(vals = self.to_list(return_copy=True),\
                           lenLim = self.lenLim, \
                           fit = self.fit, \
                           hsh = self.hsh, \
                           num_genes = self.num_genes, \
                           gene_size = self.gene_size, \
                           template = self.template)


    def get_max(self, index):
        if index%2 == 1:
            return 1
        return self.bin_len

    def generate(self):
        self.set_chromo([randint(self.bin_len) \
                            if index%2==1 else \
                            choice((0,1)) \
                            for index in \
                            range(randint(self.lenLim[0],self.lenLim[1]))])

    def get_map(self):
        mapped = [None]*self.bin_len
        for i,v in zip(self.vals[::2],self.vals[1::2]):
            if mapped[i] is None:
                mapped[i] = v
        template = self.template
        return [mapped[i] if mapped[i] is not None else template[i] \
                                for i in range(self.bin_len)]

    def append(self, item):
        self.vals.append(item)

    def extend(self, item):
        self.vals.extend(item)

    def insert(self, index, item):
        self.vals.insert(index, item)

    def pop(self, indx):
        return self.vals.pop(indx)

    # Returns a list of genes
    def get_split(self):
        mapped = self.get_map()
        return [mapped[x:x+self.gene_size] for x in \
                    range(0, self.bin_len, self.gene_size)]
