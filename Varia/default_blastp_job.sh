#!/bin/bash -x
#PBS -N Project_NAME
#PBS -S /bin/bash
#PBS -o /user/scratch/gent/vsc406/vsc40697/orthoMCL/tmp//Project_NAME.out
#PBS -e /user/scratch/gent/vsc406/vsc40697/orthoMCL/tmp//Project_NAME.err
#PBS -m abe
#PBS -l nodes=1:ppn=1,walltime=01:59:00
#PBS -q short
module load BLAST/2.2.28-ictce-4.1.13

#Fill in your own directories below
blastp -query /user/home/gent/vsc406/vsc40697/orthoMCL/Project_vbeeumen/Analysis2/With/goodProteins.fasta -db /user/home/gent/vsc406/vsc40697/orthoMCL/Project_vbeeumen/Analysis2/With/my_prot_blast_db_with -out /user/data/gent/vsc406/vsc40697/orthoMCL/Project_vbeeumen/Analysis2/With/all-vs-all_with.tsv -outfmt 6 -num_threads 4

