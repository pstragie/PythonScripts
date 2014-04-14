'''
@Author: pieter.stragier@ugent.be
@Version: v0.2
Date: 18/03/2014

Run this to obtain pairwise blast identity % mean values and pairwise numbers of orthologs
Input file = mclInput
'''
import os, argparse

#Options
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input folder")
args = parser.parse_args()

#output file
output = open(args.input + "/pairwise_meanvalues.txt", 'w')
output.write("Pairwise comparison of mean identity percentages.\n")
output.write(args.input+"\n\n")
output.write("combo\tmean Id%\tnumber of orthologs\n")

#main script
def main():
	mclinput = open(args.input + "/mclInput", 'r')
	simseq = open(args.input + "/similarSequences.txt", 'r')
	
			
	#Put mcl data into dict
	print("mcldict...")	
	taxonset = set()
	mcldict = {}
	for regel in mclinput:
		lijst = regel.split()
		for i in lijst:
		    if i.__contains__("|"):
		        taxon_id = i.split("|")[0]
		        taxonset.add(taxon_id)
		mcldict[regel.split("\t")[0]+"*"+ regel.split("\t")[1]] = 0
	mclinput.close()
	
	#make dictionary of similarsequences	
	print("orthdict...")	
	orthdict = {}	
	for regel in simseq:
		A = regel.split("\t")[0]
		B = regel.split("\t")[1]
		s = A + "*" + B
		Idperc = regel.split("\t")[6]
		orthdict[s] = Idperc
	simseq.close()
	#extract id % from similarSequences.txt based on mcldict 
	print("comparing...")
	resdict = {}	
	for a, b in orthdict.items():
		
		if a in mcldict.keys():
			combo = a.split("*")[0].split("|")[0] + "_" + a.split("*")[1].split("|")[0]
			if combo in resdict.keys():	
				lijst = resdict[combo]
				lijst.append(float(b))				
				resdict[combo] = lijst
			else:
				resdict[combo] = [float(b)]
	
	#Create matrix for percentages
	matrix = []
	for r in range(len(taxonset)+1):
		matrix += [["  *  "] * (len(taxonset)+1)] 	
	for y in range(0, len(taxonset)):
		matrix[0][y+1] = "{:6}".format(list(taxonset)[y])
		matrix[y+1][0] = "{:6}".format(list(taxonset)[y])
	
	#Create matrix for number of orthologs
	matrixO = []
	for r in range(len(taxonset)+1):
		matrixO += [["  *  "] * (len(taxonset)+1)] 	
	for y in range(0, len(taxonset)):
		matrixO[0][y+1] = "{:6}".format(list(taxonset)[y])
		matrixO[y+1][0] = "{:6}".format(list(taxonset)[y])

	#Calculate mean values
	print("calculating...")
	for k, v in sorted(resdict.items()):
		aantal = len(v)
		mean = sum(v)/aantal
		
		#Fill matrix		
		A, B = k.split("_")	
		for y in range(len(taxonset)):
			for z in range(len(taxonset)):
				if matrix[0][y+1].startswith(str(A)) and matrix[z+1][0].startswith(str(B)):
					matrix[z+1][y+1] = str(round(mean, 2))
					matrixO[z+1][y+1] = str(aantal).center(6, " ")
				elif matrix[0][y+1].startswith(str(B)) and matrix[z+1][0].startswith(str(A)):
					matrix[z+1][y+1] = str(round(mean, 2))
					matrixO[z+1][y+1] = str(aantal).center(6, " ")

		print("{}\t{}\t{}".format(k, mean, aantal))
		output.write("{}\t{}\t{}\n".format(k, mean, aantal))
	
	#Empty line in output file
	output.write("\n")
	output.write("Matrix of mean identity percentages\n")	
	
	#Matrix output percentages	
	for x in matrix:
		print("\t".join(x))
		output.write("{}\n".format("\t".join(x)))

	#Empty line in output file
	output.write("\n")
	output.write("Matrix of number of orthologs\n")	
	
	#Matrix output number of orthologs	
	for x in matrixO:
		print("\t".join(x))
		output.write("{}\n".format("\t".join(x)))


	
	
	
if __name__ == "__main__":
	main()
