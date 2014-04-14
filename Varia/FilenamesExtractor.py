'''
Created on 30-nov.-2012
Haalt de isolaatnummers uit een map met sequentiebestanden.
@author: pstragie
'''
import glob
import os

################### Enter your folder here ######################
os.chdir("C:\\Users\\pstragie\\Species\\Dickeya\\MLSA\\atpD ab1")
#################################################################

#files opvragen
species_dict = {}
experiment = {}
for files in glob.glob("*.ab1"):
    if files.split("_")[3] in experiment.keys():
        experiment[files.split("_")[3]] += 1
    else:
        experiment[files.split("_")[3]] = 1
    species = files.split("_")[2]
    species_dict[species] = files.split("_")[3]
    
print(experiment)
print("Aantal isolaten:", len(species_dict))
print("Aantal sequenties per isolaat:", set(species_dict.values()))
# Maak een strain number lijst
species_list = sorted(list(species_dict.keys()))
strain_list = []

for i in species_list:
    strain_string = ''
    for j in i:
        if j == "G":
            strain_string += j + " "
        elif j == "R":
            strain_string += j + "-"
        else:
            strain_string += j
    strain_list.append(strain_string)
   
    
print()
print("lijst van isolaten.")
print("ID\tKEY\tEXP\tSTRAIN_NUMBER")

for i in range(0, len(species_list)):
    print('{}\t{}\t{}\t{}'.format(species_list[i], species_list[i], species_dict[species_list[1]], strain_list[i]))
    
'''
you can use glob

import glob
import os
os.chdir("/mydir")
for files in glob.glob("*.txt"):
    print files
or simple os.listdir

import os
os.chdir("/mydir")
for files in os.listdir("."):
    if files.endswith(".txt"):
        print files
or if you want to traverse directory

import os
for r,d,f in os.walk("/mydir"):
    for files in f:
        if files.endswith(".txt"):
             print os.path.join(r,files)
'''             
