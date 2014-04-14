
'''
Created on 26-nov.-2012
Maak een fasta-file klaar voor MOTHUR.
Geeft een tax-bestand en een bijhorend fas-bestand terug.
@author: pstragie
'''

import time
import os

t = time.time()
##################################################
#Bestanden hier aanpassen
fastabestand = 'trainset_EMBL.fasta'
##################################################


#bestandsnaam extraheren
naam, ext = fastabestand.split(".")
#bestand openen
infl = open(fastabestand, 'r')
#uitvoerbestand bepalen
revisie = naam + "_revisie.fasta"
outflfasta = open(revisie, 'w')
unique_uit = naam + "_unique.fasta"
outflfas = open(unique_uit, 'w')


for lijn in infl:
    
    if lijn.startswith(">"):
        outflfasta.write("\n")
        outflfasta.write(lijn.strip("\n").strip(".") + "\n")
        
    else:
        outflfasta.write(lijn.strip("\n"))

outflfasta.close()
infl.close()

#Eerste lege lijn verwijderen
bestand = open(revisie, 'r')
lines = bestand.readlines()
bestand.close()
lines = filter(lambda x: not x.isspace(), lines)
bestand = open(revisie, 'w')
bestand.writelines(lines)
bestand.close()

#Invoerbestand filteren op unieke sequenties
print("Unieke sequenties filteren...")
infl = open(revisie, "r")
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
	informatie = lijn.split("|")[2]
	
	info_lijst = []
	nummer = informatie.split(" ")[0]
	for i in informatie.split(" ")[1:]:
	    info_lijst.append(i.strip(" ").strip(","))
	info = "_".join(info_lijst)
	
	phylo = "Root;Bacteria;" + info
	phylotax = "Bacteria;" + info.rstrip("\n") + ";"
	titel = ">" + nummer.rstrip('\n') + "\t" + phylo
	titeltax = nummer.rstrip('\n') + "\t" + phylotax + "\n"	
	outflfas.write(titel)
	outfltax.write(titeltax)
	
    else:
	outflfas.write(lijn)
infl.close()
outflfas.close()
outfltax.close()
filelist = [f for f in os.listdir(".") if f.__contains__("revisie") or f.__contains__("unique")]
for f in filelist:
    os.remove(f)

print("Klaar in {} seconden".format(time.time() - t))






