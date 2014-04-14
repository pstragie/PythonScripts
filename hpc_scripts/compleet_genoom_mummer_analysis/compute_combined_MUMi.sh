#!/bin/bash
#
# 6-2-2013 bart.verheyde@ugent.be V0.3
# computes MUM-index for list of input files, where each input file is an individual GenBank
# file or a directory containing GenBank files. If an input file is a directory, then all
# GenBank files from that directory are combined into a single file before processing.
#
# usage: compute_combined_MUMi.sh <input_files> <tmp_dir> <project_name_short 4_no_spaces> <output_file>

# define helper variables
input_files="$1"
#org tmp_dir="/home/pdawyndt/projects/genomic_distance/mumi_tmp"
tmp_dir="$2"
project_name="$3"
output_file="$4"

#@todo bring settings variable pool to this section
#varaible pool can be changed to lower when job is to large
# job size target is +- 6hours in short que
# Default pool= 300 a 360 bring variable to here

######################################################################################
# NO changes lower than here!!!  (unless you know what your doing)
######################################################################################
# set default values
if [ -z ${project_name} ]
then
  project_name="PROJECT_MUMi"
fi

if [ -z ${tmp_dir} ]
then
  tmp_dir="mumi_tmp"
fi

# create temporary directory
mkdir -p ${tmp_dir}

# compute MUM-index for each pair of input files (each input is directory or individual file)
gawk -v output_file=${output_file} -v tmp_dir=${tmp_dir} -v project_name=${project_name} '
BEGIN {
  # set number of pooled MUM-index computations gem 2 minutes per job
  pool=300

  if (length(output_file) == 0) {
	  printf("reading previously computed values not nessesary\n")	
  }
  else {
	  # read previously processed calculations
	  printf("reading previously computed values...\n")
	  while ( (getline < output_file) > 0 ) { 
	    computed[$1,$2]=1
	  }
  }
}

# read list of sequence names and file locations
{ 
  seqname[++seqs]=$1 
  seqfile[$1]=$2
}

END {
  printf("submitting new computation jobs on cluster...\n")
  for(i=1;i<seqs;++i) {
    seq1=seqfile[seqname[i]]
    for(j=i+1;j<=seqs;++j) {
      seq2=seqfile[seqname[j]]

      # compute MUM-index between seq1 and seq2 if not previously computed
      if (!((seqname[i] SUBSEP seqname[j]) in computed) && !((seqname[j] SUBSEP seqname[i]) in computed)) {
        if ((pool == 1) || (((++computation) % pool) == 1)) {
          # close and execute previous job (if needed)
          if (job > 0) {
            close(jobscript(job))
            command = sprintf("qsub %s",jobscript(job)); system(command);
	    #Removes job script, cleanup comment for debug
	    system(sprintf("rm %s",jobscript(job)));
          }
          # create new job script with header
          ++job; printf("%s",jobheader(job)) > jobscript(job)
        }
        # add command to job script
        printf("%s",jobcommand(job,seq1,seq2)) >> jobscript(job);
      }
      else {
        printf("[%s,%s] already computed\n",seqname[i],seqname[j]);
      }
    }
  }
  # close and execute previous job (if needed)
  if (job > 0) {
     close(jobscript(job))
     command = sprintf("qsub %s",jobscript(job)); system(command);
     #Removes job script, cleanup comment for debug
     system(sprintf("rm %s",jobscript(job)));
  }
}

# construct job name
function jobname(job,    name) {
  name = sprintf("%d",job)
  while (length(name)<7) name=sprintf("0%s",name)
  name = sprintf("%s%s",project_name,name)
  #name = sprintf("MUM%s",name)
  return name
}

# construct name of the job script
function jobscript(job) { return sprintf("%s/%s.sh",tmp_dir,jobname(job)); }

# construct name of the job output
function joboutput(job) { return sprintf("%s/%s.txt",tmp_dir,jobname(job)); }

# generate  header for the job script
function jobheader(job,   script) {
	#added for hpc computing
	script = jobheader_hpc(job,   script)

#  script = sprintf("#!/bin/bash\n")
#  script = sprintf("%s#$ -N %s\n",script,jobname(job))
#  script = sprintf("%s#$ -S /bin/bash\n",script)
#  script = sprintf("%s#$ -o %s/%s.out\n",script,tmp_dir,jobname(job))
#  script = sprintf("%s#$ -e %s/%s.err\n",script,tmp_dir,jobname(job))
#  script = sprintf("%s#$ -m abe\n,script") #send mail 
#  script = sprintf("%s#$ -cwd\n",script)
##  script = sprintf("%s#$ -q mpi.q\n",script)
  return script
}

# generate  header for the job script in hpc envirement
function jobheader_hpc(job,   script) {
  script = sprintf("#!/bin/bash\n")
  script = sprintf("%s#PBS -N %s\n",script,jobname(job))
  script = sprintf("%s#PBS -S /bin/bash\n",script)
  script = sprintf("%s#PBS -o %s/%s.out\n",script,tmp_dir,jobname(job))
  script = sprintf("%s#PBS -e %s/%s.err\n",script,tmp_dir,jobname(job))
  script = sprintf("%s#PBS -m abe\n",script) #send mail
  script = sprintf("%s#PBS -l %s\n",script,"nodes=1:ppn=1,walltime=8:00:00") #run parameters cores nodes walltime under 12 hours is short que target is 6 hours 2 hours buffer
  script = sprintf("%s#PBS -q %s\n",script,"short") #add to specific queue short, long, short , debug
#  script = sprintf("%s#PBS -l %s\n","vmem=1gb") #set RAM memory limit
#  script = sprintf("%s# -cwd\n",script)
#  script = sprintf("%s#PBS -q mpi.q\n",script)

#add modules needed for hpc

  script = sprintf("%s%s\n",script,load_modules_hpc()) #add modules to load

  return script
}

# load envirement modules hpc for the job script
function load_modules_hpc() {

  modules_to_load=""
#  modules_to_load = sprintf("%s module load BLAST/2.2.22-x64-linux\n",modules_to_load) #load moule withoud options
  return modules_to_load
}



# generate command for the job script
function jobcommand(job,seq1,seq2) {
  return sprintf("mummer_combined.sh %s %s %s %s>> %s\n",seq1,seq2,jobname(job),tmp_dir,joboutput(job))
}' ${input_files}

#Voorbereiding
# eventuele update locale bestanden van genomen
#download_complete_genomes.sh
#download_draft_genomes.sh
#
#Genereer volledige inventaris acc file
# create_sequence_list <regex>
# create_sequence_list 'compleet/*'
# create_sequence_list '*/*'
#
# generatie short acc file de bactereien van intrest
#Format = "bacterienaam	/directory van root naar locatie van genbank file
#Burkholderia_383_uid58073	/home/pdawyndt/genomes/bacteria/complete/Burkholderia_383_uid58073


#Run this file
#usage: compute_combined_MUMi.sh <input_files> <output_file>
#usage: compute_combined_MUMi.sh short_acc file <prefius results if available>

#Na uitvoeren 
#testen alles goed verlopen?
#cat *.err moet leeg zijn
#cat *.out moet leeg zijn
#
#	Indien .out of error niet leeg is zoek blok op via 
#grep " foutbootschap" /*.out of /*.err
#	Terug laten lopen via$ qsub MUM000xx.sh
#
#alle resultaten samenvoegen
#cat *.txt >compleet_result_mumi.output
#
# List2matrix start accfile resultfile_mummer kolomnrgeg factor
# list2matrix.sh Bart_rerun/burkholderia+CH34+SAR1_acc_mummer.input.txt Bart_rerun/MUM0000all.output 6 100 > Bart_rerun/Mummer_matrix_6_100.dist

#Methode 2: Boom maken
#Boom maken via simularity distance matrix via bionumerics
# Matrix moet tab gescheiden zijn en geen aantal stammen van boven
#Volgende stappen zijn voor in bionumerics
#A) procedure to import a matrix
#1)Create new database (in startupscreen)
#2)Locale database
#3)Enable Import plugin and dendogram tools plugin
#4)Create matrix experiment type
#5)Menu Experiments -> create new matrix type... -> choose custum type name
#6)Menu Scripts -> import matrix
#7)Double click rigt of the screen in the FILES window on your chosen matrix type name
#  Opens new window For a visuel cheq of the matrix values
#
#B)Procedure to create a tree
#1)Select the relevant key's in key colum (use space bar) selected shows an arrow in front
#3)Menu Comparison -> create new comparison
#4) In comparison window ->Clustering -> Calculate -> cluster analysis
#5) In comparison window -> Choose tree type UPGMA (or other)
#6) Print priview of your tree


#Methode 1: Boom maken
#Matrix is bijna in streng phylib formaat moet spatie gescheiden zijn denk ik en namen mogen niet te lang 10 tekens
#Dus sed 's:\t: :g'	//tabs zijn vervangen door spatie
#label file maken 
# create_lable_list_dir Bart_rerun/combined_mummer/burkholderia+CH34+SAR1_acc_mummer.input.txt
#
#relable file 
#relabel_file.sh Bart_rerun/combined_mummer/Mummer_matrix_5_1_spatie.dist Bart_rerun/combined_mummer/burkholderia+CH34+SAR1_acc_mummer.input.txt.input 1 3	//kolom 1 wordt kolom 3
#
#Matrix nog niet in orde 
#bacterienamen/ codes mogen maximum 10 tekens lang zijn gevolgd door spatie
# to_phylip_matrix.sh Mummer_matrix_6_1_spatie_code.dist > Mummer_matrix_6_1_spatie_code_phylib.dist 
#
#eerste lijn moet nog 5 spaties worden gevolgd door aantal stammen dus aantal lijnen
#wc filename  eerste getal geeft aantal lijnen manueel toeveogen op eerste lijn

#Boom maken van matrix via phylib
# maken dat active pad directory is waar de documenten staan testen met pwd
# phylip fitch   <enter>
# L <enter>

#output file en tree file is result
#showable with online newick tree tool

#relable file, undo the previus relabeling
#relabel_file.sh Bart_rerun/combined_mummer/outtree_mummer_6_1_code Bart_rerun/combined_mummer/burkholderia+CH34+SAR1_acc_mummer.input.txt.input 3 1 >outtree_mummer_6_1.tree








#Resultaten in matrix steken om boom van te maken
# list2matrix.sh  <accfile> <listfile> <factor>
