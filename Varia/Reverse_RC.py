def comp_nuc(nucleotide):

    '''
    Geef de complementaire nucleotide terug
    '''
    nucleotide = nucleotide.upper()
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
    elif nucleotide == "N":
        return "N"
    else:
        return "-"

def complement(sequence):
    '''
    Geef de complementaire sequentie terug
    '''
    complement = ''
    for nucleotide in sequence:
        complement += comp_nuc(nucleotide)
    return complement
def reverseComplement(sequence):
    '''
    Geef de reverse complementaire sequentie terug
    '''
    inverscomplement = ""
    for nucleotide in sequence[::-1]:
        inverscomplement += comp_nuc(nucleotide)
    return inverscomplement
