'''
Created on 11-sep.-2013

@author: pstragie
'''
'''
Created on 1-feb.-2013
Extract genome sequences from NCBI in fasta format, based on your choice of Organism
@author: pstragie
'''

from Bio import Entrez
from io import BytesIO
#import xml.etree.ElementTree as etree
import os
Entrez.email = "pieter.stragier@ugent.be"

def GetGenomeID(Organism, maxnum=170):
    search_string = Organism + "[Orgn]"
    handle = Entrez.esearch(db="genome", usehistory="y", retmax = maxnum, term=search_string)

    #Extract data from search file
    bytehandle = BytesIO(bytes(handle.read(), 'utf-8'))
    handle.close()
    record = Entrez.read(bytehandle)
    print("Totaal = {} (gevonden ID nummers)".format(record["Count"]))
    genomeID_list = list(record["IdList"])
    
    print(genomeID_list)
    return genomeID_list
    

# Fetch bioproject from bioproject
# Extract the Assembly accession number!

def GetLink(Id):
    
    """Return a list of LinkIDs"""
    handle = Entrez.elink(dbfrom="genome", db="nuccore", id=Id)
    
    #Extract data from search file
    bytehandle = BytesIO(bytes(handle.read(), 'utf-8'))
    handle.close()
    record = Entrez.read(bytehandle)
    
    dlist, lijstnuc = [], []
    try:
        LinkID_dict = record[0]["LinkSetDb"][0]
        
        lijstnuc = []
        dlist = LinkID_dict["Link"]
        
    except:
        pass
    for i in dlist:
        for v in i.values():
            lijstnuc.append(v)
    print("Aantal = {} (gevonden IDs in de nuccore database)".format(len(lijstnuc)))
    return lijstnuc

def GetGenomeFasta(Org, GenID, lijstje, formaat="fasta", bestand=open("overzicht.txt", "w"), plasmid=False):
    
    teller = 0
    for Id in lijstje:
        net_handle = Entrez.efetch(db="nuccore", id = Id, rettype=formaat, retmode="text")
        data = net_handle.read()
        
        if formaat == "fasta":    
            part = data.split("\n")[0].split("|")[4].split(" ")
            name = data.split("\n")[0].split("|")[4].split(",")[0]
            
            if name.split()[1] == "sp.":
                print("unknown species not downloaded")
            else:
                if plasmid == True and "plasmid" in part:
                    naam = name + "_" + part[2] + "_plasmid"
                    naam = naam.replace("*", "_")
                    print("Plasmide!")
                elif plasmid == False and "plasmid" in part:
                    pass
                else:
                    naam = name + "_" + part[2]
                    naam = naam.replace("*", "_")
                    sequence = data.split("\n")[1]
                    if len(sequence) > 1:
                        bestand.write(Id + "\t" + naam + "\n")
                        file = naam + "_" + Id + "_" + str(len(data.split("\n")[1:])*len(data.split("\n")[1:][0])) + "." + formaat
                        if not os.path.exists(Org):
                            os.makedirs(Org)
                            
                        if os.path.isfile(Org+"/"+file) == False:
                            outfile = open(Org + "/" +file, "w")
                            outfile.write(data)
                            outfile.close()
                        teller += 1
                    else:
                        print("Geen sequentie gevonden voor {}, {}".format(name, GenID))
        elif formaat == "gb":
            
            for regel in data:
                if regel.startswith("SOURCE"):
                    species = Org + " " + regel.split(Org)[1]
                else:
                    species = "unknown"
            file = species + "_" + Id + "_" + str(len(data.split("\n")[1:])*len(data.split("\n")[1:][0])) + "." + formaat
            print(file)
            outfile = open(Org + "/" + file, "w")
            outfile.write(data)
            outfile.close()
            teller += 1
    
    
    return "Genome written to file ({} bestanden)".format(teller)


#Esearch for genomes
print("Extract DNA sequences from NCBI Entrez Genome database.")
#Org = str(input("Organism: "))
Org = "Pseudomonas"
#Format = str(input("gb or fasta: "))
Format = "fasta"
# Search for genome ID (list)
# Link genome ID to query_key and WebEnv
bestand = open(Org + "/overzicht.txt", "w")
for BPnummer in GetGenomeID(Org):
    lijstje = GetLink(BPnummer)
    print("{}: {}".format(BPnummer, lijstje))
    print(GetGenomeFasta(Org, BPnummer, lijstje, formaat=Format, bestand=bestand, plasmid=False))
bestand.close()   
print("Done!")
