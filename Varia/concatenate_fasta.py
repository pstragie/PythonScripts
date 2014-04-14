'''
Created on 8-nov.-2012
Concateneer contigs of meerdere fasta's tot 1 sequentie
@author: pstragie
'''
#invoerbestand invullen (in zelfde folder als script)
infl = open('PD5684PEptp100simplified.fa', 'r')
#uitvoerbestand invullen
outflfas = open('PD5684PEptp100simplifiedconcatenated.fa', 'w')
#Nieuwe hoofding kiezen voor de sequentie
hoofding = ">PD5684PEptp100simplifiedconcatenated"

#Script (afblijven)
print(hoofding, end = "\n", file = outflfas)
count = 0
for line in infl:
    if line.startswith('>'):
        count += 1
    else:
        print(line.strip(), end = "", file= outflfas)    

print("%s contigs concatenated" % count)
