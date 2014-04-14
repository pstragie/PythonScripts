#!/usr/bin/python3
'''
Created on 26 Mar 2013
Convert fasta to phylip format
@author: pstragie
'''

file = "C:/Users/pstragie/Species/Dickeya/MLSA/All/atpD/Dickeya_atpD.fasta"
filename = file.split(".")[0]
infile = open(file, "r")
outfile = open(filename+".tmp", "w")
count = 0
print("Converting to phylip format...")
for line in infile:
    if line.startswith(">"):
        count += 1
        head = line[1:].strip("\n")
        heading = ""
        for i in head:
            if i != " ":
                heading += i
            else:
                pass
    else:
        lengte = len(line)
        outfile.write('{:9s} {:s}'.format(heading, line))
infile.close()
outfile.close()

infile = open(filename+".tmp", "r")
outfile = open(filename+".phy", "w")

outfile.write(str(count) + " " + str(lengte) + "\n")
for line in infile:
    
    outfile.write(line)
infile.close()
outfile.close()
print("Finished")

