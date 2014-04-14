'''
@Author: pieter.stragier@ugent.be
@Version: v0.3
Date: 18/03/2014

This script will run all orthomcl analyses after the blastp step in orthoMCL.
It will also run 3 python scripts for data analysis.

Good luck!
'''

import os, subprocess, argparse
cur = os.getcwd()
print("Current working directory: {}".format(cur))
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input folder")
parser.add_argument("-o", "--overwrite", help="overwrite existing files", default=False)
parser.add_argument("-c", "--core_cluster", help="execute core_genome cluster script. yes/no", default="ask")
parser.add_argument("-m", "--mean_identity", help="execute identity_mean script. yes/no", default="ask")
args = parser.parse_args()
print("File directory (user input): {}".format(args.input))

if args.overwrite == True or args.overwrite.lower() == "yes":
	overwrite = True
else:
	overwrite = False

def main():
	if not args.input:
		print("Input data missing")
		print("Use -i <file> to set the folder with the all-vs-all.tsv file")
	else:
		if overwrite == True:
			print("Overwiting is granted")
		else:		
			print("Overwriting not granted")		
		var = args.input
		os.chdir(var)
		#Start subprocesses
		#Verify overwrite rights
		if overwrite == False:
			if os.path.exists(args.input+"/similarSequences.txt"):
				print("similarSequences already exists")
			else:		
				subprocess.call("orthomclBlastParser all-vs-all.tsv compliantFasta > similarSequences.txt", shell = True)
				print("Klaar met BlastParser. Running LoadBlast...")
			if os.path.exists(args.input+"/mclOutput"):
				print("mclOutput already exists")
			else:				
				subprocess.call("mcl mclInput --abc -I 1.5 -o mclOutput", shell=True)
				print("Klaar met mcl. Running MclToGroups...")
			if os.path.exists(args.input+"/groups.txt"):
				print("groups.txt already exists")
			else:
				subprocess.call("orthomclMclToGroups my_prefix 1000 < mclOutput > groups.txt", shell=True)
				print("Klaar MclTogroups. Running ExtractProteinIdsFromGroupsFile...")
			if os.path.exists(args.input+"/protIds.txt"):
				print("protIds.txt already exists")
			else:
				subprocess.call("orthomclExtractProteinIdsFromGroupsFile groups.txt > protIds.txt", shell=True)
				print("Klaar met protIds. Running ExtractProteinPairsFromGroupsFile...")
			if os.path.exists(args.input+"/pairs.txt"):
				print("pairs.txt already exists")
			else:
				subprocess.call("orthomclExtractProteinPairsFromGroupsFile groups.txt > pairs.txt", shell=True)
				print("Klaar met pairs. Running Singletons...")
			if os.path.exists(args.input+"/singletons.txt"):
				print("singletons.txt already exists")
			else:
				subprocess.call("orthomclSingletons goodProteins.fasta groups.txt > singletons.txt", shell=True)
				print("Klaar met singletons. Running SortGroupsFile...")
			if os.path.exists(args.input+"/groups_sorted.txt"):
				print("groups_sorted.txt already exists")
			else:
				subprocess.call("orthomclSortGroupsFile groups.txt | sort  > groups_sorted.txt", shell=True)
				print("Klaar met sorteren. Running SortGroupMembersByScore...")
			if os.path.exists(args.input+"/sortedGroupsMembersandScore.txt"):
				print("sortedGroupsMembersandScore.txt already exists")
			else:
				subprocess.call("orthomclSortGroupMembersByScore groups_sorted.txt pairs > sortedGroupsMembersandScore.txt", shell=True)
				print("Klaar met sorteren per score. Running Analyze_groups...")
			if os.path.exists(args.input+"/groups_count.txt"):
				print("groups_count.txt already exists")
			else:				
				os.chdir(cur)
				subprocess.call("python Analyze_groups.py -i "+args.input+"/groups.txt > groups_count.txt", shell=True)
				print("Klaar met Analyze_groups.")
				if args.core_cluster == "ask":
					Voortgaan = input("Create alignment file for each cluster? 1/0 ")
					if Voortgaan == 1:
						subprocess.call("python coreGene_clusters.py -f "+args.input+" -i groups.txt", shell=True)
						print("Klaar met coreGene_clusters. Run identity_mean?")
					else:
						print("Continue with identity_mean?")
				elif args.core_cluster == "yes":
					subprocess.call("python coreGene_clusters.py -f "+args.input+" -i groups.txt", shell=True)
					print("Klaar met coreGene_clusters. Run identity_mean?")
				else:
					print("Finished")
				if args.mean_identity == "ask":				
					Confirmation = input("Run identity_mean? 1/0")
					if Confirmation == 1:
						subprocess.call("python identity_mean.py -i "args.input, shell = True)
						print("Klaar met identity_mean.")
					else:
						print("Helemaal klaar.")
				elif args.mean_identity == "yes":
					subprocess.call("python identity_mean.py -i "args.input, shell = True)
					print("Helemaal klaar.")
				else:
					print("Helemaal klaar.")
		else:		
			subprocess.call("orthomclBlastParser all-vs-all.tsv compliantFasta > similarSequences.txt", shell = True)
			print("Klaar met BlastParser. Running LoadBlast...")
		
			subprocess.call("orthomclLoadBlast orthomcl.config similarSequences.txt", shell=True)
			print("Klaar met LoadBlast. Running Pairs...")
		
			subprocess.call("orthomclPairs orthomcl.config log_file cleanup=yes", shell=True)
			print("Klaar met Pairs. Running DumpPairsFiles...")

			subprocess.call("orthomclDumpPairsFiles orthomcl.config", shell=True)
			print("Klaar met DumpPairsFiles. Running mcl...")

			subprocess.call("mcl mclInput --abc -I 1.5 -o mclOutput", shell=True)
			print("Klaar met mcl. Running MclToGroups...")

			subprocess.call("orthomclMclToGroups my_prefix 1000 < mclOutput > groups.txt", shell=True)
			print("Klaar MclTogroups. Running ExtractProteinIdsFromGroupsFile...")

			subprocess.call("orthomclExtractProteinIdsFromGroupsFile groups.txt > protIds.txt", shell=True)
			print("Klaar met protIds. Running ExtractProteinPairsFromGroupsFile...")

			subprocess.call("orthomclExtractProteinPairsFromGroupsFile groups.txt > pairs.txt", shell=True)
			print("Klaar met pairs. Running Singletons...")

			subprocess.call("orthomclSingletons goodProteins.fasta groups.txt > singletons.txt", shell=True)
			print("Klaar met singletons. Running SortGroupsFile...")

			subprocess.call("orthomclSortGroupsFile groups.txt | sort  > groups_sorted.txt", shell=True)
			print("Klaar met sorteren. Running SortGroupMembersByScore...")

			subprocess.call("orthomclSortGroupMembersByScore groups_sorted.txt pairs > sortedGroupsMembersandScore.txt", shell=True)
			print("Klaar met sorteren per score. Running Analyze_groups...")

		
			os.chdir(cur)
			subprocess.call("python Analyze_groups.py -i "+args.input > groups_count.txt", shell=True)
			print("Klaar met Analyze_groups. Running coreGene_clusters...")
			if args.core_cluster == "ask":
				Voortgaan = input("Create alignment file for each cluster? 1/0 ")
				if Voortgaan == 1:
					subprocess.call("python coreGene_clusters.py -f "+args.input+" -i groups.txt", shell=True)
					print("Klaar met coreGene_clusters. Run identity_mean?")
				else:
					print("Continue with identity_mean?")
			elif args.core_cluster == "yes":
				subprocess.call("python coreGene_clusters.py -f "+args.input+" -i groups.txt", shell=True)
				print("Klaar met coreGene_clusters. Run identity_mean?")
			else:
				print("Finished")
			if args.mean_identity == "ask":				
				Confirmation = input("Run identity_mean? 1/0")
				if Confirmation == 1:
					subprocess.call("python identity_mean.py -i "args.input, shell = True)
					print("Klaar met identity_mean.")
				else:
					print("Helemaal klaar.")
			elif args.mean_identity == "yes":
				subprocess.call("python identity_mean.py -i "args.input, shell = True)
				print("Helemaal klaar.")
			else:
				print("Helemaal klaar.")

if __name__ == "__main__":
    main()
