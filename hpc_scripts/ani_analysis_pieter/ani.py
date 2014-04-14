#!/usr/bin/python
#14-02-2014 pieter.stragier@ugent.be v0.1
# Computes the ANI similarity value between two given complete genome sequences. If a genome sequence is 
# contained within a directory, all chromosomes of the genome sequences are merged before the genomes are 
# compared with each other.
#
# INPUT
#   seq1  GenBank file or directory containing GenBank files for the same genome
#   seq2  GenBank file or directory containing GenBank files for the same genome
#   -p    optional prefix used for creation of temporary file names (default: "ANI")
#   -t    optional directory for storage of temporary files (default: "/tmp")
#   -s    optional list of selected genomes to be combined with all others (default: all vs all)
# syntax: ani [-p prefix] [-t tmp_dir] [-i files_dir] [-o out_dir] [-s selected_genome]

#Dependencys: blast, emboss

######################################################################################
# NO changes lower than here!!!  (unless you know what your doing)
######################################################################################

#Process command line options
import optparse # needed for reading the options 
import os, sys, stat   # needed for file and directory handling
import itertools # needed for making combinations


def processcommandline():
    
    desc="""
    # This program runs an ANI analysis from the source files in the directory
    # # INPUT
    #   LMGxxxx.fa : a fasta file (.fa, .faa, .fasta, .fas)
    #   Single or multifasta file
    #OPTIONS
    #    -p --prefix    optional prefix used for creation of temp file names (default: "ANI")
    #    -t --temp_dir    Directory for temporary files
    #    -i --input_dir    Input directory
	#    -o --out_dir     Output directory
	#    -s --sel_genomes  Selection of genomes
    #    -d --debug        debug information progres and messages
    #    -v --verbose  verbose progress and messages
    #
    # usage: ani.py [options ]
    # syntax: ani.py -t /tmp -i /Fasta > save file
    # syntax: ani.py -s LMG23076
    """
    # Makes variable options anywhere available
    global options
    global args
    parser = optparse.OptionParser(  description=desc,
                            usage="usage: %prog [options] ",
                            version='%prog version 0.1')
                                           
    parser.add_option("-p", "--prefix",
                       action="store",
                      dest="o_prefix",
                       default="ANI",
                      help="Defines the temporary files prefix, default is set to ANI")
    parser.add_option("-t", "--temp_dir",
                       action="store",
                      dest="o_temp_dir",
                       default="/tmp",
                      help="Defines the temporary directory, default is set to /tmp")
    parser.add_option("-i", "--files_dir",
                       action="store",
                      dest="o_files_dir",
                       default="/",
                      help="Defines the fasta or genbank files directory, default is set to /") 
    parser.add_option("-s", "--sel_genome", 
                       action="store",
                      dest="o_sel_genome",
                       default=False,
                      help="Defines a specific genome to be combined with all the others, no other combinations will be made")					  
    parser.add_option("-o", "--out_dir",
                       action="store",
                      dest="o_out_dir",
                       default="/",
                      help="Defines the output directory, default is set to /") 
    parser.add_option("-d", "--debug",
                      action="store_true",
                      dest="o_debug_flag",
                      default=False,
                      help="Writes all kinds of debug info, step by step, and progress not good for piping")
    parser.add_option("-v", "--verbose",
                      action="store_true",
                      dest="o_verbose_flag",
                      default=False,
                      help="Writes all kinds of info for following progress, not good for piping")
                      
    (options, args) = parser.parse_args()   # splits the options and the arguments

    #Way of accessing the options
    #print "option save file default" +options.o_save_file

    
        
    if options.o_verbose_flag or options.o_debug_flag:
        print("options: ")
        print(options)
        print("Arguments: ")
        print(args)
    
    #    #Test if all arguments (1 and 2) of args are file names or directories and are valid
    #    if not os.path.isfile(args[0]) or not os.path.isfile(args[1]):
    #        parser.error("wrong number of arguments, only files and directories can be passed")
    
    #    #Set automatically -D diagonal value when making a full matrix
    #    if options.o_full_matrix_flag:
    #        #user did not choose a value for the diagonal
    #        if options.o_diagonal_flag is None:
    #            options.o_diagonal_flag= str(100)

            
    # flags are filled and processed (arguments in correct file extension?)
    #test 1 file

def main():
    import itertools
    import subprocess
    processcommandline()
    #debug test section
    lijst_input=read_input_file()
    result_ani=calculate_ani(lijst_input)

    #temporary directory
    if options.o_temp_dir:
        temp_dir = options.o_temp_dir
    else:
        temp_dir = "/tmp"
    #output directory
    if options.o_out_dir:
        out_dir = options.o_out_dir    
    #files folder
    if options.o_files_dir:
        files_dir = options.o_files_dir
    else:
        files_dir = "/"
    #selection of genomes
    if options.o_sel_genome:
        selection = options.o_sel_genome
    else:
        selection = False
    
  
    list_all_combinations=list(itertools.combinations(lijst_input, 2))
    if selection == False:  
        for combo in list_all_combinations:
            calculate_ani(combo)
    else:
    	for combo in list_all_combinations:
            if combo.__contains__(selection):
                calculate_ani(combo)

def read_input_file():
    import os
    lijst_files = []
    
    var = options.o_files_dir
    for dirpath, dirnames, filenames in os.walk(var):
        for file in filenames:
            if not file.__contains__("conc"):
                ext = file.split(".")[1]
                if ext.startswith("fa"):
                    #File is in fasta format
                    invoer = open(dirpath + "/" + file, 'r')
                    count = 0
                    for regel in invoer:
                        if regel.startswith(">"):
                            count += 1
                    if count > 1:
                        if not file.split(".")[0]+"_conc.fa" in filenames:
                            filelocation = dirpath + "/" + file
                            combine_multifasta(filelocation)
                    invoer.close()
                    Fformat = True
                elif ext.startswith("gb"):
                    #File is in genbank format
                    Fformat = False
                else:
                    pass
                lijst_files.append(dirpath + "/" + file)
    return lijst_files

def combine_multifasta(file):
    name, ext = file.split(".")
    invoer = open(file, 'r')
    uitvoer = open(name+"_conc."+ext, 'w')
    uitvoer.write(">" + name.rsplit("/")[-1] + "\n")
    count = 0
    for line in invoer:
        if line.startswith('>'):
            count += 1
        else:
            uitvoer.write(line)
    print("{} contigs concatenated in {}".format(count, file))
    invoer.close()
    uitvoer.close()

def convert_genbank_to_fasta(file):
    return "genbank to fasta"

def calculate_ani(combolist, name="job", logfile="output.$JOB_ID", errfile="error.$JOB_ID", cleanup=True, prefix="", slots=1):
    #Create for each makeblastdb job a .sh file and run it (qsub)
    import subprocess
        
    lijst_combo = []
    
    for file in combo:        
       lijst_combo.append(file)

    print(lijst_combo)
    #Uitvoerfolder   
    o_jobs = options.o_out_dir
    i_fasta = options.o_files_dir
    file1 = lijst_combo[0].split("/")[-1]
    file2 = lijst_combo[1].split("/")[-1]
    
    if not os.path.exists(o_jobs):
        os.mkdir(o_jobs)
    naam = lijst_combo[0].rsplit("/")[-1].split(".")[0] + "_" + lijst_combo[1].rsplit("/")[-1].split(".")[0]
    uitvoerbestand = o_jobs + "/ani_" + naam +".sh"
    uitvoer = open(uitvoerbestand, 'w')
    hoofding = "#!/bin/bash -x\n#PBS -N {}\n#PBS -S /bin/bash\n#PBS -o /user/scratch/gent/vsc406/vsc40697/ANI/tmp/ANI_{}.out\n#PBS -e /user/scratch/gent/vsc406/vsc40697/ANI/tmp/ANI_{}.err\n#PBS -m abe\n#PBS -l nodes=1:ppn=1,walltime=00:10:00\n#PBS -q short\n".format(naam, naam, naam)
    uitvoer.write(hoofding)
    uitvoer.write("module load BLAST/2.2.28-ictce-4.1.13\n")
    uitvoer.write("pool_size=1000\n")
    
    #makeblastdb commando line
    o_make1, db, invoer = o_jobs +'/'+ naam.split("_")[0] + "_my_nuc_blastdb", "nucl", i_fasta + '/' + file1
    commando_makeblastdb1 = "makeblastdb -in {} -dbtype {} -out {}\n".format(invoer, db, o_make1)
    uitvoer.write(commando_makeblastdb1)
    uitvoer.write("wait\n")
    o_make2, db, invoer = o_jobs +'/'+ naam.split("_")[1] + "_my_nuc_blastdb", "nucl", i_fasta + '/' + file2
    commando_makeblastdb2 = "makeblastdb -in {} -dbtype {} -out {}\n".format(invoer, db, o_make2)
    uitvoer.write(commando_makeblastdb2)
    uitvoer.write("wait\n")
    #blastn commando line
    o = o_jobs + '/' + naam + "_A.blastn.txt"
    commando_blastn1 = "blastn -db {} -query {} -out {} -outfmt 6 -dust no -max_target_seqs 1\n".format(o_make1, i_fasta + '/' + file2, o)
    uitvoer.write(commando_blastn1)
    uitvoer.write("wait\n")
    o = o_jobs + '/' + naam + '_B.blastn.txt'
    commando_blastn2 = "blastn -db {} -query {} -out {} -outfmt 6 -dust no -max_target_seqs 1\n".format(o_make2, i_fasta + '/' + file1, o)
    uitvoer.write(commando_blastn2)
    uitvoer.write("wait\n")
    
    uitvoer.write("seq1_name="+i_fasta + '/' + file1 +"\n")
    uitvoer.write("seq2_name="+i_fasta + '/' + file2+"\n")
    uitvoer.write("seq1_cds="+i_fasta + '/' + file1.split(".")[0] + "_conc." + file1.split(".")[1]+"\n")
    uitvoer.write("seq2_cds="+i_fasta + '/' + file2.split(".")[0] + "_conc." + file2.split(".")[1]+"\n")
    uitvoer.write("blastout1="+o_jobs + '/' + naam+"_A.blastn.txt"+"\n")
    uitvoer.write("blastout2="+o_jobs + '/' + naam+"_B.blastn.txt"+"\n")
    uitvoer.write("ANI_output="+o_jobs + '/' + naam + '_ani_output.txt' + '\n')
    var = os.getcwd()
    awk = open(var + '/ani_subroutine_apex.txt', 'r')
    for regel in awk:
        uitvoer.write(regel)
    uitvoer.close()
    import stat
    os.chmod(uitvoerbestand, stat.S_IRWXU)
    print("job created for {}".format(naam))
    subprocess.call('qsub ' + uitvoerbestand, shell=True)
    return "qsub submitted"

if __name__ == "__main__":
    main()
