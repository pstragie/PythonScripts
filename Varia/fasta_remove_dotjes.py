'''
Created on 6-dec.-2012

@author: pstragie
'''
''' Verwijdert alle punten in de sequentie (niet in de hoofding) van een fasta-file. '''
########## Bestandsnamen aanpassen #########
invoer = open('testfasta.fasta', 'r')
uitvoer = open('testfastauit.fasta', 'w')

########## Script #########
for regel in invoer:
    if regel.startswith(">"):
        uitvoer.write(regel)
    else:
        nieuwe_regel = ''
        for i in regel:
            if i != '.':
                nieuwe_regel += i
        uitvoer.write(nieuwe_regel)
invoer.close()
uitvoer.close()