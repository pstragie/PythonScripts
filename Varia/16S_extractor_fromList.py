'''
Created on 4-dec.-2013

@author: pstragie
'''
from Bio import Entrez
from io import BytesIO
Entrez.email = "pieter.stragier@ugent.be"
Entrez.tool = 'biopython'

uitvoer = open("16S_Xanthomonas.fasta", "w")
lijst = ["Y10766", "X95918", "X99299","Y10754", "Y10756", "AB558557", "X95919", "JX986960", "JX986954", "JX986962", "JX986955", "FR749910", "FR733718", "JX986961", "FR749942", "Y10755", "GU993265", "Y10765", "Y10759", "Y10757","Y10764","X95921","Y10762","Y10758", "JQ955625", "Y10760", "AB558558", "X95920", "FR749911", "Y10761","X95917", "X95922", "Y10763","AF208315", "M59158"]
for seq in lijst:

    Organism = seq
    print("Opzoeken: ", Organism)
    """ Obtain gene id number from Entrez """ 
    #Entrez.esearch in the nucleotide/gene/genome/nuccore database
    
    search_string = Organism
    handle = Entrez.esearch(db="nucleotide", usehistory="y", term=search_string)
    
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