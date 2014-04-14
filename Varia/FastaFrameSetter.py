'''
Created on 24-jan.-2013
Plaats elke sequentie in reading frame 1 op basis van de correcte aminozuursequentie.
@author: pstragie
'''
# TODO: output list of sequences without match

####### Bestandsnaam invullen ######
#ask for fasta file

#fastabestand = str(input("bestandsnaam: "))
fastabestand = "pseudomonas_dnaA.fasta"
#window = input("window size: ")
window = 7
#### Veranderen indien van toepassing #####
#Dit bestand bevat de codon omzettingstabel
codoncode = 'standaard_code.txt'



######### Script (afblijven) ############
shortname, extension = fastabestand.split(".") # split inputfilename into name and extension
outputfile = shortname + "_inFrame1.fasta" # change name

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

#ask for DNA template in the correct frame
template_DNA = str(input("Geef template DNA in reading frame +1:"))

#translate template to amino acid sequence
code = GenetischeCode(codoncode)
AAtemplate = code.eiwit(template_DNA)
print(AAtemplate)
print("fasta-bestand lezen...")
#use AA sequence as template motif
def motieven(sequentie, subsequentie = AAtemplate, window = window, begin = 0, einde = 500):
    
    a = begin-1
    b = einde 
    for _ in range(0, b-a):
        for j in range(0, len(subsequentie)-window):  
            a = sequentie.find(subsequentie[j:j+window], a+1, b)
            if a >= 0:
                return "yes"


fastafile = open(fastabestand, "r")
#Remove \n from between sequences
file = fastafile
outfile = open('fastaTmp.txt', 'w')
regels = ""
for regel in file:
    if regel.startswith(">"):
        regels += "\n" + regel
    else:
        regels += regel.rstrip()
outfile.write(regels)
file.close()
outfile.close()
    
fastafile = open('fastaTmp.txt', 'r')
fastafile.readline()
#read fasta file line by line
uitvoerbestand = open(outputfile, 'w')
uitvoer2 = open("nomatch.fasta", "w")
counttotal, count1, count2, count3, countmin1, countmin2, countmin3, countnonefound = 0, 0, 0, 0, 0, 0, 0, 0
name_list = []
nomatch_list = []
for seqline in fastafile:
    
    seqline = seqline.rstrip("\n")
    if seqline.startswith(">"):
        print("+1: {:6} +2: {:6} +3: {:6} -1: {:6} -2: {:6} -3: {:6}    Total: {:6}   No matching reading frame: {}\n".format(count1, count2, count3, countmin1, countmin2, countmin3, counttotal, countnonefound))
    
        name_list.append(seqline)
        uitvoerbestand.write(seqline + "\n")
	uitvoer2.write(seqline + "\n")
    else:
        counttotal += 1        
        if motieven(code.eiwit(seqline[:])) == "yes":
            count1 += 1
	    if len(seqline) % 3 == 0:
		x = None
	    elif len(seqline) % 3 == 1:
		x = "-1"
	    elif len(seqline) % 3 == 2:
		x = "-2"
            uitvoerbestand.write(seqline[:x] + "\n")

        elif motieven(code.eiwit(seqline[1:])) == "yes":
            count2 += 1
	    if len(seqline[1:]) % 3 == 0:
		x = None
	    elif len(seqline[1:]) % 3 == 1:
		x = "-1"
	    elif len(seqline[1:]) % 3 == 2:
		x = "-2"
            uitvoerbestand.write(seqline[1:x] + "\n")
        elif motieven(code.eiwit(seqline[2:])) == "yes":
            count3 += 1
	    if len(seqline[2:]) % 3 == 0:
		x = None
	    elif len(seqline[2:]) % 3 == 1:
		x = "-1"
	    elif len(seqline[2:]) % 3 == 2:
		x = "-2"
            uitvoerbestand.write(seqline[2:x] + "\n")
        elif motieven(code.eiwit(reverseComplement(seqline[:]))) == "yes":
            countmin1 += 1
	    if len(seqline[1:]) % 3 == 0:
		x = None
	    elif len(seqline[1:]) % 3 == 1:
		x = "1"
	    elif len(seqline[1:]) % 3 == 2:
		x = "2"
            uitvoerbestand.write(reverseComplement(seqline[x:]) + "\n")
        elif motieven(code.eiwit(reverseComplement(seqline[:-1]))) == "yes":
            countmin2 += 2
            uitvoerbestand.write(reverseComplement(seqline[x:-1]) + "\n")
        elif motieven(code.eiwit(reverseComplement(seqline[:-2]))) == "yes":
            countmin3 += 3
            uitvoerbestand.write(reverseComplement(seqline[x:-2]) + "\n")
        else:
            print("None found")
	    uitvoer2.write(seqline + "\n")
            nameseq = name_list[counttotal-1]
            nomatch_list.append(nameseq)
            countnonefound += 1
uitvoerbestand.close()
uitvoer2.close()
print("Finished! Output written to {}".format(outputfile))
print("No match found in: ", nomatch_list)
