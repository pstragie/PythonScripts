'''
Created on 3-dec.-2013

@author: pstragie
'''
from Bio import Entrez
from io import BytesIO


Entrez.email = "pieter.stragier@ugent.be"
Entrez.tool = 'biopython'
maxnum = 50

uitvoer = open("BN_adding16S.fasta", "w")

invoer = open("BN_missing16S", "r")
invoer.readline()

for regel in invoer:
    Organism = regel.split("\t")[1]
    if not Organism.startswith("R-"):
        print("Opzoeken: ", Organism)
        """ Obtain gene id number from Entrez """ 
        #Entrez.esearch in the nucleotide/gene/genome/nuccore database
        
        search_string = Organism + " AND 16S rRNA[Gene]"
        handle = Entrez.esearch(db="nucleotide", usehistory="y", retmax = maxnum, term=search_string)
        
        #Extract data from search file
        bytehandle = BytesIO(bytes(handle.read(), 'utf-8'))
        handle.close()
        record = Entrez.read(bytehandle)
        
        print("Totaal = {} (gevonden ID nummers)".format(record["Count"]))
        geneID_list = record["IdList"]
        print("geneID_lijst: ", geneID_list)
        
        """ Fetch the sequence """
        #Fetch the fasta sequence
        if len(geneID_list) == 1:
            handle = Entrez.efetch(db="nuccore", id=geneID_list, rettype="fasta")
            data = handle.read()
            if len(data) < 2000:
                uitvoer.write(data + "\n")
            
    else:
        print("Niet opgezocht: {}".format(Organism))
invoer.close()
uitvoer.close()