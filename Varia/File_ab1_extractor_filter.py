'''
Created on 17-jan.-2013

Verplaats alle sequencing bestanden naar de respectievelijke folders


@author: pstragie
'''
import shutil
import os
import fnmatch
#Locatie hoofdmap bepalen
totaal = 0

var = "Z:\\home\\Species\\Pseudomonas\\MLSA\\Unsorted"
dstatpA = "Z:\\home\\Species\\Pseudomonas\\MLSA\\All\\atpA"
dstglnA = "Z:\\home\\Species\\Pseudomonas\\MLSA\\All\\glnA"
dstrpoB = "Z:\\home\\Species\\Pseudomonas\\MLSA\\All\\rpoB"
dstrpoD = "Z:\\home\Species\Pseudomonas\\MLSA\\All\\rpoD"
dstsecA = "Z:\\home\Species\Pseudomonas\\MLSA\\All\\secA"
dstgshA = "Z:\\home\Species\Pseudomonas\\MLSA\\All\\gshA"

andere = "Z:\\home\\Species\\Pseudomonas\\MLSA\\All\\andere"
for dirpath, dirnames, filenames in os.walk(var, topdown=True, followlinks=False):
        
    print(dirpath)
        
    dirList=os.listdir(dirpath)
    print(dirList)
    for file1 in dirList: #file the files
        print(file1)
        if fnmatch.fnmatch(file1, '*.ab1'):
            try:
                if file1.split("_")[3].lower().startswith("atpa"):
                    dst = dstatpA
                elif file1.split("_")[3].lower().startswith("glna"):
                    dst = dstglnA
                elif file1.split("_")[3].lower() == "cm" or file1.split("_")[3].lower().startswith("rpob"):
                    dst = dstrpoB
                elif file1.split("_")[3].lower().startswith("laps"):
                    dst = dstrpoB
                elif file1.split("_")[3].lower().startswith("pseg") or file1.split("_")[3].startswith("rpoD"):
                    dst = dstrpoD
                elif file1.split("_")[3].lower().startswith("seca"):
                    dst = dstsecA
                elif file1.split("_")[3].lower().startswith("gsha"):
                    dst = dstgshA
                else:
                    dst = andere
            except:
                dst = andere
            print(file1) #echo the list of files to check 
            shutil.move(dirpath+'\\'+file1, dst+'\\'+file1) # move the files from origin to destination
            
            totaal += 1
print(totaal)                
