'''
Created on 23-okt.-2013

@author: pstragie
'''
bestand = open("Bionumerics_export\\rpoB_Valoram.txt", "r")
uitvoer = open("Bionumerics_export\\rpoB_Valoram.fasta", "w")

for regel in bestand:
    key = ""
    if regel.startswith(">"):
        #key
        stam = regel.split("[")[0][1:]
        for i in stam:
            if i == " ":
                pass
            elif i == "-":
                pass
            else:
                key += i
        #species
        species = regel.split("[")[1].split("]")[0].split("=")[1]
        print(species)
        #gene
        #gene = regel.split(",")[0].split("for")[1].lstrip()
        #uitvoer.write(">" + key + "|" + species + "|" + gene + "\n")
        
        #uitvoer wegschrijven
        uitvoer.write(">" + key.rstrip() + "|" + species + "\n")
    else:
        #sequentie
        seq = regel
        uitvoer.write(regel)

bestand.close()
uitvoer.close()
        