#!/bin/bash
#PBS -N Start_ANIBLASTDef00
#PBS -S /bin/bash
#PBS -m abe
#PBS -l nodes=1:ppn=1,walltime=0:59:00
#PBS -q debug

# No modules needed for Start_htc_ani_project job

## 15-6-2013 bart.verheyde@ugent.be v0.8
## 13-2-2014 pieter.stragier@ugent.be v0.9
## This files contains all the steps to guide you to the right cluster
## and setting the envirement
## Read carefully and you should be fine
##


#@todo make this in arguments/ioptions when done
#############################################################################################
###  Variables   ###
#############################################################################################
##tips use as mutch the folowing varibles helps portability an prevend path problems
##$VSC_HOME: user home directory	3GB Default (For the scripts and results depending on size)
##$VSC_DATA: user data directory	25GB Default (For the Dataset)
##$VSC_SCRATCH: user scratch directory	25GB Default ( For all tmp and intermidair steps)
##$VSC_SCRATCH_NODE: local (on blade) scratch directory 85GB shared ( For all tmp and intermediairy steps when staying on the node)

##Show quota's
show_quota.py


project_name=Pediococcus

input_files=$VSC_HOME/ani_analysis_pieter/complete_genome_ani_analysis/$project_name/acc_interest_list.txt.input
tmp_dir=$VSC_SCRATCH/project_ani/$project_name/tmp


if [ -f "$input_files" ]; then
  echo "Input file exists"
else
  echo "Dont forget to modify all the variables!! --> Aborted"
  exit 0;
fi




###########################################################################################################
## NO CHANGES behind this line (unless you know what you are doing)
###########################################################################################################
## Init default basic envirement, Default needed modules
##	load jobs module "keep this"
module load jobs
module load scripts

#############################################################################################
###  Cluster switching ###
#############################################################################################
## choose cluster
## on basis of load of clusters
## see http://tropius.ugent.be/pbsmon2php/pbs_mon_json.php
## on basis of specs of cluster
## see http://hpc.ugent.be/userwiki/index.php/Main_Page -> Hardware 
## see list of available clusters
## command
module av cluster

## website :see http://hpc.ugent.be/userwiki/index.php/User:VscClusters
#!!!Pick only 1 swap current out for the one you want
module swap cluster/raichu 

#module swap cluster/raichu				#(Jobs that stay on 1 node or even 1 core, LOW network load) NEWEST
#module swap cluster/haunter				#(Jobs that stay on 1 node or even 1 core, LOW network load)
#module swap cluster/gulpin				#(NUMA architecture, other scripting)
#module swap cluster/gastly				#(Jobs that stay on 1 node or even 1 core, LOW network load)
#module swap cluster/dugterio				#(NUMA architecture, other scripting)
#module swap cluster/gengar				#(Large IO, large network load, large multi node jobs!= threads)

#see cluster and load
pbsmon


############################################################
###  load nessesary modules dependant of cluster and Job ###
############################################################

# On cluster most correct list
#module av 2>av_modules.txt
#see http://hpc.ugent.be/userwiki/index.php/Admin:SoftwareInst

##show list currently loaded modules including cluster
module list



#############################################################################################
###  Cleanup previus directorys and make new ones if nessesairy and not done by the script###
#############################################################################################
##available variables on HPC use this as mutch as possible as arguments, improves portabillity
#http://hpc.ugent.be/userwiki/index.php/User:StorageDetails
#    $VSC_HOME: user home directory
#    $VSC_DATA: user data directory
#    $VSC_SCRATCH: user scratch directory
#    $VSC_SCRATCH_NODE: local (on blade) scratch directory
#    if you are member of a VO
#        $VO_DATA: data directory of your VO
#        $VO_SCRATCH: scratch directory of your VO 


##Make tmp directory dont forget to remove
#mkdir -p $VSC_SCRATCH/cgi-project
#mkdir -p $VSC_HOME/CGI_project/cgi_tmp_20121019 # contains db result filter result from twigrid

##Clean previus attempt
#rm $VSC_SCRATCH/cgi-project/CBLAST*.sh
#rm $VSC_SCRATCH/cgi-project/CBLAST*.out
#rm $VSC_SCRATCH/cgi-project/CBLAST*.err
#cp -r $VSC_HOME/CGI_project/cgi_tmp_20121019/* $VSC_SCRATCH/cgi-project


#####################################################
###Script to run on cluster witch creates the jobs###
#####################################################

#compute_conserved_genes.sh <input_files> <project_name> <tmp_dir> <orthomcl_config> 
#compute_combined_ANI.sh <input_files> <tmp_dir> <project_name_short 4_no_spaces> <previus_output_file_not_nessesairy>
compute_combined_ANI.sh $input_files $tmp_dir $project_name


#####################################################
###Start post processing JOB with dependensys of privus list
#####################################################
# are written to .out 
# get job numbers with awk or grep waiting job to start if all previus wones are done
#process results


##genernal info about queues
##– short: walltime less than 12h
##– long: walltime more than 12h, less than 72h
##– debug: walltime less than 1h
##• useful for debugging scripts (sanity check)
##• a few workernodes are dedicated to this queue
##– bshort: backfll queue for short jobs
##• not counted in fair share
##• use this for non-urgent jobs that require less than 12h
##– see show_queues command for overview

##see show_queues command for overview
#show_queues
