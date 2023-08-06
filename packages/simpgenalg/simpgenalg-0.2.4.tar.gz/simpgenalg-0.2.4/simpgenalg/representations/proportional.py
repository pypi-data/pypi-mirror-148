from .basics import *
import unittest, random, logging

class proportionalChromo(basicChromo):

    __slots__ = ('n_chars')

    def __init__(self, *args, **kargs):

        super().__init__(*args, **kargs)

        self.n_chars = kargs.get('n_chars', kargs.get('max'))
        if self.n_chars is None:
            self.log.exception('n_chars/max has to be given')

        self.lenLim = kargs.get('lenLim', None)
        if self.lenLim is None:
            if 'len' in kargs:
                self.lenLim = (kargs.get('len'),kargs.get('len'))
            elif 'len' in self.config:
                self.lenLim = (self.config.get('len', dtype=int, mineq=1),\
                               self.config.get('len', dtype=int, mineq=1))
            elif 'lenmin' in kargs and 'lenmax' in kargs:
                self.lenLim = (kargs.get('lenmin'),kargs.get('lenmax'))
            elif 'lenmin' in self.config and 'lenmax' in self.config:
                self.lenLim = (self.config.get('lenmin', dtype=int, mineq=1),\
                               self.config.get('lenmax', dtype=int, mineq=1))
            else:
                self.log.exception('Need to provide lenLim', err=ValueError)

        self.min, self.max, self.dtype = 0, self.n_chars, int

        if 'vals' not in kargs and kargs.get('generate', True):
            self.generate()

    def copy(self):
        return proportionalChromo(vals = self.to_list(return_copy=True),\
                                    lenLim = self.lenLim, \
                                    fit = self.fit, \
                                    hsh = self.hsh, \
                                    n_chars = self.n_chars)

    def __hash__(self):
        if self.hsh is None:
            self.hsh = {(key, item) \
                            for key, item in \
                            self.returnCounter().items()}.__hash__()
        return self.hsh

class proportionalRepresentation(basicRepresentation):

    __slots__ = ('num_genes', 'n_noncoding_chars', 'map_fxn', '_map', 'n_chars')

    def __init__(self, *args, **kargs):

        super().__init__(*args, **kargs)
        # Get number of genes
        self.num_genes = kargs.get('num_genes', None)
        if self.num_genes is None:
            self.num_genes = self.config.get('num_genes',dtype=int, min=0)

        # Get number of noncoding characters
        self.n_noncoding_chars = kargs.get('n_noncoding_chars',None)
        if self.n_noncoding_chars is None:
            self.n_noncoding_chars = \
                        self.config.get('n_noncoding_chars',0,dtype=int,mineq=0)

        # Parameters dependent on mapfxn
        self.map_fxn = kargs.get('map_fxn', None)
        if self.map_fxn is None:
            self.map_fxn = self.config.get('map_fxn', options=(1,2,3,None))

        # Select parameters based off
        if self.map_fxn == 1:
            # Save min / max
            self.n_chars = self.n_noncoding_chars + self.num_genes
            # Get gene min / max (seperate from other two maps as dflt is 0-1)
            self.val_min = kargs.get('val_min',self.config.get('min',0, dtype=(int,float)))
            self.val_max = kargs.get('val_max',self.config.get('max',1, dtype=(int,float)))
            # Verify correct gene min/max
            if self.val_min >= self.val_max:
                self.log.exception('min cannot be >= max', err=ValueError)
            # Set map fxn
            self._map = self.map1
        elif self.map_fxn == 2 or self.map_fxn == 3:
            # Two characters for every gene
            self.n_chars = self.n_noncoding_chars + self.num_genes*2
            # Get gene min / max (No dflt for map1 and 2)
            self.val_min = kargs.get('val_min', None)
            if self.val_min is None:
                self.val_min = self.config.get('min', dtype=(int,float))
            self.val_max = kargs.get('val_max', None)
            if self.val_max is None:
                self.val_max = self.config.get('max', dtype=(int,float))
            # Verify correct gene min/max
            if self.val_min >= self.val_max:
                self.log.exception('min cannot be >= max', err=ValueError)
            # Pick correct map (map1 or map2)
            self._map = self.map2 if self.map_fxn == 2 else self.map3

        if kargs.setdefault('n_chars', self.n_chars) != self.n_chars:
            self.log.exception('Incorrect num characters in kargs', \
                                                                err=ValueError)
        if 'chromo' not in kargs:
            self.chromo = proportionalChromo(*args, **kargs)

    def map1(self, chromo):
        cntr, lst, length, vmin, vmax = chromo.returnCounter(), [],\
             self.__len__(), self.val_min, self.val_max
        for char in range(0, self.n_chars):
            freq = cntr.get(char,0)
            #self.set_attr(f'char_{char}_%', freq/self.__len__())
            lst.append(vmin + (freq / length)*(vmax-vmin))
        return lst

    def map2(self, chromo):
        cntr, lst, vmin, vmax = \
                    chromo.returnCounter(), [], self.val_min, self.val_max
        for char in range(0, self.n_chars, 2):
            pos, neg = cntr.get(char,0), cntr.get(char+1,0)
            #self.set_attr(f'char_{char}_%', pos/self.__len__())
            #self.set_attr(f'char_{char+1}_%', neg/self.__len__())
            lst.append(vmin + (pos/(pos+neg))*(vmax-vmin) \
                            if pos+neg!=0 else 0)
        return lst

    def map3(self, chromo):
        cntr, lst, vmin, vmax = \
                    chromo.returnCounter(), [], self.val_min, self.val_max
        for char in range(0, self.n_chars, 2):
            pos, neg = cntr.get(char,0), cntr.get(char+1,0)
            #self.set_attr(f'char_{char}_pct', pos/self.__len__())
            #self.set_attr(f'char_{char+1}_pct', neg/self.__len__())
            lst.append(vmin + (pos/neg if (pos<neg and neg!=0) \
                                else (neg/pos if pos!=0 else 0))*(vmax-vmin))
        return lst

    def copy(self, copy_ID=False):
        if copy_ID:
            return proportionalRepresentation(\
                                    logger=self.log,\
                                    num_genes=self.num_genes,\
                                    n_noncoding_chars=self.n_noncoding_chars,\
                                    val_min=self.val_min,\
                                    val_max=self.val_max,\
                                    chromo=self.get_chromo(return_copy=True),\
                                    fit=self.get_fit(),\
                                    map_fxn=self.map_fxn,\
                                    attrs=self.get_attrs(return_copy=True),\
                                    ID=self.get_ID())
        return proportionalRepresentation(\
                                logger=self.log,\
                                num_genes=self.num_genes,\
                                n_noncoding_chars=self.n_noncoding_chars,\
                                val_min=self.val_min,\
                                val_max=self.val_max,\
                                chromo=self.get_chromo(return_copy=True),\
                                fit=self.get_fit(),\
                                map_fxn=self.map_fxn,\
                                attrs=self.get_attrs(return_copy=True))
