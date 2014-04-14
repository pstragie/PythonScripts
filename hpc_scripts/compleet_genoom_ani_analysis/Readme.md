ANI analysis walkthrough
For complete and/or draft genomes
12-3-2013 bart.verheyde@ugent.be v0.3
12-02-2014 pieter.stragier@ugent.be v0.4

Step by step manual

used syntax and meaning
$> Signifies command line commands
#> Signifies command line commands as root
! Attention point
!!! Very important, no way around it
f= result files
= result of the step

PREP (1h without download time)
1) Get genomes
!!! Do this step on your PC, due to the 1 hour time limit on login node and size limit

All known bacteria are loaded from NCBI
! Choose your target directory in 
download_complete_genomes.sh and/or download_draft_genomes.sh

For full genomes
$> download_compleet_genomes.sh
For draft genomes (per family) do once per family
! Choose your bacteria family in download_draft_genomes.sh
$>download_draft_genomes.sh

= Results in dir filled up /genomes/bacteria/complete/*
  Results in dir filled up /genomes/bacteria/draft/*
f= acc.txt a file with .gbk accession nrs 
of format: NC_015674	/home/baverhey/genomes/bacteria/complete/Helicobacter_bizzozeronii_CIII_1_uid68141/NC_015674.gbk

2) Copy the directories of the genome files to your space on the server (hpc)
! Keep the directory structure 

3) Generate full sequence list of all the bacteria you want to use.
There are 2 strategies, pick 1.
First strategy:
Remove all the bacteria from complete genomes you don't want to use.
This saves space on the cluster.
Downside: if you change your mind later on, you have to redo the download and the work of course.
Upside: visually clear and easy to do

Second strategy:
Leave everything in place and modify the full .acc file to the bacteria/dir you wan to use

! First part is path to directory of your genome files, second argument is reg expression to
generate full sequence list 
! best is to use full path, you can use comand $>pwd
$> create_sequence_list '/home/baverhey/genomes/bacteria' '*/*' > acc_full_list.txt
$> ./create_sequence_list '/user/home/gent/vsc406/vsc40682/data/genomes/bacteria' '*/*' > ~/mummer/mummer_cupriavidus_ralstonia/acc_full_list.txt


Other possibilities:
Drafts only
create_sequence_list '/home/baverhey/genomes/bacteria' 'draft/*'> acc_drafts_only_list.txt

= file with 2 columns, first column bacteria name, second column with the path to the directory
f= acc_full_list.txt format: Ralstonia_solanacearum_UW551_uid54307 /home/baverhey/genomes/bacteria/draft/Ralstonia_solanacearum_UW551_uid54307

4) Generete acc file of interest whit the bacteria of your interest.
The larger the file the longer the time
There are 2 strategies, pick 1
Strategy1: Manual editing the file
!be aware of syntax errors, error prone.

Strategy2:use grep repeat this line for all interested bacteria families
grep <insert interested bacteria * > acc_full_list.txt >>acc_intrest_list.txt
all matching lines are added to interest_list 
$>grep Ralstonia* acc_full_list.txt >>acc_intrest_list.txt
$>grep Cupriavi* ~/mummer/mummer_cupriavidus_ralstonia/acc_full_list.txt >> ~/mummer/mummer_cupriavidus_ralstonia/acc_interest_list.txt 
$>grep Burkhold* ~/mummer/mummer_cupriavidus_ralstonia/acc_full_list.txt >> ~/mummer/mummer_cupriavidus_ralstonia/acc_intrest_list.txt 



5) Check your file this is your starting point.
! Create label list easier to work with bacteria codes instead off full names
! Also prevents problem for some programs of too long names
$>create_lable_list_dir ~/mummer/mummer_cupriavidus_ralstonia/acc_interest_list.txt  

f=acc_interest_list.txt.input /input file to be used with labels
f=acc_interest_list.txt.label /legends of the labels


RUN
6) Start the ani analysis
Normally Not necessary //Modify settings in  compute_combined_ANI.sh pool_size
! make sure the $PATH variable contains the folder where the scrips are located
! you can add this script path to $PATH in .bash_profile file in your root of hpc PATH=~/scripts:$PATH
Modify default_start_htc_ani_project with your own parameters if necessary
$> default_start_htc_ani_project
	Change cluster Best to use raichu (default action)
	Make the cluster jobs and submit them.
	compute_combined_ANI.sh <input_files> <tmp_dir> <project_name_short 4_no_spaces> <output_file_with_previus_results if available>


@todo nog aanpassen en testen voor hpc
$> compute_combined_ANI.sh acc_intrest_list.txt ~/ani_tmp
$> compute_combined_ANI.sh ~/project_ani/ani_cupriavidus_ralstonia/compleet_only/acc_intrest_list.txt.input ~/scratch/project_ani/ani_cupriavidus_ralstonia/complete_only ani_cup_ral_complete_only 



7) Check when all jobs are done
$>qstat
empty results == is no planned or running jobs
Standard settings give you start and stop emails per job

Post processing
8) Quality test
in result directory
$>cat *.err result must be empty but 
"tput: No value for $TERM and no -T specified" is allowed


$>cat *.out result must be empty

! errors sometimes happen
When you found an error, find file
$>grep  " error message" /*.out of /*.err
Rerun the Job file qsub MUM000xx.sh

9) Make Complete result set
$>cat *.txt >complete_result_ANI_project_name.output
f=complete_result_mumi.output 
with format:Burkholderia_383_uid58073	Burkholderia_ambifaria_AMMD_uid58303	8676277	7484986	0.394000	0.392027

10) Make similarity matrix to make tree

List2matrix options_inverse  start_accficdle resultfile_mummer column number multiply_factor
! Important python version 3.2
module load Python/3.2.3-ictce-4.0.6

!# -i gives inverted matrix necessary for result of ani
For import in bionumerics7 -b flag
$> python3.2 ~/scripts/list2matrix.py -i -b acc_intrest_list.txt complete_result_mumi_complete_only.output 6 1 > matrix_compleet_only_6_100.dist.txt
!# -i gives inverted matrix necessary for result of ani
python3.2 ~/scripts/list2matrix.py -f -D 0 -i 1 acc_intrest_list.txt ani_cupriavidus_ralstonia_compleet_and_draft0000001.txt 10 0.01 > ani_cupriavidus_ralstonia_compleet_and_draft_10_001_inverse.dist


Optional if labels are to long: relabel file
$>relable_file.py -f 0 complete_result_mumi_complete_only.output acc_interest_list.txt.input 1 3


11) Make tree
With program of your choice

For some programs the keys will be to long:
substitute keys with the files from step 5
You can do this from the beginning or in the beginning of step 10
$>relable_file.py -f 1  matrix_complete_only5_100.dist acc_interest_list.txt.input 1 3 > matrix_compleet_only5_100.dist.relabeled

or you can do this in step 10

0)Fast result through website (manual work)
$>wc -l < matrix_renamed10_001_inverse.dist
! Full matrix necessary with diagonal and line numbers at the top -n option
!# -i gives inverted matrix necessary for result of ani
python3.2 ~/scripts/list2matrix.py -f -n -D 0 -i 1 acc_intrest_list.txt ani_cupriavidus_ralstonia_compleet_and_draft0000001.txt 10 0.01 > ani_cupriavidus_ralstonia_compleet_and_draft_10_001_inverse.dist


Matrix to Newick Tree
http://www.trex.uqam.ca/index.php?action=matrixToNewick&project=trex
Tree viewer
http://www.trex.uqam.ca/index.php?action=newick&project=trex

A) Bionumerics
! for bionumerics 7 the matrix must have 100 at the end of every line the diagonal
notepad ++ Find replace \n with \t100\n
@To DO: python script for adding 100 at the end of every line

Create new empty local DB
File -> install /remove plug-ins
Enable the following plug-ins/utilities in BN7:
 * Import
 * Dendrogram tools
 * Databasetools
>Right top box
Create new experiment of type matrix
File-> import (upper left corner)
Import matrix file (not to long key names) , Select matrix, select experiment type
select all entries
right bottom create new comparison
clustering->calculate->clustering analysis
*UPGMA
*neighborhood joining
reroot tree if necessary
! the distance matrix get recomputed in another order, same result?? 

B) PHYLIP @todo
Optional if labels are to long: relabel file
$>relable_file.py -f 0 complete_result_mumi_complete_only.output acc_interest_list.txt.input 1 3 >matrix_renamed.dist
wc -l < matrix_renamed.dist > matrix_renamed.dist_phylib
to_phylip_matrix.sh matrix_renamed.dist >> matrix_renamed.dist_phylib

phylip neighbor matrix_file.for strict fhylip max 10 characters for the name, so relabeling is necessary
To go from list result to correct matrix

python3.2 ~/scripts/list2matrix.py -f -D 0 -i 1 acc_intrest_list.txt ani_cupriavidus_ralstonia_compleet_and_draft0000001.txt 10 0.01 > ani_cupriavidus_ralstonia_compleet_and_draft_10_001_inverse.dist
relable_file.py -f 0 ani_cupriavidus_ralstonia_compleet_and_draft_10_001_inverse.dist acc_intrest_list.txt.input 1 3 >matrix_renamed10_001_inverse.dist
wc -l < matrix_renamed10_001_inverse.dist > matrix_renamed10_001_inverse.dist_phylib
to_phylip_matrix.sh matrix_renamed10_001_inverse.dist >> matrix_renamed10_001_inverse.dist_phylib

Phylip neighbor
>



ani_cupriavidus_ralstonia_compleet_and_draft_10_1.dist


C)MEGA5 @todo

D) via website seems not reliable, very strange result,  be careful
! use copy add line numbers on first line
!select root of tree row number

$> wc -l < matrix_renamed10_001_inverse.dist
! Full matrix necessary with diagonal and line numbers at the top
Matrix to Newick Tree
http://www.trex.uqam.ca/index.php?action=matrixToNewick&project=trex
Tree viewer
http://www.trex.uqam.ca/index.php?action=newick&project=trex

E) python
http://pythonhosted.org/DendroPy/downloading.html

sudo pip install dendropy
d
F) Dendroscope @todo


Done
