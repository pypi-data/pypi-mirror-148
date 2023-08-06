from .basics import *
import math, random
from statistics import mean, stdev

class floatingBinaryChromo(basicChromo):

    def __init__(self, *args, **kargs):

        super().__init__(self, *args, **kargs)

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

        self.min, self.max, self.dtype = 0, 1, int

        if 'vals' not in kargs and kargs.get('generate', True):
            self.generate()

        def copy(self):
            return floatingBinaryChromo(vals = self.to_list(return_copy=True),\
                                        lenLim = self.lenLim, \
                                        fit = self.fit, \
                                        hsh = self.hsh)

class floatingRepresentation(basicRepresentation):

    __slots__ = ('template', 'gene_id_len', 'gene_ids','gene_size', 'num_genes',\
                    'start_tag', 'end_tag', 'dtype', 'sign_bit')

    # Variables needed to be accessed by all floating individuals
    cls_start_tag, cls_end_tag, cls_gene_ids, cls_gene_id_len, cls_template = \
        None, None, None, None, None

    def __init__(self, *args, **kargs):

        super().__init__(*args, **kargs)
        # Get number of genes
        self.num_genes = kargs.get('num_genes', None)
        if self.num_genes is None:
            self.num_genes = self.config.get('num_genes')

        # Get gene size
        self.gene_size = kargs.get('gene_size',None)
        if self.gene_size is None:
            self.gene_size = self.config.get('gene_size', dtype=int, mineq=1)

        # Get dtype
        self.dtype = kargs.get('dtype',None)
        if self.dtype is None:
            self.dtype = self.config.get('dtype', options=(int, float, None))
            if self.dtype is not None:
                self.sign_bit = self.config.get('sign_bit', False)

        # Determine value min / max
        if self.dtype is int:
            self.val_min, self.val_max = 0, self._cnvrt_to_int([1]*self.gene_size)
        elif self.dtype is float:
            self.val_min, self.val_max = 0, 1
        elif self.dtype is None:
            self.val_min, self.val_max = None, None
        else:
            self.log.exception('Expected dtype to be int, float, or None')


        # Extract class variables (unless given something else)
        self.start_tag = kargs.get('start_tag', \
                                        floatingRepresentation.cls_start_tag)
        self.end_tag = kargs.get('end_tag', \
                                        floatingRepresentation.cls_end_tag)
        self.gene_ids = kargs.get('gene_ids', \
                                        floatingRepresentation.cls_gene_ids)
        self.gene_id_len = kargs.get('gene_id_len', \
                                        floatingRepresentation.cls_gene_id_len)
        self.template = kargs.get('template', \
                                        floatingRepresentation.cls_template)

        # Handle missing variables by generating for whole class
        if self.start_tag is None:
            if 'start_tag' in self.config:
                self.start_tag = self.config.get('start_tag', dtype=list)
                floatingRepresentation.cls_start_tag = self.start_tag
            else:
                if 'start_tag_len' in kargs:
                    length = kargs.get('start_tag_len')
                else:
                    length = self.config.get('start_tag_len',3,dtype=int,mineq=1)
                self.start_tag = \
                    floatingRepresentation.generate_start_tag(length=length, \
                                                              return_vals=True)

        # Handle missing end tag
        if self.end_tag is None and self.config.get('use_end_tag', True, dtype=bool):
            if 'end_tag' in self.config:
                self.end_tag = self.config.get('end_tag', dtype=list)
                floatingRepresentation.cls_end_tag = self.end_tag
            else:
                if 'end_tag_len' in kargs:
                    length = kargs.get('end_tag_len')
                else:
                    length = self.config.get('end_tag_len',3,dtype=int,mineq=1)
                self.end_tag = \
                    floatingRepresentation.generate_end_tag(length=length, \
                                                            return_vals=True)

        # Handle missing gene ids
        if self.gene_ids is None:
            if self.gene_id_len is None and 'gene_id_len' in self.config:
                self.gene_id_len = self.config.get('gene_id_len', None, \
                                                        dtype=int, mineq=1)
            self.gene_ids, self.gene_id_len = \
                                floatingRepresentation.generate_gene_ids(\
                                                    num_genes=self.num_genes,\
                                                    length=self.gene_id_len,\
                                                    return_vals=True)
        # If missing gene_id_len (would occur if given gene ids but not length)
        #   go through and verify length
        if self.gene_id_len is None:
            length = None
            for key in self.gene_ids.keys():
                if isinstance(key, tuple):
                    if length is None:
                        length = len(key)
                    elif length != len(key):
                        raise ValueError('Inconsistent Gene Id Length')
            self.gene_id_len, floatingRepresentation.cls_gene_id_len = \
                                                                length, length

        # If no template, then use all zeros
        if self.template is None:
            self.template = [0]*self.num_genes
            floatingRepresentation.cls_template = self.template

        # Generate chromosome if not given one
        if 'chromo' not in kargs:
            self.chromo = floatingBinaryChromo(*args, **kargs)

    def copy(self, copy_ID=False):
        if copy_ID:
            return floatingRepresentation(logger=self.log,\
                                          chromo=self.get_chromo(return_copy=True),\
                                          fit=self.get_fit(),\
                                          attrs=self.get_attrs(return_copy=True),\
                                          ID=self.get_ID(),\
                                          val_min=self.get_valmin(),\
                                          val_max=self.get_valmax(),\
                                          dtype=self.dtype)
        return floatingRepresentation(logger=self.log,\
                                      chromo=self.get_chromo(return_copy=True),\
                                      fit=self.get_fit(),\
                                      attrs=self.get_attrs(return_copy=True),\
                                      val_min=self.get_valmin(),\
                                      val_max=self.get_valmax(),\
                                      dtype=self.dtype)
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

    def _map(self, chromo):

        # Create map lst and lbls
        map, lbls, extractions = [None]*self.num_genes, \
                                 [set() for x in range(len(chromo))], \
                                 {key:list() for key in range(0, self.num_genes)}
        # Get start tag info and gene info
        strt, strt0, strt_len, gene_id_len, gene_size, chr_len = \
                        self.start_tag, self.start_tag[0], len(self.start_tag),\
                        self.gene_id_len, self.gene_size, len(chromo)
        tot_len = strt_len + gene_id_len + gene_size


        stats = dict.fromkeys(('n_starts', 'n_bad_starts', 'n_ends',\
                    'n_encoded_genes', 'n_unique_encoded_genes',\
                    'meaningful_bits', 'meaningful_bits_pct',\
                    'gene_len_avg', 'gene_len_stdev',
                    'meaningful_bit_overlap_avg'), 0)

        # Find end tags
        if self.end_tag is not None:
            # Get end tag info
            end, end0, end_len = self.end_tag, self.end_tag[0], len(self.end_tag)
            # Enumerate through and find all end tags
            for indx, b in enumerate(chromo):
                # If cannot fit an end tag, end it
                if indx+end_len > chr_len:
                    break
                if b == end0 and end == chromo[indx:indx+end_len]:
                    stats['n_ends'] += 1
                    for lbl in lbls[indx:indx+end_len]:
                        lbl.add('E')

        # Enumerate through binary values
        for indx, b in enumerate(chromo):
            # If cannot fit a start tag, end it
            if indx+strt_len > chr_len:
                break
            # If at start of a start tag, extract it
            if b == strt0 and strt == chromo[indx:indx+strt_len]:
                stats['n_starts'] += 1
                for i in range(indx, indx+strt_len):
                    lbls[i].add('S')

                # If can fit gene ID too, get the ID
                if indx+strt_len+gene_id_len < chr_len:
                    gID = self.gene_ids.get(tuple(chromo[indx+strt_len:\
                                                   indx+strt_len+gene_id_len]),
                                                   None)
                    if gID is None:
                        stats['n_bad_starts'] += 1
                        continue
                    for lbl in lbls[indx+strt_len:indx+strt_len+gene_id_len]:
                        lbl.add('ID')
                else:
                    stats['n_bad_starts'] += 1
                    continue

                # Record extraction
                gene = []
                for cur_indx in range(indx+strt_len+gene_id_len, \
                                            min(chr_len, indx+tot_len)):
                    if 'E' in lbls[cur_indx]:
                        break

                    lbls[cur_indx].add(gID)
                    gene.append(chromo[cur_indx])
                if len(gene) > 0:
                    extractions[gID].append(gene)
                    stats['n_encoded_genes'] += 1

        # Find gene values through averaging
        gene_len_sum = 0

        # Conversion function if int or float
        if self.dtype is int:
            cnvrt = self._cnvrt_to_int
        elif self.dtype is float:
            cnvrt = self._cnvrt_to_float

        # Go through extracted genes and average them (unless dtype is none)
        for gene_num, genes in extractions.items():
            # If no genes found skip
            if len(genes) == 0:
                continue
            stats['n_unique_encoded_genes'] += 1
            # Find average after conerting to int/float
            if self.dtype is not None:
                map[gene_num] = mean([cnvrt(lst) for lst in genes])
            else: #Unless it is none, then we will just return list of each
                map[gene_num] = genes

        # Get some final stats
        #   Average gene length of extracted genes
        glens = [len(gene_lst) for gene_lst in extractions.values()]
        #   Get how many labels assigned to each bit
        bit_use = [len(lbl) for lbl in lbls]
        #   Get number of bit uses
        num_bits_used = sum([1 if uses > 0 else 0 for uses in bit_use])
        # If at least one bit is used, find the mean overlap for those
        if any([bit!=0 for bit in bit_use]+[False]):
            bit_overlap = mean([use for use in bit_use if use!=0])
        # Update the stats dictionary to contain all this info
        stats.update({'gene_len_avg':mean(glens),\
                      'gene_len_stdev':stdev(glens),\
                      'meaningful_bits':num_bits_used,\
                      'meaningful_bits_pct':num_bits_used/len(chromo),\
                      'meaningful_bit_overlap_avg':bit_overlap,\
                      'pct_template':\
                            1-(stats['n_unique_encoded_genes']/self.num_genes)})
        # Replace missing values with the template
        map = [chrval if chrval is not None else tempval \
                    for chrval, tempval in zip(map, self.template)]
        # Return the mapped value and the stats
        return map, stats

    # Returns chromosome mapped
    def get_mapped(self, return_copy=True):
        if self.mapped is None or \
                            self.get_chromo(return_copy=False).get_fit() is None:
            self.mapped, mapstats = self._map(self.get_chromo())
            self.update_attrs(mapstats)
        if return_copy:
            return self.mapped.copy()
        return self.mapped

    ''' Functions for generating gene ids, tags, templates, etc '''

    # Generate a start tag for the class to use
    @classmethod
    def generate_start_tag(cls, length=3, **kargs):
        # Generate a tag
        tag = random.choices((0,1), k = length)

        end_tag = kargs.get('end_tag', cls.cls_end_tag)

        # If end tag is there, make sure it does not equal that
        if end_tag is not None:
            # If length is 1, just invert and return
            if length == 1:
                tag[0] = (tag[0] + 1)%2
                return tag
            # Keep iterating if still equals end tag
            while(tag == end_tag):
                tag = random.choices((0,1))

        if kargs.get('set_for_class', True):
            cls.cls_start_tag = tag
        if kargs.get('return_vals', False):
            return tag

    # Generate an end tag for the class to use
    @classmethod
    def generate_end_tag(cls, length=3, **kargs):
        # Generate a tag
        tag = random.choices((0,1), k = length)

        start_tag = kargs.get('start_tag', cls.cls_start_tag)

        # If end tag is there, make sure it does not equal that
        if kargs.get('start_tag',start_tag) is not None:
            # If length is 1, just invert and return
            if length == 1:
                tag[0] = (tag[0] + 1)%2
                return tag
            # Keep iterating if still equals end tag
            while(tag == start_tag):
                tag = random.choices((0,1))
        if kargs.get('set_for_class', True):
            cls.cls_end_tag = tag
        if kargs.get('return_vals', False):
            return tag

    @classmethod
    def set_template(cls, template=None):
        if template is None:
            raise Exception('')

    # Generate gene ids
    @classmethod
    def generate_gene_ids(cls, num_genes=None, length=None, **kargs):
        # Verify we have the number of genes
        if num_genes is None:
            raise Exception('Need num_genes to generate an ID dict')
        start_tag = kargs.get('start_tag', cls.cls_start_tag)
        end_tag = kargs.get('end_tag', cls.cls_end_tag)
        # Get the minimum length
        min_length = math.log2(num_genes)
        # Either set to min length or make sure at least min length
        if length is None:
            length = min_length
        elif length < min_length:
            raise Exception('Given length is too small')
        # If start tag or end tag is the same length, increment so our start
        #   tag and end tag are not the same as a gene id
        if start_tag is not None and len(start_tag) == length:
            length += 1
        if end_tag is not None and len(end_tag) == length:
            length += 1

        # Apply ceiling function so we have an integer length
        length = math.ceil(length)

        # Function for generating ids
        def genbin(lst, length):
            if len(lst) == 0:
                lst = [[0], [1]]
            elif len(lst[0]) >= length:
                return lst
            newlst = []
            for sublst in lst:
                newlst.append(sublst.copy()+[0])
                newlst.append(sublst.copy()+[1])
            return genbin(newlst, length)

        # Generate all possible IDs of that length then shuffle them
        ids = genbin([], length)
        random.shuffle(ids)

        # Grab enough IDs for the num_genes, make sure not equal to start/end tag
        ids = [id for id in ids if id != start_tag and id != end_tag]\
                    [:num_genes]
        # Place the tuple of the IDs and the ints of the IDs in the dct
        dct = {}
        for gene_num, id in enumerate(ids):
            dct[gene_num] = tuple(id)
            dct[dct[gene_num]] = gene_num

        if kargs.get('set_for_class',True):
            cls.cls_gene_ids, cls.cls_gene_id_len = dct, length
        if kargs.get('return_vals',False):
            return dct, length
