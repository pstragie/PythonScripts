'''
Created on 4-dec.-2013

@author: pstragie
'''
import itertools
class IncExc:
    '''
    Count unique members of multiple lists based on the inclusion-exclusion principle
    
    >>> I = IncExc()
    >>> I.toevoegen({1, 2, 3, 4, 5})
    >>> I.calculate()
    5
    >>> I.toevoegen({4, 5, 6, 7, 8})
    >>> print(I)
    [{1, 2, 3, 4, 5}, {8, 4, 5, 6, 7}]
    >>> I.calculate()
    8
    >>> I.toevoegen({2, 7, 8})
    >>> I.calculate()
    8
    >>> I.toevoegen({8, 7, 1, 2})
    >>> I.calculate()
    8
    '''
    def __init__(self):
        self.L = []
    
    def __str__(self):
        return str(self.L) 
    
    def __repr__(self):
        return str(self.L)    
        
    def toevoegen(self, setje):
        self.L.append(setje)
    
    def calculate(self):
        #list all possible combinations
        totalecombolijst = []
        for i in range(2, len(self.L)+1):
            totalecombolijst.extend(list(itertools.combinations(self.L, i)))
        
        teller = 0
        #add the lengths of the individual list
        for J in self.L:
            teller += len(J)
        
        #add or subtract the lengths of the intersections of the combinations
        for s in totalecombolijst:
            for i in s:
                X = 0
                b = i.intersection(*s)
                
                X += len(b)
                z = len(s) % 2  # + or - based on length lists in combo
            teller += ((-1)**(z-1)) * X  # shortened version of the inclusion-exclusion formula
            
        return int(teller)
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()