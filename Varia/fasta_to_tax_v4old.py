'''
Created on 26-nov.-2012
Maak een fasta-file klaar voor MOTHUR.
Geeft een tax-bestand en een bijhorend fas-bestand terug.
@author: pstragie
'''

import time


t = time.time()
##################################################
#Bestanden
infl = open('fasta.seq', 'r')
outflfas = open('fasta.fas', 'w')
outfltax = open('fasta.tax', 'w')
##################################################

for lijn in infl:
    if lijn.startswith(">"):
        #dubbele underscores verwijderen
        data_lijst = list(lijn)
        
        for i in range(len(data_lijst)-3):
            
            if data_lijst[i] == data_lijst[i+1] == data_lijst[i+2] == "_":
                del data_lijst[i+1]
                del data_lijst[i]
            if data_lijst[i] == data_lijst[i+1] == "_":
                del data_lijst[i]    
        lijn = "".join(data_lijst)
        
        woorden = lijn.split("_")
        lijn = woorden[0] + "\t" + ";".join(woorden[1:])
        outflfas.write(lijn)
        lijn = lijn[1:].rstrip()
        outfltax.write(lijn+";"+"\n")
    else:
        outflfas.write(lijn)
print("ready")
print("klaar in %.3f secondeen" % (time.time()-t))       
