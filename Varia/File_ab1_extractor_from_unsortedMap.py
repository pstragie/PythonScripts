'''
Created on 17-jan.-2013

Wanneer er na sequencing, meerdere folders zijn met sequentiebestanden,
gebruik dan dit script om al deze bestanden naar 1 folder te kopieren (!).

rpoB synoniemen worden omgezet naar 'rpoB_#'


@author: pstragie
'''
import shutil
import os
import fnmatch
#Locatie hoofdmap bepalen
totaal = 0
#pseulijst = ["LMG27888T","LMG27905T","LMG980T",  "LMG2123T", "LMG2137T", "LMG21995t1T" "LMG21995t2T" "LMG2335T", "LMG5011T", "LMG981T",  "LMG11722T","LMG1223T", "LMG1225T", "LMG13190T","LMG1794T", "LMG1874T", "LMG20220T","LMG20222T","LMG21316T","LMG21317T","LMG2158T", "LMG21605T","LMG21606T","LMG21607T","LMG21609T","LMG21611T","LMG21614T","LMG21629T","LMG21640T","LMG21661T","LMG2172T", "LMG21749T","LMG21750T","LMG21931T","LMG21977T","LMG2215T", "LMG2223T", "LMG2257T", "LMG2274T", "LMG23064T","LMG23066T","LMG23134T","LMG23197T","LMG23199T","LMG23201T","LMG2336T", "LMG2342T", "LMG23759T","LMG24016T","LMG24038T","LMG24039T","LMG7040T", "LMG26364T","LMG5327T(t1)""LMG20221T","LMG2209T", "LMG24791T","LMG27252T","LMG5004T", "LMG5694T", "LMG21467T","LMG21625T","LMG2243T", "LMG24676T","LMG24737T","LMG26839T","LMG11199T","LMG1224T", "LMG1242T", "LMG1245T", "LMG1247T", "LMG13184T","LMG13517T","LMG17761T","LMG17764T","LMG18376T","LMG18378T","LMG18387T","LMG19695T","LMG19851T","LMG2112T", "LMG21284T","LMG21318T","LMG21464T","LMG21465T","LMG21466T","LMG2152T", "LMG21539T","LMG21608T","LMG21615T","LMG21623T","LMG21624T","LMG2162T", "LMG21630T","LMG21662T","LMG2190T", "LMG2191T", "LMG21974T","LMG21995T","LMG2210T", "LMG22119T","LMG22120T","LMG22121T","LMG2229T", "LMG22563T","LMG22709T","LMG22710T","LMG2273T", "LMG23068T","LMG23075T","LMG23076T","LMG2352T", "LMG23570T","LMG23572T","LMG23661T","LMG23662T","LMG23769T","LMG24280T","LMG24281T","LMG24738T","LMG24752T","LMG25475T","LMG25716T","LMG26048T","LMG5096T", "LMG7041T"]
var = "Z:\\home\\Species\\Pseudomonas\\MLSA\\Unsorted"

dst = "Z:\\home\\Species\\Pseudomonas\\MLSA\\Unsorted"
for dirpath, dirnames, filenames in os.walk(var, topdown=True, followlinks=False):
    print(dirpath)
    Dir1 = dirpath #File Origin Directory - note this is for OSX
    Dir2 = dst #File Destination Directory - note this is for OSX 
    
    dirList=os.listdir(Dir1)
    
    for file1 in dirList: #file the files
        
        if fnmatch.fnmatch(file1, '*.ab1'): #make sure they match the wildcard
            print(file1) #echo the list of files to check 
            shutil.copy(Dir1+'\\'+file1, Dir2+'\\'+file1) # copy the files from origin to destination
            totaal += 1
        
print(totaal)                
'''
for root, dirs, files in os.walk(dst):
    for names in files:
        if names.__contains__("CM_32b"):
            A, B, C, D, E, F = names.split("_")
            nieuwe_naam = A + "_" + B + "_" + C + "_" + "rpoB_1" + "_" + F
            os.rename(dst+"\\"+names, dst2+"\\renamed"+nieuwe_naam)
        elif names.__contains__("CM81"):
            A, B, C, D, E = names.split("_")
            nieuwe_naam = A + "_" + B + "_" + C + "_" + "rpoB_2" + "_" + E
            os.rename(dst+"\\"+names, dst2+"\\renamed"+nieuwe_naam)
        elif names.__contains__("CM32b"):
            A, B, C, D, E = names.split("_")
            nieuwe_naam = A + "_" + B + "_" + C + "_" + "rpoB_3" + "_" + E
            os.rename(dst+"\\"+names, dst2+"\\renamed"+nieuwe_naam)
        elif names.__contains__("CM_81"):
            A, B, C, D, E, F = names.split("_")
            nieuwe_naam = A + "_" + B + "_" + C + "_" + "rpoB_4" + "_" + F
            os.rename(dst+"\\"+names, dst2+"\\renamed"+nieuwe_naam)
'''