'''
@Author: pieter.stragier@ugent.be
@Version: v0.2
Date: 18/03/2014

Run this to obtain the cluster count
Input file = groups.txt
'''

import os, itertools, argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input folder")
args = parser.parse_args()
if not args.input:
	print("Input data missing")
	print("Use -i <file> to set the location and name of the input file")
else:		
	bestand = args.input + "/groups.txt"
	
	invoer = open(bestand, 'r')
	complete_set = set()
	comp_dct = {}
	for regel in invoer:
		heading, combos = regel.split(":")
		setje = set()	
		for c in combos.split():
			genome = c.split("|")[0]	
			setje.add(genome)	
			complete_set.add(genome)
		comp_dct[heading] = setje

	print(complete_set)
	lijst_combos = []
	maxL = len(complete_set)
	print("Aantal genomen: {}".format(maxL))
	for x in range(2, len(complete_set)+1):
		combos = itertools.combinations(complete_set, x)
		lijst_combos.append(set(combos))

	dct = {}
	while maxL > 0:
	
		for k, v in comp_dct.items():
			x = str(maxL)
			tel = "tel" + x
		
			if len(v) == maxL:
				dct[tel] = dct.get(tel, 0) + 1
		maxL -= 1

	#print(comp_dct)
	teller = 0
	for k, v in dct.items():
		print("{}: {}".format(k, v))
		teller += v
	print("Total number of orthologs: {}".format(teller))
	
	ana_dct = {}
	for k, v in comp_dct.items():
		ana_dct[str(v)] = ana_dct.get(str(v), 0) + 1
	for k, v in sorted(ana_dct.items()):
		print("{}: {}".format(k.lstrip("set([").rstrip("])"), v))
