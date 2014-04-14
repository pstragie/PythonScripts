#! /usr/bin/python
''' This program creates a matrix from the following source files
# # INPUT
#   maldi_peak file: a .csv file
#   maldi_peak FileFormat: File with header row , header row contains peak name
#                            Each row starts with organism name followed by peak yes or no 0/1
#                            Cell A1 is empty/not used
#       example:    ;Maldi:3728.15;Maldi:5036.67;Maldi:10822.6;
#                    awieme0047529;0;0;0;0;1;
#                    awieme0047530;1;1;1;1;1;
#
# Looks for the shared peaks in a combination of given organisms analog to CGI core genome
# Default gives a list per combination for all the shared peaks
#
# the scientific explanation:
# 
# This script calculates the number of shared Matrix-Assisted Laser 
# Desorption/Ionization Time-of-Flight Mass Spectrometry (MALDI-TOF MS) 
# peak classes between all possible entry combinations. 
# Such an entry must consist of a label and a binary character table 
# that represents the presence of certain peak classes. 
# Subsequently, the sequential inclusion of an entry within the dataset 
# was simulated in all possible combinations. The output will not only 
# show the number of shared peak classes for all possible combinations, 
# but also the corresponding m/z value, the average number of peak classes
# and the number of possible combinations per included entry.
#
#   field_nr: The number of the field that has to be used as value. First column is 1 and so on
#   OPTIONS
#    -c --csv_delimiter_input   Defines the delimiter value of the source file, default is set to ;
#    -C --csv_delimiter_output   Defines the delimiter value of the output file, default is set to \t
#    -d --debug        debug information progress and messages
#    -g --graph        Makes an output easy for making graphs (there is loss of data)
#    -v --verbose  verbose progress and messages
#
# usage: maldi_peak2matrix.py [options ] <inputfilein csv> 
# syntax: maldi_peak2matrix.py -c '\t' -C ';' source.csv > save file
# syntax: maldi_peak2matrix.py source.csv | post processing
# syntax: maldi_peak2matrix.py source.csv 
'''

#@todo

# TODO Sensible use of the -v verbose messaging
# TODO More readable debug output -d
# TODO sensible output to error stream when something is wrong
# TODO extra output form if necessary
# TODO Refractor to split argument and option handling away from program logic
# TODO Better help texts

__author__="baverhey"
__date__ ="$26-augustus-2013 16:31:47$"


import optparse # needed for reading the options 
#import os   # needed for file and directory handling
import itertools # needed for making combinations
#import pprint   # needed for prittyprint pprint nice debug

def processcommandline():
    
    desc="""
    # This program creates a matrix from the following source files
    # # INPUT
    #   maldi_peak file: a csv file
    #   maldi_peak FileFormat: File with header row , header row contains peak name
    #                            Eatch row starts with organism name folowed by peak jes or no 0/1
    #                            Cell A1 is empty/not used
    #       example:    ;Maldi:3728.15;Maldi:5036.67;Maldi:10822.6;
    #                    awieme0047529;0;0;0;0;1;
    #                    awieme0047530;1;1;1;1;1;
    #
    # Looks for the shared peaks in a combinations of given organisms analog to CGI core genome
    # Default gives a list per combination for all the shared peaks
    #
    # the scientific explanation:
    # 
    # This script calculates the number of shared Matrix-Assisted Laser 
    # Desorption/Ionization Time-of-Flight Mass Spectrometry (MALDI-TOF MS) 
    # peak classes between all possible entry combinations. 
    # Such an entry must consist of a label and a binary character table 
    # that represents the presence of certain peak classes. 
    # Subsequently, the sequential inclusion of an entry within the dataset 
    # was simulated in all possible combinations. The output will not only 
    # show the number of shared peak classes for all possible combinations, 
    # but also the corresponding m/z value, the average number of peak classes
    # and the number of possible combinations per included entry.
    #   field_nr: The number of the field that has to be used as value. First column is 1 and so on
    #   OPTIONS
    #    -c --csv_delimiter_input   Defines the delimiter value of the source file, default is set to ;
    #    -C --csv_delimiter_output   Defines the delimiter value of the output file, default is set to \t
    #    -d --debug        debug information progres and messages
    #    -g --graph        Makes a output easy for making graphs (there is loss of data)
    #    -v --verbose  verbose progress and messages
    #
    # usage: maldi_peak2matrix.py [options ] <inputfilein csv> 
    # syntax: maldi_peak2matrix.py -c '\t' -C ';' source.csv > save file
    # syntax: maldi_peak2matrix.py source.csv | post processing
    # syntax: maldi_peak2matrix.py source.csv 
    """
    # Makes variable options anywhere available
    global options
    global args
    parser = optparse.OptionParser(  description=desc,
                            usage="usage: %prog [options] input_cvv_file ",
                            version='%prog version 0.1')

    parser.add_option("-c", "--csv_delimiter_input",
                       action="store",
                      dest="o_csv_delimiter_input_value",
                       default=";",
                      help="Defines the delimiter value of the source file, default is set to ;")
                                           
    parser.add_option("-C", "--csv_delimiter_output",
                       action="store",
                      dest="o_csv_delimiter_output_value",
                       default="\t",
                      help="Defines the delimiter value of the output, default is set to \t")
    parser.add_option("-d", "--debug",
                      action="store_true",
                      dest="o_debug_flag",
                      default=False,
                      help="Writes all kinds of debug info, step by step, and progres not good for piping")

    parser.add_option("-g", "--graph",
                      action="store_true",
                      dest="o_graph_flag",
                      default=False,
                      help="Makes a output easy for making graphs (there is los of data)")

    parser.add_option("-v", "--verbose",
                      action="store_true",
                      dest="o_verbose_flag",
                      default=False,
                      help="Writes all kinds of info for folowing progress, not good for piping")
                      
    (options, args) = parser.parse_args()   # splits the options and the arguments

    #Way of accessing the options
    #print "option save file default" +options.o_save_file

    if len(args) < 1:
        parser.error("wrong number of arguments")
        
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
    processcommandline()    
    #debug test section
    dict_input=read_input_file(args[0])
    result_cgi_matrix=calculate_cgi(dict_input)
        
    dict_gelijke_pieken_per_combinatie=result_cgi_matrix["dict_gelijke_pieken_per_combinatie"]
    list_all_combinations=result_cgi_matrix["list_all_combinations"]
    

    #graph output chosen
    if options.o_graph_flag :
        print_gem_gelijke_pieken_voor_grafiek(dict_gelijke_pieken_per_combinatie,list_all_combinations)
        
    #default complete output
    else:
        print_gelijke_pieken(dict_gelijke_pieken_per_combinatie,list_all_combinations)
    

def read_input_file(input_file):

    '''
    Read 1 input file to arrays
    Split the input file in a header list, organism list, and the peak values
    '''

    #will hold all the values, values only, now row headers or ?
    value_matrix=[]

    #open file
    with open(input_file, 'r') as filereader:
        #read all lines
        all_file_data = filereader.readlines()    

    #close file
    filereader.closed
  
   
    
    #read first line
    header_line=all_file_data[0]
    #remove \n end lines
    header_line = header_line.replace('\n','')
            
    #split line in an array/list table header per column
    list_peaks_headers=header_line.split(options.o_csv_delimiter_input_value)
        
    if options.o_debug_flag :
        print("Removed the A1 cell %s",list_peaks_headers[0])
    #remove the first A1 cell (should be empty)
    del list_peaks_headers[0]
    
    list_organisms_rows=[]
    #read rest of the lines

    for rownr in range(1,len(all_file_data)):
    
        #process 1 line
        #read line
        line = all_file_data[rownr]
        #remove \n end lines
        line = line.replace('\n','')
        list_peaks_values=line.split(options.o_csv_delimiter_input_value)
        
        #Remove first column, organism name
        list_organisms_rows.append(list_peaks_values[0])
        if options.o_debug_flag :
            print("\nRemoved the first column organism name: %s",list_peaks_values[0])
        del list_peaks_values[0]
        
        value_matrix.append(list_peaks_values)

    result={"list_peaks_headers":list_peaks_headers,"list_organisms_rows":list_organisms_rows,"value_matrix":value_matrix}

    if options.o_debug_flag :
        print ("\n Result of reading file")
        print (result)

    return result

def calculate_cgi(matrix_dictionary):
    '''
    Gets the result of the read file function
    a matrix dictionary containing
    result={"list_peaks_headers":list_peaks_headers,"list_organisms_rows":list_organisms_rows,"value_matrix":value_matrix}
    
    '''
    list_peaks_headers = matrix_dictionary["list_peaks_headers"]
    list_organisms_rows = matrix_dictionary["list_organisms_rows"]
    value_matrix = matrix_dictionary["value_matrix"]
    dict_gelijke_pieken_per_combinatie={}
    list_all_combinations=[]

    #Make faculty groupings n!
    #AB    BC    CD        Step2    ABC    BCD
    #BC    BD                    ABD
    #BD
    #
    
    max_length_of_groupings = len(list_organisms_rows)
    
    for length_of_groupings in range (1,max_length_of_groupings+1):
        
        #all combinations of length
        list_combinations=list(itertools.combinations(list_organisms_rows,length_of_groupings))
        list_all_combinations.append(list_combinations)

        if options.o_debug_flag :
            print ("All combinations of lengt =",length_of_groupings)
            print ( str( list_combinations) )

        #Run through all combinations for length i and count the shared peaks
        for combinatie_i in list_combinations :
            #Treat one combination
            #init counters for 1 combination
            gemeenschapelijke_pieken=[]
            
            #go through all peaks
            for piek_x in list_peaks_headers:
                
                
                #Continue as long all peaks of the combination are equal until the length of combination is reached
                piek_gedeeld=True
                for organism_y in combinatie_i:
                    
                    if options.o_debug_flag :
                        print ("organism_y [Piek]= {0}[{1}] = {2}  wordt getest",
                            organism_y,piek_x,
                            value_matrix[list_organisms_rows.index(organism_y)][list_peaks_headers.index(piek_x)])
                    
                    #if 1 value is not a peak stop looking (save work)
                    if value_matrix[list_organisms_rows.index(organism_y)][list_peaks_headers.index(piek_x)]!= '1':
                        
                        #debug test if fail is correct
                        if options.o_debug_flag :
                            print ("Failed >>>organism_y [Piek]= {0}[{1} wordt getest",organism_y,piek_x)
                            
                        piek_gedeeld=False
                        break
                    
                #Save result if piek is shared
                if piek_gedeeld :
                    gemeenschapelijke_pieken.append(piek_x)
            
            # save the shared peaks for that combination
            if options.o_debug_flag :
                print("Combination to be saved:  {0}".format(combinatie_i))
                print("Shared peaks  {0} of combination: {1}".format(len(gemeenschapelijke_pieken),gemeenschapelijke_pieken))
                
            dict_gelijke_pieken_per_combinatie[combinatie_i]=gemeenschapelijke_pieken
            
        
    #print result for debug
    if options.o_debug_flag :
        print ("\n result peak counts per combination: \n")
        print (dict_gelijke_pieken_per_combinatie)
    
    result={"dict_gelijke_pieken_per_combinatie":dict_gelijke_pieken_per_combinatie,"list_all_combinations":list_all_combinations}
    
    return result


def print_gelijke_pieken (dict_gelijke_pieken_per_combinatie,list_combinations):
    '''
    print_gelijke_pieken does a clean datadump of
    "Combination","equal_peaks","name_of_peaks"
    list combinations is necessary to preserve the order of the collections
    dictionary is not ordered but the list is order witch we can use to recall the dict in order
    '''
    #list_combinations is a List of Lists of combinations per length with a combination being a tuple
    #                 [[(ab),(ac)],[(abc)]]
    #dict_gelijke_pieken_per_combinatie index in dictgelijkepieken matches with one list of peak names

    #print column header of csv
    kolom_header= "{0}{3}{1}{3}{2}".format("Combination","equal_peaks","name_of_peaks",options.o_csv_delimiter_output_value)
    print (kolom_header)
    
    #run through all combinations
    for combinations_of_length in list_combinations :
        
        if options.o_debug_flag :
            number_of_combination="#Number_of_combination{1}{0}".format(len(combinations_of_length),options.o_csv_delimiter_output_value)
            #pp = pprint.PrettyPrinter(indent=8)
            #pp.pprint(combinations_of_length)
            print (number_of_combination)
        
        #run through all combinations of 1 length
        for combin_i in combinations_of_length:
        
            #pp.pprint(dict_gelijke_pieken_per_combinatie[combin_i])
            formated_tuple_to_print=",".join(combin_i)
            formated_list_to_print= ",".join(dict_gelijke_pieken_per_combinatie[combin_i])
            lijn= "{0}{3}{1}{3}{2}".format(formated_tuple_to_print,len(dict_gelijke_pieken_per_combinatie[combin_i]), formated_list_to_print,options.o_csv_delimiter_output_value)
            print (lijn)

def print_gem_gelijke_pieken_voor_grafiek (dict_gelijke_pieken_per_combinatie,list_combinations):
    '''
    print_gem_gelijke_pieken_voor_grafiek does a datadump of 
    "length_of_Combination","number_of_combinations","average_shared_peaks","number_shared_peaks_per_combination"
    list combinations is necessary to preserve the order of the collections
    dictionary is not ordered but the list is order witch we can use to recall the dict in order
    There is loss of data, this print is only for convenience, for graph
    '''
    
    #list_combinations is a List of Lists of combinations per length with a combination being a tuple
    #                 [[(ab),(ac)],[(abc)]]
    #dict_gelijke_pieken_per_combinatie index in dictgelijkepieken matches with a list of peak names

    #print column header of csv
    kolom_header= "{0}{4}{1}{4}{2}{4}{3}".format("length_of_Combination","number_of_combinations","average_shared_peaks","number_shared_peaks_per_combination",options.o_csv_delimiter_output_value)
    print (kolom_header)
    
    #run through all combinations
    for combinations_of_length in list_combinations :
        
        number_of_combinations=len(combinations_of_length)        
        length_of_combination=len(combinations_of_length[0])
        total_shared_peaks_per_combination_length=0
        shared_peaks_datapoints=[]
        
        #print ("#######")
        #pp = pprint.PrettyPrinter(indent=8)
        #pp.pprint(combinations_of_length)
             
        #run through all combinations of 1 length
        for combin_i in combinations_of_length:
        
            number_of_shared_peaks=len(dict_gelijke_pieken_per_combinatie[combin_i])
            total_shared_peaks_per_combination_length+=number_of_shared_peaks
            shared_peaks_datapoints.append(str(number_of_shared_peaks))
            
        #create the line to print
        formated_list_to_print= str(options.o_csv_delimiter_output_value).join(shared_peaks_datapoints)
        #calculate average total shared peaks divided by number of combinations by that length
        avg=total_shared_peaks_per_combination_length/number_of_combinations
        print ("{0}{4}{1}{4}{2:.2f}{4}{3}".format(length_of_combination,number_of_combinations,avg,formated_list_to_print,options.o_csv_delimiter_output_value))
    



if __name__ == "__main__":
    main()
