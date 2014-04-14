#!/bin/bash -x
#
# 15-7-2013 bart.verheyde@ugent.be V0.5
# computes ANI for list of input files, where each input file is an individual GenBank
# file or a directory containing GenBank files. If an input file is a directory, then all
# GenBank files from that directory are combined into a single file before processing.
#
# usage: compute_combined_ANI.sh <input_files> <tmp_dir> <project_name_short 4_no_spaces> <previus_output_file_not_nessesairy>

# define helper variables
input_files="$1"
#org tmp_dir="/home/pdawyndt/projects/genomic_distance/ani_tmp"
tmp_dir="$2"
project_name="$3" #no spaces aloud @todo insert c
output_file="$4"

#@todo bring settings variable pool to this section make parameter ?
#varaible pool can be changed to lower when job is to large
# job size target is +- 10hours in short queue +-2 hours buffer

#15' voor 75 ani.sh calculations
#pool_size=3000 #aming at 10hours if it is linear probbebly not
pool_size=1000 

######################################################################################
# NO changes lower than here!!!  (unless you know what your doing)
######################################################################################
#@todo insert chek for no spaces in project name replace with _ or good error output 2>
#@todo insert chek for input file exist good error 2>


# set default values
if [ -z ${project_name} ]
then
  project_name="PROJECT_ANI"
fi

if [ -z ${tmp_dir} ]
then
  tmp_dir="ani_tmp"
fi

#make shure directory is empty otherwise output file gets appended remove if exists
if [ -d "${tmp_dir}" ]; then
  rm -rf ${tmp_dir}
fi



# create temporary directory
mkdir -p ${tmp_dir}


# compute ANI for each pair of input files (each input is directory or individual file)
awk -v output_file=${output_file} -v tmp_dir=${tmp_dir} -v project_name=${project_name} -v pool_size=${pool_size} '
BEGIN {

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

      # compute ANI between seq1 and seq2 if not previously computed
      if (!((seqname[i] SUBSEP seqname[j]) in computed) && !((seqname[j] SUBSEP seqname[i]) in computed)) {
        if ((pool_size == 1) || (((++computation) % pool_size) == 1)) {
          # close and execute previous job (if needed)
          if (job > 0) {
            close(jobscript(job))
            command = sprintf("qsub %s",jobscript(job)); system(command);
	    #Removes job script, cleanup comment for debug
#	    system(sprintf("rm %s",jobscript(job)));
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
#     system(sprintf("rm %s",jobscript(job)));
  }
}

# construct job name
function jobname(job,    name) {
  name = sprintf("%d",job)
  while (length(name)<7) name=sprintf("0%s",name)
  name = sprintf("%s%s",project_name,name)
  return name
}

# construct name of the job script
function jobscript(job) { return sprintf("%s/%s.sh",tmp_dir,jobname(job)); }

# construct name of the job script
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
#  script = sprintf("%s#$ -cwd\n",script)
#  script = sprintf("%s#$ -q mpi.q\n",script)
  return script
}


# generate  header for the job script in hpc envirement
function jobheader_hpc(job,   script) {
  script = sprintf("#!/bin/bash\n") #for normal functioning
#  script = sprintf("#!/bin/bash   -x\n") #for debug
  script = sprintf("%s#PBS -N %s\n",script,jobname(job))
  script = sprintf("%s#PBS -S /bin/bash\n",script)
  script = sprintf("%s#PBS -o %s/%s.out\n",script,tmp_dir,jobname(job))
  script = sprintf("%s#PBS -e %s/%s.err\n",script,tmp_dir,jobname(job))
  script = sprintf("%s#PBS -m abe\n",script) #send mail
  script = sprintf("%s#PBS -l %s\n",script,"nodes=1:ppn=1,walltime=11:59:00") #run parameters cores nodes walltime under 12 hours is short que target is 10 hours 2 hours buffer
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
#Gengar  modules_to_load = sprintf("%s module load BLAST/2.2.22-x64-linux\n",modules_to_load) #load moule withoud options
#Raichu
  modules_to_load = sprintf("%s module load BLAST/2.2.28-ictce-4.1.13\n",modules_to_load) #load module withoud options
  #problems#modules_to_load = sprintf("%s module load EMBOSS/6.5.7-ictce-4.1.13\n",modules_to_load) #load module withoud options
  #new version
  modules_to_load = sprintf("%s module load EMBOSS/6.5.7-ictce-4.1.13-no-pq\n",modules_to_load) #load module withoud options

  return modules_to_load
}


# generate command for the job script
function jobcommand(job,seq1,seq2) {
  return sprintf("ani.sh -t %s -p %s %s %s >> %s\n",tmp_dir,jobname(job),seq1,seq2,joboutput(job))
}
' ${input_files}
