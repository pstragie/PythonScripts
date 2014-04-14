'''
@Author: pieter.stragier@ugent.be
@Version: v0.1
Script to extract the common clusters into separate fasta files per cluster
'''
import os, itertools, argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input_file", help="input file")
parser.add_argument("-f", "--folder", help="folder that contains the files")
parser.add_argument("-c", "--compliantFastaFolder", help="folder with compliantFasta", default="compliantFasta")
args = parser.parse_args()
if not (args.input_file and args.folder):
	print("Input data missing")
	print("Use -i <file> to set the location and name of the input file")
else:		
	bestand = os.path.join(args.folder, args.input_file)
	invoer = open(bestand, 'r')


	#Extract the core gene accession numbers (orthologs present in all species)

	dct = {}
	complete_set = set()
	for regel in invoer:
		sleutel = regel.split(":")[0]
		waarde = list(regel.split(":")[1].split())
		setje = set()
		for x in waarde:
			stam = x.split("|")[0]
			setje.add(stam)	
			complete_set.add(stam)
		aantal = len(setje)
		dct[sleutel] = [waarde, aantal]
	aantal_stammen = len(complete_set)
	count = 0
	invoer.close()
	
	
	AA = ""
	seqdb = {}
	for k, v in dct.items():
		count += 1
		print("{}/{}".format(count, len(dct)))
		if v[1] == aantal_stammen:
			
			protdct = {}
			for prot in v[0]:
				
				
				
				stam, ref = prot.split("|")
				seq = stam + ".fasta"
				bestand = open(os.path.join(args.folder,args.compliantFastaFolder,seq), 'r')
				for regel in bestand:
					if regel.startswith(">"):
						if AA != "":
							
							if heading == prot:
								protdct[prot] = AA
								
						AA = ""
						heading = regel.lstrip(">").rstrip()
					else:
						AA += regel.strip()
							
				seqdb[k] = protdct	
				bestand.close()

	print(seqdb)
	for k, v in seqdb.items():
		if len(v) == aantal_stammen:
			
			Fastafolder = os.path.join(args.folder, "cluster_fastafiles")
			if not os.path.exists(Fastafolder):
				os.mkdir(Fastafolder)
			uitvoer = open(Fastafolder+"/"+k+".fasta", "w")
			for s, w in v.items():			
				uitvoer.write(">"+s+"\n")
				uitvoer.write(w+"\n")
			uitvoer.close()
