#/usr/bin/python3
'''
Created on 26 Mar 2013

@author: pstragie
'''

file = "dnaA.fasta"
filename = file.split(".")[0]
infile = open("/home/pstragie/workspace/Clavibacter/Files/"+file, "r")
outfile = open("/home/pstragie/workspace/Clavibacter/Files/"+filename+".tmp", "w")
count = 0
for line in infile:
    if line.startswith(">"):
        count += 1
        head = line[1:].strip("\n")
        print(head)
        outfile.write(head+ "     ")
    else:
        lengte = len(line) - 1
        outfile.write(line)
infile.close()
outfile.close()

infile = open("/home/pstragie/workspace/Clavibacter/Files/"+filename+".tmp", "r")
outfile = open("/home/pstragie/workspace/Clavibacter/Files/"+filename+".seq", "w")

outfile.write(" " + str(count) + " " + str(lengte) + "\n")
for line in infile:
    outfile.write(line)
infile.close()
outfile.close()


