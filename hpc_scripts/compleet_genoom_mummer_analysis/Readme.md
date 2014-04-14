Mummer analysis walk through
For complete or draft genomes
15-2-2013 bart.verheyde@ugent.be v0.5

Step by step manual

used syntax and Meaning
$>Signifies command line commands
#>Signifies command line commands as root
! Attention point
!!! Very important, no way around it
f= result files
= result of the step

PREP (1h without download time)
1)Get genomes
!!! Do this step on your PC, due to the 1 hour time limit on login node and size limit

All know bacteria are loaded from NCBI
!Choose your target directory in 
download_complete_genomes.sh and/or download_draft_genomes.sh

For full genomes
$>download_compleet_genomes.sh
For drafts genomes (per family) do once per family
!Choose your bacteria family in download_draft_genomes.sh
$>download_draft_genomes.sh

= Results in dir filled up /genomes/bacteria/compleet/*
  Results in dir fileld up /genomes/bacteria/draft/*
f= acc.txt a fille with .gbk accession nrs 
of format: NC_015674	/home/baverhey/genomes/bacteria/complete/Helicobacter_bizzozeronii_CIII_1_uid68141/NC_015674.gbk

2)Copy the directorys of the genoom files you to your space on the server (hpc)
! Keep the Directory structure 

3)Generate full sequence list of all the bacteria you want to use
There are 2 strategies, pick 1
first strategy:
remove all the bacteria from copmlete genoom you dont want to use,
This saves space on te cluster.
Downsite: if you change your mind later on, you have to redownload and the work ofcource.
Upsite: visualy clear and easy to do

Second strategy:
Leave every thing in place and modify the full acc file to the bacteria/dir you wan to use

! first part is path to directory of your genome files second argument is reg expresion
generate full sequence list 
! best is to use full path, you can use comand $>pwd
$> create_sequence_list '/home/baverhey/genomes/bacteria' '*/*' > acc_full_list.txt
$> ./create_sequence_list '/user/home/gent/vsc406/vsc40682/data/genomes/bacteria' '*/*' > ~/mummer/mummer_cupriavidus_ralstonia/acc_full_list.txt


Other posibilitys:
Drafts only
create_sequence_list '/home/baverhey/genomes/bacteria' 'draft/*'> acc_drafts_only_list.txt

= file with 2 colums, first colum bacteria name, secodn colum with the pad to tthe directory
f= acc_full_list.txt format: Ralstonia_solanacearum_UW551_uid54307 /home/baverhey/genomes/bacteria/draft/Ralstonia_solanacearum_UW551_uid54307

4)Generete acc file of intrest whit the bacteria of your intrest.
The langer the file the longer the time
There are 2 strategies, pick 1
Strategy1: Manual editing the file
!be aware of syntax errors, error prone.

Strategy2:use grep repeat this line for all intrested bacteria families
grep <insert intrested bacteria * > acc_full_list.txt >>acc_intrest_list.txt
all matching lines are addes to intrest_list 
$>grep Ralstonia* acc_full_list.txt >>acc_intrest_list.txt
$>grep Cupriavi* ~/mummer/mummer_cupriavidus_ralstonia/acc_full_list.txt >> ~/mummer/mummer_cupriavidus_ralstonia/acc_intrest_list.txt 
$>grep Burkhold* ~/mummer/mummer_cupriavidus_ralstonia/acc_full_list.txt >> ~/mummer/mummer_cupriavidus_ralstonia/acc_intrest_list.txt 



5) Check your file this is your starting point.
!Create label list easer to work ith bateria codes insted off full names
!Also prevens problem for some programs of to long names
$>create_lable_list_dir ~/mummer/mummer_cupriavidus_ralstonia/acc_intrest_list.txt  

f=acc_intrest_list.txt.input /input file to be used with labels
f=acc_intrest_list.txt.label /legends of the labels


RUN
6)Start the mummer analysis
Modify settings in  compute_combined_MUMi.sh
! make sure the $PATH variable contains the folder where the scrips are located
! you can add this script path to $PATH in .bash_profile file in your root of hpc PATH=~/scripts:$PATH
Make the cluster jobs and submit them.
ompute_combined_MUMi.sh <input_files> <tmp_dir> <project_name_short 4_no_spaces> <output_file_with_previus_results if availible>

@todo nog aanpassen en testen voor hpc
$>compute_combined_MUMi.sh acc_intrest_list.txt ~/mumi_tmp
$>compute_combined_MUMi.sh ~/mummer/mummer_cupriavidus_ralstonia/acc_intrest_list.txt ~/scratch/mummer/mummer_cupriavidus_ralstonia/tmp_mumi MUM_cup_ral_all

$>compute_combined_MUMi.sh /user/home/gent/vsc406/vsc40682/mummer/mummer_cupriavidus_ralstonia/acc_intrest_list.txt /user/home/gent/vsc406/vsc40682/scratch/mummer/mummer_cupriavidus_ralstonia/tmp_mum_comp MUM_comp 



7) check when all jobs are done
$>qstat
empty results == is no planned or running jobs
Standard settings give you start and stop emails per job

Post processing
8) Quality test
in result directory
$>cat *.err result must be empty
$>cat *.out result must be empty

!errors sometimes happens
When you found an error, find file
$>grep " error message" /*.out of /*.err
Rerun the Job file qsub MUM000xx.sh

9) Make Compleet result set
$>cat *.txt >compleet_result_mumi.output
f=compleet_result_mumi.output 
with format:Burkholderia_383_uid58073	Burkholderia_ambifaria_AMMD_uid58303	8676277	7484986	0.394000	0.392027

10) Make simularity matrix to make tree

List2matrix start_accficdle resultfile_mummer kolomnr multiply_factor
!Important python version 3.2
$> python3.2 scripts/list2matrix.py mummer/mummer_cupriavidus_ralstonia/compleet_only/acc_intrest_list.txt.input mummer/mummer_cupriavidus_ralstonia/compleet_only/compleet_result_mumi_compleet_only.output 6 100 > mummer/mummer_cupriavidus_ralstonia/matrix_compleet_only6_100.dist
of in dir
$> python3.2 ~/scripts/list2matrix.py acc_intrest_list.txt compleet_result_mumi_compleet_only.output 5 100 > matrix_compleet_only_5_100.dist
For import in bionumerics -b flag
$> python3.2 ~/scripts/list2matrix.py -b acc_intrest_list.txt compleet_result_mumi_compleet_only.output 6 100 > matrix_compleet_only_6_100.dist


Optional if labels are to long relabel file
$>relable_file.py -f 0 compleet_result_mumi_compleet_only.output acc_intrest_list.txt.input 1 3


11) Make tree
With program of your choise

For some programs the keys will be to long:
substitude keys with the files from step 5
You can do this from the beginning or in the beginning of step 10
$>relable_file.py -f 1  matrix_compleet_only5_100.dist acc_intrest_list.txt.input 1 3 > matrix_compleet_only5_100.dist.relabeled

or you can do this in step 10


A)Bionumerics
!for bionumerics 7 the matrix must have 100 at the end of every line the diagonal
Create new empty local DB
Enable the folowing plugins/utilities in D7:
 * Import
 * Dendrogram tools
 * Databasetools
Create new experiment of type matrix
Import matrix file (not to long key names) button onder File in the left upper corner, Select matrix
select all entries
right bottom create new comparison
clustering->calculate->clustering analysis
*upgma
*neigberhood joining
reroot tree if nessesairy
! the distans matrix get recomputed in an other order, same result?? 

B)PHYLIP @todo

C)MEGA5 @todo

D) via website seemes not trelaiable very strange result be carefull
http://www.trex.uqam.ca/index.php?action=phylip
! use copy add line numers on first line
!select lower triangle
!select root of tree row number

Done
