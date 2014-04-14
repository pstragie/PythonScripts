'''
Created on 11-dec.-2012
Bionumerics output -- > fasta-formaat
@author: pstragie
'''
###invoerbestand###
invoer = open('export.txt', 'r')
###uitvoerbestand###
uitvoer = open('export.fasta', 'w')

###script (afblijven)###
for regel in invoer:
    if regel != '\n':
        hoofding, sequentie = regel.split()
        uitvoer.write('>{}\n'.format(hoofding))
        uitvoer.write("{}\n".format(sequentie))
    
