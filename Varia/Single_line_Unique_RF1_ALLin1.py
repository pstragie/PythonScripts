'''
Created on 5-Feb.-2013

@author: pstragie

leest een fasta-bestand en verwijdert end-of-lines tussen de sequenties.
'''
invoer = str(input("bestandsnaam: "))
#bestandsnaam extraheren
naam, ext = invoer.split(".")
#Bestandsnamen aanpassen
file = open(invoer, 'r')
uitvoer = naam + "_clean.fasta"
outfile = open(uitvoer, 'w')

#Script (afblijven)
regels = ""
for regel in file:
    if regel.startswith(">"):
        regels += "\n" + regel
    else:
        regels += regel.rstrip()
outfile.write(regels.lstrip("\n"))
print("Done. Output written in {}".format(uitvoer))
outfile.close()
file.close()
next = str(input("Filter unique names/sequences? y/n: "))

if next == "y":
    fastabestand = uitvoer


    #bestandsnaam extraheren
    naam, ext = fastabestand.split(".")
    #bestand openen
    infl = open(fastabestand, 'r')

    filter = str(input("filter on name ('N') or sequences ('S')? "))
    if filter == "S" or filter == "sequence":

	#uitvoerbestand bepalen
	unique_uit = naam + "_unique_sequences.fasta"
	outflfas = open(unique_uit, 'w')

	#Invoerbestand filteren op unieke sequenties
	print("Unieke sequenties filteren...")

	seq_dict = {}

	for lijn in infl:
	    if lijn.startswith(">"):
		name = lijn
	
	    else:
		if lijn in seq_dict.keys():
		    pass
		else:
		    seq_dict[lijn] = name
	    
		    outflfas.write(name)
		    outflfas.write(lijn)
	print("{} sequenties in bestand".format(len(seq_dict)))
	infl.close()
	outflfas.close()

    elif filter == "N" or filter == "name":

	#uitvoerbestand bepalen
	unique_uit = naam + "_unique_names.fasta"
	outflfas = open(unique_uit, 'w')

	#Invoerbestand filteren op unieke namen
	print("Unieke namen filteren...")

	seq_dict = {}

	for lijn in infl:
	    if lijn.startswith(">"):
		if lijn in seq_dict.keys():
		    pass
		    out = 1
		else:
		    seq_dict[lijn] = lijn
		    outflfas.write(lijn)
		    out = 0
	    else:
		if out == 1:
		    pass
		else:
		    outflfas.write(lijn)	    

	print("{} sequenties in bestand".format(len(seq_dict)))
	infl.close()
	outflfas.close()

    next2 = str(input("Put all sequences in reading frame 1? y/n: "))
    if next2 == "y":
	
	fastabestand = unique_uit
	window = input("window size: ")
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
	outfile.write(regels.lstrip("\n"))
	file.close()
	outfile.close()
	    
	fastafile = open('fastaTmp.txt', 'r')
	
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
		    uitvoerbestand.write(seqline + "\n")
		elif motieven(code.eiwit(seqline[1:])) == "yes":
		    count2 += 1
		    uitvoerbestand.write(seqline[1:] + "\n")
		elif motieven(code.eiwit(seqline[2:])) == "yes":
		    count3 += 1
		    uitvoerbestand.write(seqline[2:] + "\n")
		elif motieven(code.eiwit(reverseComplement(seqline[:]))) == "yes":
		    countmin1 += 1
		    uitvoerbestand.write(reverseComplement(seqline[:]) + "\n")
		elif motieven(code.eiwit(reverseComplement(seqline[:-1]))) == "yes":
		    countmin2 += 2
		    uitvoerbestand.write(reverseComplement(seqline[:-1]) + "\n")
		elif motieven(code.eiwit(reverseComplement(seqline[:-2]))) == "yes":
		    countmin3 += 3
		    uitvoerbestand.write(reverseComplement(seqline[:-2]) + "\n")
		else:
		    print("None found")
		    uitvoer2.write(seqline + "\n")
		    nameseq = name_list[counttotal-1]
		    nomatch_list.append(nameseq)
		    countnonefound += 1
	uitvoerbestand.close()
	uitvoer2.close()
	print("Finished! Wrote output to {}".format(outputfile))
	print("No match found in: ", nomatch_list)        
else:
    print("Finished")
