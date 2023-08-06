class Tree:
    def __new__(cls, item, l=None, r=None, *args, **kwargs):
        if type(item) is Tree:
            return item
        else:
            return super(Tree, cls).__new__(cls, *args, **kwargs)
        
    def __init__(self, item, l=None, r=None):
        #print(f'creating tree from item {item}, left {l}, and right {r}') #debug
        
        if type(item) is dict and l is None and r is None:
            self.value = list(item.keys())[0]
            #print(f'self value is {self.value}') #debug
            sub = list(item.values())[0]
            
            if sub is None:
                self.l = None
                self.r = None
                
            else:
                keys = list(sub.keys())
                values = list(sub.values())
                #print(f'sub is {sub}, keys are {keys}, values are {values}') #debug
                
                self.l = Tree({
                    str(keys[0]): values[0]
                })
                #print(f'self.l is {self.l}') #debug

                self.r = Tree({
                    str(keys[1]): values[1]
                })
                #print(f'self.r is {self.r}') #debug
            
        else:
            self.value = item
            self.l = Tree(l)
            self.r = Tree(r)

    def __repr__(self):
        return self.value

    @property
    def max_depth(self):
        if self.l is not None:
            lDepth = self.l.max_depth
        else:
            lDepth = -1

        if self.r is not None:
            rDepth = self.r.max_depth
        else:
            rDepth = -1

        if lDepth > rDepth:
            return lDepth + 1
        else:
            return rDepth + 1

    @property
    def min_depth(self):
        if self.l is not None:
            lDepth = self.l.min_depth
        else:
            lDepth = -1

        if self.r is not None:
            rDepth = self.r.min_depth
        else:
            rDepth = -1

        if lDepth < rDepth:
            return lDepth + 1
        else:
            return rDepth + 1

    def __getitem__(self, index):
        if index == 0:
            return self.value
            
        elif type(index) is str:
            current = self
            for direction in index:
                #print(f'current is {self}') #debug
                if direction == '<':
                    current = current.l
                elif direction == '>':
                    current = current.r
    
                if current is None:
                    raise IndexError('tree index out of depth')
    
            return current.value

        else:
            raise KeyError(str(index))