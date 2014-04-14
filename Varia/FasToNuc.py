#/usr/bin/python2
'''
Created on 26 Mar 2013
Convert fasta to .nuc and make the sequences multitudes of 3.
@author: pstragie
'''

file = "gyrB_inFrame1.fasta"
filename = file.split(".")[0]
infile = open("/home/pstragie/workspace/Clavibacter/Files/"+file, "r")
outfile = open("/home/pstragie/workspace/Clavibacter/Files/"+filename+".tmp", "w")
count = 0
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
        print(heading)
        outfile.write(heading + "  ")
    else:
        lengte = len(line) - 1
        if lengte % 3 == 0:
            outfile.write(line)
            lengte = lengte
        elif lengte % 3 == 1:
            outfile.write(line[:-2] + "\n")
            lengte = lengte - 1
        elif lengte % 3 == 2:
            outfile.write(line[:-3] + "\n")
            lengte = lengte - 2
infile.close()
outfile.close()

infile = open("/home/pstragie/workspace/Clavibacter/Files/"+filename+".tmp", "r")
outfile = open("/home/pstragie/workspace/Clavibacter/Files/"+filename+".nuc", "w")

outfile.write("\t" + str(count) + " " + str(lengte) + "\n")
for line in infile:
    outfile.write(line)
infile.close()
outfile.close()


