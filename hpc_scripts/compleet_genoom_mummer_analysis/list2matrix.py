#! /usr/bin/python
# This program creates a matrix from the folowing source files
# as step for preprocessing to tget to a newick format tree
# INPUT
#   acc file: used to run the calculations
#   acc FileFormat: <genomename>  <genomedirectory> [<customkeyfor further processing>]
#       example:    NC_007509	/home/pdawyndt/genomes/bacteria/complete/Burkholderia_383_uid58073Bac0
#                   Burkholderia_383 /home/pdawyndt/genomes/bacteria/complete/Burkholderia_383 BU01
#
#   listfile: result file for example mummer analysis
#   listfile FileFormat:    Sequentie1_name	Sequentie2_name	seq1_lengte	
#                           seq2_lengte	seq1_cov	seq2_cov		
#                           Sim1	Sim2	Sim3	Sim4
#
#                           NC_007509.gbk	NC_007510.gbk	1395069		
#                            3694126		75366		87964	
#                            0.05402313	0.02381186	0.03209348	0.03891750
#
#   factor: value by witch the result is multiplayed
#
#   field_nr: The numer of the field that has to be used as value. First colum is 1 and so on
#   OPTIONS
#    -b --bionumerics   compatibility for import in bionumerics (7)
#    -d --debug        debug information progres and messages
#    -D --diagonal        choose the value at the diagonal at eatch line
#    -i --inverse        inverse every value against the chosen value
#    -f --full_matrix        gives full matrix instead of deafualt lower matrix
#    -n --number_of_rows        addes number of rows on fist line
#    -v --verbose  verbose progres and messages
#
# usage: list2matrix.py [< -i invers_value>] <accfile> <outputfile_in_liste> <field_nr> [< multiply_factor>] 
# syntax: list2matrix.py acc.txt.input MUM0000all.txt 5 100 



__author__="baverhey"
__date__ ="$21-augustus-2013 16:31:47$"


import optparse #nodig voor lezen opties 
import os   #nodig voor bestand en directory manipulaties


def main():
    
    desc="""
    @todo
    Comentaar vanboven aan file kopieren waneer bijna af
    """
    #Maakt variable opties overal aanspreekbaar
    global options
    
    parser = optparse.OptionParser(  description=desc,
                            usage="usage: %prog [options] acc-file result-file colum nr [factor] ",
                            version='%prog version 0.7')

    parser.add_option("-b", "--bionumerics",
                       action="store_true",
                      dest="o_bionumerics_flag",
                       default=False,
                      help="Writes a \t 100 ad the end of eatch line for compatibility reasons, import bionumerics7") 

    parser.add_option("-D", "--diagonal",
                       action="store",
                      dest="o_diagonal_flag",
                      default=None,
                      help="Writes a \t chosen value at the diagonal of eatch line (incompatible with -b --bionumerics7") 

    parser.add_option("-d", "--debug",
                      action="store_true",
                      dest="o_debug_flag",
                      default=False,
                      help="Writes all kinds of debug info, step by step, and progres not good for piping")

    parser.add_option("-i", "--inverse_matrix",
                       action="store",
                      dest="o_inverse_value",
                      default=None,
                      help="Inverces every value with the chosen value after the multiply factor") 

    parser.add_option("-f", "--full_matrix",
                      action="store_true",
                      dest="o_full_matrix_flag",
                      default=False,
                      help="When set a full matrix is created automaticly enables -D to defautl value, default its lower triangle")

    parser.add_option("-n", "--number_of_rows",
                      action="store_true",
                      dest="o_number_of_rows_flag",
                      default=False,
                      help="adds on the first line the number of rows of the matrix(use wc -l <input file when piping)")

    parser.add_option("-v", "--verbose",
                      action="store_true",
                      dest="o_verbose_flag",
                      default=False,
                      help="Writes all kinds of info for folowing progress, not good for piping")
                      

                      
#    parser.add_option("-p", "--prefix",
#                      action="store",
#                      dest="o_prefix",
#                      default="WE10_SORT_TREE",
#                      help="optional prefix used for creation of temporary file\
#                      names (default: [%default] )")
                      
#    parser.add_option("-f", "--filetype",
#                      action="store",
#                      dest="o_file_type",
#                      default="txt",
#                      help="optional filetype used for processing file names\
#                      (default: [%default] )")
    
#    parser.add_option("-t", "--tempdir",
#                      action="store", # optional because action defaults to "store"
#                      dest="o_tmp_dir",
#                      default="/tmp",
#                      help="optional directory for storage of temporary files (default: [%default] )",)
                      
#    parser.add_option("-s", "--save_file",
#                      action="store",
#                      dest="o_save_file",
#                      default="Result_sort_genoom_tree",
#                      help="Filename where the results will be saved in same directory of first file (default: [%default] )")                      
    
    (options, args) = parser.parse_args()   #splitst de opties en argumenten

    #Way of asaccing the options
    #print "option save file defoutl" +options.o_save_file

    if len(args) < 3:
        parser.error("wrong number of arguments")
        
    if options.o_verbose_flag or options.o_debug_flag:
        print("options: ")
        print(options)
        print("Arguments: ")
        print(args)
    
    #Testen of alle argumenten 1 en 2 van args wel bestandsnamen of directorys zijn en geldig
    if not os.path.isfile(args[0]) or not os.path.isfile(args[1]):
        parser.error("wrong number of arguments, only files and directorys can be passed")

    #Set automaticly -D diagonal value when making a full matrix
    if options.o_full_matrix_flag:
        #user did not choose a value for the diagonal
        if options.o_diagonal_flag is None:
            options.o_diagonal_flag= str(100)

            
    # hier zijn vlaggen gevuld en argumenten zijn bestanden juiste indeling ?? nog niet bevestigd
    #test 1 file
    
    #debug test section
    #int cast string to int
    dictionary_computed=read_result_file(args[1],int(args[2]))
    list_acc=read_acc_file(args[0])
    print_matrix(list_acc,dictionary_computed,float(args[3]))
    #process_one_file(args[0])
    #process_all(args)



def read_result_file(result_file, field_nr):
        
    '''
    Goal is to read the result file in to array with the assosiated
    computed[$1,$2]=computed[$2,$1]=$field
    computed[genpiece1, genpiece2]= value field
    INPUT
    result file
    field nr= nr of collum started form 1 ,python counts from 0 so adjust
    
    OUTPUT
    dictionary={(seq1,seq2): value_from_colum_field}
    
    '''
    #python counts from 0 so
    field_nr= field_nr -1
    
    if options.o_verbose_flag  or options.o_debug_flag:
        print("read_result_file:" + result_file)

    #open file
    #read lines
    with open(result_file, 'r') as filereader:
        #read line
        list_data = filereader.readlines()
            
    #close file
    filereader.closed
    
    if options.o_debug_flag :
        print("ingelezen data verwerken, Splitten")
    dictionary_computed={}
    
    #process all read lines
    for i in range(len(list_data)):
        
        if options.o_debug_flag :
            print () #just for nicer debug result
            print("Process line in one file")
            print(list_data[i] ,end="")
        #spit lijn in een array/list woord per celsleutel 
        list_line=list_data[i].split()
        
        if options.o_debug_flag :
            print("Line splitted in List/array")
            print(list_line)
        
        #Functional opvullen dictionary_computed
        #save in array [field1][field2]=value colum  
        #save in array [field2][field1]=value colum 
        key_tuple_1= (list_line[0],list_line[1])
        key_tuple_2= (list_line[1],list_line[0])
       
        dictionary_computed[key_tuple_1]=list_line[field_nr]
        dictionary_computed[key_tuple_2]=list_line[field_nr]
              
        if options.o_debug_flag :
            print('key: {0}     Value: {1}' .format(key_tuple_1,dictionary_computed[key_tuple_1]))
            print('key: {0}     Value: {1}' .format(key_tuple_2,dictionary_computed[key_tuple_2]))

    if options.o_debug_flag :

        print ('####################################')
        print ('###  Whole calculated dictionary  ###')
        print ('####################################')
        print (dictionary_computed)
        print ('####################################')

    return dictionary_computed


def read_acc_file(acc_file):
        
    '''
    Goal is to read the acc file in to array is a list of al seq    
    INPUT
    acc file
    
    OUTPUT
    List=[seq1,seq2,...]
    
    '''

    
    if options.o_verbose_flag  or options.o_debug_flag:
        print("read_acc_file: "+ acc_file)

    #open file
    #read lines
    with open(acc_file, 'r') as filereader:
        #read line
        list_data = filereader.readlines()
            
    #close file
    filereader.closed
    
    if options.o_debug_flag :
        print("ingelezen data verwerken, Splitten")
    #empty List
    list_acc=[]
    
    #process all read lines
    for i in range(len(list_data)):
        
        if options.o_debug_flag :
            print("Process one line in file")
            print(list_data[i])
        #spit lijn in een array/list woord per celsleutel 
        list_line=list_data[i].split()
        
        if options.o_debug_flag :
            print("Line splitted in List/array")
            print(list_line)
        
        #Functional opvullen dictionary_computed
        #save in list first field only
        
        list_acc.append(list_line[0])
              
        if options.o_debug_flag :
            #http://docs.python.org/3/tutorial/inputoutput.html
            print('key: {0}     Value: {1}'.format(len(list_acc)-1,list_line[0]))
            

    if options.o_debug_flag :
         print('\n####Result list_acc_ read file')
         print(list_acc)


    #return array       
    return list_acc

def print_matrix(list_acc, dictionary_computed, factor):

        
    '''
    Print the claculate matrix according to the desired options

    '''

    if options.o_debug_flag :
        print("In Print_matrix")
    
    #option  number of rows nessesairy for phylib
    if options.o_number_of_rows_flag :
        print(len(list_acc))

    # writes all lines of the matrix       
    for i in range(len(list_acc)):    
        line_to_print= list_acc[i]

        if options.o_debug_flag :
           print("Make line for : "+ line_to_print)
        
        #writes 1 line of the matrix
        for j in range(0,i):
            
            #construct key
            key_tuple= (list_acc[i],list_acc[j])
            if options.o_debug_flag :
                print('\n key_tuple = {0}' .format(key_tuple,))
                    
            #if value excists print * factor     
            if key_tuple in dictionary_computed:            
                #multiply by factor
                d_value=float(dictionary_computed[key_tuple])*factor
                
                #if option inverse_value set
                if options.o_inverse_value is not None:
                    d_value= float(options.o_inverse_value) - d_value
                
                line_to_print += "\t"+ str(d_value)
                
            else:
                line_to_print += "\t"+ "???"

        #The diagonal value
        #Writes \t 100 at the end of eatch line in the matrix, the diagonal
        if options.o_bionumerics_flag :
            line_to_print += "\t"+ "100"
        elif options.o_diagonal_flag is not None :
            line_to_print += "\t"+ options.o_diagonal_flag

        #The upper Triangle
        if options.o_full_matrix_flag :
            #the i+1 for the diagonal, that one is already done
            for u in range(i+1,len(list_acc)):
                #construct key
                key_tuple= (list_acc[i],list_acc[u])
                if options.o_debug_flag :
                    print('key_tuple = {0}' .format(key_tuple,))
                        
                #if value excists print * factor     
                if key_tuple in dictionary_computed:            
                    #multiply by factor
                    d_value=float(dictionary_computed[key_tuple])*factor
                    
                    #if option inverse_value set
                    if options.o_inverse_value is not None:
                        d_value= float(options.o_inverse_value) - d_value
                    
                    line_to_print += "\t"+ str(d_value)
                    
                else:
                    line_to_print += "\t"+ "???"

        
        line_to_print += "\n"
        print(line_to_print, end="")
  


if __name__ == "__main__":
    main()