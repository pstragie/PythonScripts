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
    elif nucleotide == "N":
        return "N"
    else:
        return "-"
    
def reverseComplement(sequence):
    '''
    Geef de reverse complementaire sequentie terug
    '''
    inverscomplement = ""
    for nucleotide in sequence[::-1]:
        inverscomplement += complement(nucleotide)
    return inverscomplement

def ambigue(codon):
    """Ambigue codons omzetten indien mogelijk"""
    amb_lijst = ['W', 'S', 'R', 'Y', 'K', 'M', 'B', 'D', 'H', 'V', 'N']
    AA1 = ""
    AA2 = ""
    AA3 = ""
    AA4 = ""
    for i in codon:
        if i in ["A", "G", "C", "T"]:
            AA1 += i
            AA2 += i
            AA3 += i
            AA4 += i
        elif i == "W":
            AA1 += "A"
            AA2 += "T"
            AA3 += "A"
            AA4 += "T"
        elif i == "S":
            AA1 += "G"
            AA2 += "C"
            AA3 += "G"
            AA4 += "C"
        elif i == "R":
            AA1 += "A"
            AA2 += "G"
            AA3 += "A"
            AA4 += "G"
        elif i == "Y":
            AA1 += "C"
            AA2 += "T"
            AA3 += "C"
            AA4 += "T"
        elif i == "K":
            AA1 += "G"
            AA2 += "T"
            AA3 += "G"
            AA4 += "T"
        elif i == "M":
            AA1 += "A"
            AA2 += "C"
            AA3 += "A"
            AA4 += "C"
        elif i == "B":
            AA1 += "C"
            AA2 += "G"
            AA3 += "T"
            AA4 += "C"
        elif i == "D":
            AA1 += "A"
            AA2 += "G"
            AA3 += "T"
            AA4 += "A"
        elif i == "H":
            AA1 += "A"
            AA2 += "C"
            AA3 += "T"
            AA4 += "A"
        elif i == "V":
            AA1 += "A"
            AA2 += "C"
            AA3 += "G"
            AA4 += "A"
        elif i == "N":
            AA1 += "A"
            AA2 += "C"
            AA3 += "G"
            AA4 += "T"
    return [AA1, AA2, AA3, AA4]
class GenetischeCode:
    '''Genetische code'''
    
    def __init__(self, bestand):
        self.codon_file = bestand
        codons = open(self.codon_file, 'r')
        codon_dict = {}
        for regel in codons:
            code = regel.split()
            codon_dict[code[0].upper()] = code[1]
            RNA_streng = ''
            for i in code[0]:
                if i == "T" or i == "t":
                    RNA_streng += 'U'
                elif i == 'U' or i == 'u':
                    RNA_streng += 'T'
                else:
                    RNA_streng += i.upper()
            codon_dict[RNA_streng.upper()] = code[1]
                    
        self.code = codon_dict    
    def aminozuur(self, codon):
        assert(codon.upper() in self.code), "'%s' is geen geldig codon." % (codon)
        return self.code[codon.upper()]
    
    def eiwit(self, streng):
        alfabet = "ACTUGWSRYKMBDHVN"
        result = ""
        for i in streng:
            assert(i.upper() in alfabet), "ongeldige DNA- of RNA-sequentie."
        L = len(streng)
        if L % 3 == 0:
            streng = streng.upper()
        elif L % 3 == 1:
            streng = streng[:-1].upper()
        else:
            streng = streng[:-2].upper()
        for i in range(0, len(streng), 3):
            if not streng[i:i+3].upper() in self.code.keys():
                AA = ambigue(streng[i:i+3])
                if len(AA) == 2:
                    if self.code[AA[0]] == self.code[AA[1]]:
                        eiwit = self.code[AA[0]]
                        result += eiwit
                    else:
                        result += "?"
                elif len(AA) == 3:
                    if self.code[AA[0]] == self.code[AA[1]] == self.code[AA[2]]:
                        eiwit = self.code[AA[0]]
                        result += eiwit
                    else:
                        result += "?"
                elif len(AA) == 4:
                    if self.code[AA[0]] == self.code[AA[1]] == self.code[AA[2]] == self.code[AA[3]]:
                        eiwit = self.code[AA[0]]
                        result += eiwit
                    else:
                        result += "?"
                else:
                    result += "?"
            else:
                eiwit = self.code[streng[i:i+3].upper()]
                result += eiwit
        
        return result

codontabel = str(input("standard code? yes/no "))
if codontabel == "yes" or codontabel == "y":
    code = GenetischeCode("standaard_code.txt")
else:
    codoncode = str(input("file with code?: "))
    if codoncode == "":
        print("standard code is used.")
        codoncode = "standaard_code.txt"
    code = GenetischeCode(codoncode)
invoer = str(input("DNA or RNA sequence: "))
RF_list = ["1", "2", "3", "all", "-1", "-2", "-3"]
RF = str(input("Reading frame? 1/2/3/all/-1/-2/-3: "))
while not RF in RF_list:
    print("wrong reading frame")
    RF = str(input("Reading frame? 1/2/3/all/-1/-2/-3: "))
if RF == "1" or RF == "2" or RF == "3":
    print(code.eiwit(invoer[int(RF)-1:]))
elif RF == "all":
    print("+1 {}".format(code.eiwit(invoer.upper())))
    print("+2 {}".format(code.eiwit(invoer[1:].upper())))
    print("+3 {}".format(code.eiwit(invoer[2:].upper())))
    print("-1 {}".format(code.eiwit(reverseComplement(invoer.upper()))))
    print("-2 {}".format(code.eiwit(reverseComplement(invoer.upper())[1:])))
    print("-3 {}".format(code.eiwit(reverseComplement(invoer.upper())[2:])))
else:
    print("script not ready")
    RF = str(input("Reading frame? 1/2/3/all/-1/-2/-3: "))