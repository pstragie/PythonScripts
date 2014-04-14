#/usr/bin/python3
'''
Created on 26 Mar 2013

@author: pstragie
'''

file1 = open("/home/pstragie/workspace/Clavibacter/dnaA.fas", "r")
file2 = open("/home/pstragie/workspace/Clavibacter/gyrB.fas", "r")
outfile = open("/home/pstragie/workspace/Clavibacter/compare.txt", "w")

file1list = []
file2list = []
for line in file1:
    if line.startswith(">"):
        file1list.append(line.split("|")[1].strip("\n"))
for line in file2:
    if line.startswith(">"):
        file2list.append(line.split("|")[1].strip("\n"))
file1list.sort()
file2list.sort()
file1.close()
file2.close()
outfile.close()

print(file1list)
print(file2list)

file = "gyrB.fas"
filename = file.split(".")[0]
infile = open("/home/pstragie/workspace/Clavibacter/"+file, "r")
outfile = open("/home/pstragie/workspace/Clavibacter/"+filename+".tmp", "w")
count = 0
for line in infile:
    if line.startswith(">"):
        
        head = line.split("|")[1]
        print(head)
        if head in file1list and head in file2list:
            count += 1
            outfile.write(">" + head)
    else:
        lengte = len(line) - 1
        outfile.write(line)
infile.close()
outfile.close()

