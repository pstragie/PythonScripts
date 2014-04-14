#!/usr/bin/python3
'''
Created on 26-nov.-2012
Extract sequences with unique name or sequence from fasta file
@author: pstragie
'''
fastabestand = str(input("bestandsnaam: "))
#bestandsnaam extraheren
naam, ext = fastabestand.split(".")
#bestand openen
infl = open(fastabestand, 'r')

filter = str(input("filter on name ('N') or sequence ('S')? "))
if filter == "S" or filter == "sequence":
	
	#uitvoerbestand bepalen
	unique_uit = naam + "_unique_sequences.fasta"
	outflfas = open(unique_uit, 'w')

	#Invoerbestand filteren op unieke sequenties
	print("Unieke sequenties filteren...")

	seq_dict = {}

	for lijn in infl:
	    if lijn.startswith(">"):
		name = lijn
		
	    else:
		if lijn in seq_dict.keys():
		    pass
		else:
		    seq_dict[lijn] = name
	    
		    outflfas.write(name)
		    outflfas.write(lijn)
	print("{} sequenties in bestand".format(len(seq_dict)))
	infl.close()
	outflfas.close()

elif filter == "N" or filter == "name":
	
	#uitvoerbestand bepalen
	unique_uit = naam + "_unique_names.fasta"
	outflfas = open(unique_uit, 'w')

	#Invoerbestand filteren op unieke namen
	print("Unieke namen filteren...")

	seq_dict = {}

	for lijn in infl:
	    if lijn.startswith(">"):
		if lijn in seq_dict.keys():
		    pass
		    out = 1
		else:
		    seq_dict[lijn] = lijn
		    outflfas.write(lijn)
		    out = 0
	    else:
		if out == 1:
		    pass
		else:
		    outflfas.write(lijn)	    

	print("{} sequenties in bestand".format(len(seq_dict)))
	infl.close()
	outflfas.close()
