
'''
Created on 26-nov.-2012
Maak een fasta-file klaar voor MOTHUR.
Geeft een tax-bestand en een bijhorend fas-bestand terug.
@author: pstragie
'''

import time


t = time.time()
##################################################
#Bestanden hier aanpassen
fastabestand = 'Test.fasta'
##################################################


#bestandsnaam extraheren
naam, ext = fastabestand.split(".")
#bestand openen
infl = open(fastabestand, 'r')
#uitvoerbestand bepalen
unique_uit = naam + "unique.fasta"
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

infl = open(unique_uit, 'r')
fasuit = naam + ".fas"
outflfas = open(fasuit, 'w')
taxuit = naam + ".tax"
outfltax = open(taxuit, 'w')

#Unieke invoer omzetten naar fas en tax bestand
print("fasta omzetten naar fas en tax...")
for lijn in infl:
    if lijn.startswith(">"):
	lijn.rstrip("\n")
	spec, nummer = lijn.split("|")
	
	genus, species = spec[1:].split(" ")
	phylo = "Root;Bacteria;" + genus + ";" + genus + "_" + species
	phylotax = "Bacteria;" + genus + ";" + genus + "_" + species	
	titel = ">" + nummer.rstrip('\n') + "\t" + phylo + "\n"
	titeltax = nummer.rstrip('\n') + "\t" + phylotax + ";" + "\n"	
	outflfas.write(titel)
	outfltax.write(titeltax)
	
    else:
	outflfas.write(lijn)
infl.close()
outflfas.close()
outfltax.close()
print("Klaar in {} seconden".format(time.time() - t))






