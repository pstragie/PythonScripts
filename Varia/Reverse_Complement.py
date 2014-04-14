'''
Created on 2-nov.-2012
Geeft het complement en het reverse complement van een DNA-streng terug
@author: pstragie
'''
#Vraag naar DNA-streng:
invoer = input("nucleotidestreng: ")
invoer = invoer.upper()



def complement(nucleotide):
    '''
    Geef de complementaire nucleotide terug
    '''
    if nucleotide == "G":
        return "C"
    elif nucleotide == "C":
        return "G"
    elif nucleotide == "A":
        return "T"
    elif nucleotide == "T":
        return "A"
    elif nucleotide == "R":
        return "Y"
    elif nucleotide == "Y":
        return "R"
    elif nucleotide == "W":
        return "W"
    elif nucleotide == "S":
        return "S"
    elif nucleotide == "K":
        return "M"
    elif nucleotide == "M":
        return "K"
    elif nucleotide == "B":
        return "V"
    elif nucleotide == "D":
        return "H"
    elif nucleotide == "H":
        return "D"
    elif nucleotide == "V":
        return "B" 
    else:
        return "-"
    
def inversComplement(sequence):
    '''
    Geef de reverse complementaire sequentie terug
    '''
    inverscomplement = ""
    for nucleotide in sequence[::-1]:
        inverscomplement += complement(nucleotide)
    return inverscomplement

def Complementseq(sequence):
    '''
    Geef de complementaire sequentie terug
    '''
    comp = ''
    for nucleotide in sequence:
        comp += complement(nucleotide)
    return comp

print("complement:", Complementseq(invoer))
print("reverse complement:", inversComplement(invoer))
