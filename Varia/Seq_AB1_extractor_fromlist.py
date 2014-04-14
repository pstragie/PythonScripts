'''
Created on 26-02-2014

Extraheer BKL1 sequenties van XL3130


@author: pstragie
'''
import shutil, os, fnmatch, optparse

def processcommandline():
    
    desc="""
    # This program runs an ANI analysis from the source files in the directory
    
    #OPTIONS
    #    -s --search    optional search parameter (gene or primer name) (default: "BKL1")
    #    -y --year      optional year (default: all years)
    #    -i --input     optional file location
    #    -o --output    optional output directory
    """
    # Makes variable options anywhere available
    global options
    global args
    parser = optparse.OptionParser(  description=desc,
                            usage="usage: %prog [options] ",
                            version='%prog version 0.1')
                                           
    parser.add_option("-s", "--search",
                       action="store",
                      dest="o_search",
                       default="All",
                      help="Defines the gene or primer name, default is set to all")
    
    parser.add_option("-y", "--year",
                       action="store",
                      dest="o_year",
                       default="All",
                      help="Defines the year to look in, default is set to all years")
    parser.add_option("-i", "--input",
                       action="store",
                      dest="o_input",
                       default=os.path.join(os.getcwd(), "strain.txt"),
                      help="Defines the input directory and file name which contains the strains, default is set to current directory/strains.txt")
    parser.add_option("-o", "--output",
                       action="store",
                      dest="o_output",
                       default=os.path.join(os.getcwd(), "AB1_sequences"),
                      help="Defines the output directory, default is set to current directory/AB1_sequences") 
    (options, args) = parser.parse_args()   # splits the options and the arguments

    
    
        
def main():    
    processcommandline()
    geneprimer = "All"
    if options.o_search:
        geneprimer = options.o_search
        #print("Looking for {}".format(geneprimer))
    year = "All"
    if options.o_year:
        year = options.o_year
        #print("Looking in years: {}".format(year))
    #directories
    if options.o_input:
        input_dir = options.o_input
    else:
        input_dir = os.path.join(os.getcwd(), "strains.txt")
    if options.o_output:
        output_dir = options.o_output
    else:
        if options.o_search:
            folder = options.o_search
        else:
            folder = "AB1_sequences"
        output_dir = os.path.join(os.getcwd(), folder)
    var = r"\\3130XLCOMPUTER\Sequencing runs"


    totaal = 0
    #Maak de lijst van stammen op basis van een tekstbestand
    pseulijst = []
    bestand = input_dir
    invoer = open(bestand, "r")
    for regel in invoer:
        pseulijst.append(regel.rstrip())
    invoer.close()
    
    
    
    #print("Input file: {}".format(input_dir))
    #print("Output folder: {}".format(output_dir))


    
    
    dst = output_dir
    if not os.path.exists(dst):
        os.mkdir(dst)
        
    for dirpath, dirnames, filenames in os.walk(var, topdown=True, followlinks=False):
        
        
        #dirnames[:] = [d for d in dirnames if "2012" not in d]
        #dirnames[:] = [d for d in dirnames if "2013" not in d]        
        #rnames[:] = [d for d in dirnames if "2010" not in d]         
        dirnames[:] = [d for d in dirnames if "LMG runs" not in d] 
        #dirnames[:] = [d for d in dirnames if "SEQUENCING RUNS 2007-12-03 tem 2008-02-14" not in d] 
        #dirnames[:] = [d for d in dirnames if "SEQUENCING RUNS 2007-09-04 tem 2007-11-28" not in d] 
        #dirnames[:] = [d for d in dirnames if "SEQUENCING RUNS 2007-03-05 tem 2007-08-30" not in d] 
        if year != "All":
            dirnames[:] = [d for d in dirnames if d.startswith(options.o_year)]        
        print(dirpath)
        Dir1 = dirpath #File Origin Directory - note this is for OSX
        Dir2 = dst #File Destination Directory - note this is for OSX 
        
        dirList=os.listdir(Dir1)
        
        for file1 in dirList: #file the files
            
            if fnmatch.fnmatch(file1, '*.ab1'): #make sure they match the wildcard
                if file1.split("_")[2] in pseulijst:
                    if options.o_search != "All":
                        if file1.split("_")[3].startswith(options.o_search):
                            print(file1) #echo the list of files to check 
                            shutil.copy(Dir1+'\\'+file1, Dir2+'\\'+file1) # copy the files from origin to destination
                            totaal += 1
                    else:
                        print(file1) #echo the list of files to check 
                        shutil.copy(Dir1+'\\'+file1, Dir2+'\\'+file1) # copy the files from origin to destination
                        totaal += 1
            
    print(totaal)                

if __name__ == '__main__':
    main()
