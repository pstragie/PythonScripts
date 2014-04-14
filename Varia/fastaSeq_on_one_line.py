'''
Created on 3-dec.-2012

@author: pstragie
'''
''' 
leest een fasta-bestand en verwijdert end-of-lines tussen de sequenties.
'''
#Bestandsnamen aanpassen
file = open('fastatestCP.txt', 'r')
outfile = open('fastatestCP_out.txt', 'w')

#Script (afblijven)
regels = ""
for regel in file:
    if regel.startswith(">"):
        regels += "\n" + regel
    else:
        regels += regel.rstrip()
outfile.write(regels)
