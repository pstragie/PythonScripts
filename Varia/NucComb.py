#/usr/bin/python3
'''
Created on 27 Mar 2013

@author: pstragie
'''


files = ["dnaA_inFrame1.nuc", "gyrB_inFrame1.nuc"]
listlength = len(files)
output = open("/home/pstragie/workspace/Clavibacter/Files/concatenated.nuc", "w")
totalcount = 0

countlist = []
lijntjeslist = []
for al in files:
    doc = open("/home/pstragie/workspace/Clavibacter/Files/" + al, "r")
    doc.readline()
    
    
    lijntjes = 0
    for line in doc:
        lijntjes += 1
        sequence = line.split("  ")[1]
        seqlength = len(sequence) -1
    countlist.append(seqlength)
    lijntjeslist.append(lijntjes)
    doc.close()

totalnuc = sum(countlist)


print(str(lijntjeslist[0]) + " " + str(totalnuc) + " G")        
print("G " + str(listlength) + " " + str(countlist[0]) + " " + str(countlist[1]))
output.write(str(lijntjeslist[0]) + " " + str(totalnuc) + " G\n")
output.write("G " + str(listlength) + " " + str(countlist[0]) + " " + str(countlist[1]) + "\n")
seqdic = {}
for al in files:
    doc = open("/home/pstragie/workspace/Clavibacter/Files/" + al, "r")
    doc.readline()
    for line in doc:
        nameseq = line.split("  ")
        if not nameseq[0] in seqdic:
            seqdic[nameseq[0]] = nameseq[1].strip("\n")
        else:
            seqdic[nameseq[0]] += nameseq[1].strip("\n")
        
print(seqdic)
print(len(seqdic))

for key, value in seqdic.items():
    
    a = "".join(value)
    b = ""
    for i in range(0, len(a), 3):
        b += a[i:i+3] + " "
    print(b)
    output.write(key + "  " + b + "\n")
output.close()
