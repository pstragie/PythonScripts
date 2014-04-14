'''
Created on 1-feb.-2013
Extract DNA gene sequences from NCBI in fasta format, based on your choice of Organism and Gene.
@author: pstragie
'''

from Bio import Entrez
from io import BytesIO
import os
Entrez.email = "pieter.stragier@ugent.be"

def complement(nucleotide):
    '''
    Geef de complementaire nucleotide terug
    '''
    if nucleotide == "G":
        return "C"
    elif nucleotide == "C":
        return "G"
    elif nucleotide == "A":
        return "T"
    elif nucleotide == "T":
        return "A"
    elif nucleotide == "R":
        return "Y"
    elif nucleotide == "Y":
        return "R"
    elif nucleotide == "W":
        return "W"
    elif nucleotide == "S":
        return "S"
    elif nucleotide == "K":
        return "M"
    elif nucleotide == "M":
        return "K"
    elif nucleotide == "B":
        return "V"
    elif nucleotide == "D":
        return "H"
    elif nucleotide == "H":
        return "D"
    elif nucleotide == "V":
        return "B" 
    else:
        return "-"
    
def ReverseComplement(sequence):
    '''
    Geef de reverse complementaire sequentie terug
    '''
    inverscomplement = ""
    for nucleotide in sequence[::-1]:
        inverscomplement += complement(nucleotide)
    return inverscomplement

#Esearch
print("Extract DNA sequences from NCBI Entrez Gene database.")
Org = str(input("Organism: "))
Q1 = str(input("General search ('A') or Gene search ('G'): "))
if Q1 == "A" or Q1 == "a":
    Gene = str(input("Term: "))
elif Q1 == "G" or Q1 == "g" or Q1 == "gene" or Q1 == "Gene":
    Gene = str(input("Gene: ")) + "[GENE]"
print(Gene)




search_string = str(Org + "[ORGN]+" + Gene) 
print("search string = " + search_string)
try:
    maxnum = int(input("Maximum number of results? (default = 20): "))
except:
    maxnum = 20
if maxnum == "":
    maxnum = 20
handle = Entrez.esearch(db="gene", usehistory="y", retmax = maxnum, term=search_string)

#change to bytes
#bytehandle = BytesIO(bytes(handle.read(), 'utf-8'))
record = Entrez.read(handle)
print("Total = {}".format(record["Count"]))
print("IdList length = {}".format(len(record["IdList"])))

handle.close()

ID_list = record["IdList"]
print(ID_list)
teller = min([maxnum, len(ID_list)])
handle.close()
print("Esearch finished")

#empty the file
outfile = str(Org + "_" + Gene + ".tmp")
file = open(outfile, "w")
file.write("")
file.close()


#Efetch from gene
lijst = ",".join(ID_list)
net_handle = Entrez.efetch(db="gene", id=lijst, rettype="gb", retmode="text")
out_handle = open("my_file.tmp", "w")

for line in net_handle:
    out_handle.write(line)

out_handle.close()
net_handle.close()
print("Efetch from gene ready. Output (n = {}) written in my_file.tmp".format(teller))
print("Efetch sequences in nuccore...")

#Extract annotation from gene information in my_file.txt
infile = open("my_file.tmp", "r")
infile.readline()
teller2 = teller

RC = {}

out_handle = open(outfile, "a")
teller3 = 1
for data in infile:
    
    if data.startswith("Annotation"):
        if data.__contains__("complement"):
	    try:
	        _, name, loc, comp = data.split(" ")
		start, stop = loc[1:-1].split("..")
            except:
		print("Data could not be automatically extracted: {}".format(data))
		name = input("NC#: ")
		start = input("from: ")
		stop = input("till: ")
	    
	    RC[teller3] = "complement"
	else:    
	    try:            
		_, name, loc = data.split(" ")
                start, stop = loc[1:-2].split("..")
	    except:
		print("Data could not be automatically extracted: {}".format(data))
		name = input("NC#: ")
		start = input("from: ")
		stop = input("till: ")
	    RC[teller3] = "forward"
        teller3 += 1
        print(str(teller2) + " " + name + " from " + start + " till " + stop) 
        teller2 = teller2 - 1
        #Efetch in nuccore   
        in_handle = Entrez.efetch(db="nuccore", id=name, rettype="fasta", seq_start=start, seq_stop=stop)
        
        for line in in_handle:
	    out_handle.write(line)
	in_handle.close()
out_handle.close()
infile.close()
print("Efetch ready. {} sequences written to {}".format(teller, outfile))
print("Checking complementarity...")
comp = RC.values().count("complement")
print("{} complement sequences found. Making reverse complement ... ".format(comp))


#Clean up fasta file
file = open(outfile, "r")
outfilefas = str(Org + "_" + Gene + ".tmp2")
outfile = open(outfilefas, "w")

regels = ""
for regel in file:
    if regel.startswith(">"):
        regels += "\n" + regel
    else:
        regels += regel.rstrip()
outfile.write(regels)
file.close()
outfile.close()
#Reverse Complement when needed
infile = open(outfilefas, "r")
outfilefas = str(Org + "_" + Gene + ".fasta")
outfile = open(outfilefas, "w")
infile.readline()
count = 0
regels = ""
for regel in infile:
    if regel.startswith(">"):
	regels += ">"
	specs = " ".join(regel.split(" ")[1:5])
	regels += specs + "\n"
	
	count += 1
    else:
	if RC[count] == "forward":
	    regels += regel
	    
	else:
	    regels += ReverseComplement(regel.rstrip("\n")) + "\n"
outfile.write(regels)
infile.close()
outfile.close()
print("output written to {}".format(outfilefas))
print("removing temporary files...")
filelist = [f for f in os.listdir(".") if f.__contains__("tmp")]
for f in filelist:
    os.remove(f)
print("Done!")
