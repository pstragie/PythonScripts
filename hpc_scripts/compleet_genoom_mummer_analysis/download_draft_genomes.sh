#!/bin/bash -x

#relative data dir
datadir="${HOME}"
wanted_bacteria='Cupriavidus' 	#'Burkholderia' 'Cupriavidus' 'Ralstonia' 
ftp_language_dir='Map' 		# 'Map' or 'Directory' depending on your os language


######################################################################################
# NO changes lower than here!!!  (unless you know what your doing)
######################################################################################
# create directory for storing genome sequences
genomedir="${datadir}/genomes"
bactdir="${genomedir}/bacteria"
bactdir_draft="${bactdir}/draft"

#rm -rf ${bactdir_draft}   #When downlouding different draft one after an other they otherwise get removed
mkdir -p ${genomedir}
mkdir -p ${bactdir}
mkdir -p ${bactdir_draft}

cd "${bactdir_draft}"
cdir=`pwd`

#for visual check of available drafts go to ftp://ftp.ncbi.nih.gov/genomes/Bacteria_DRAFT

# download and unpack bacterial genomes
for dir in $(wget -qO - ftp://ftp.ncbi.nih.gov/genomes/Bacteria_DRAFT/ | grep $ftp_language_dir | grep $wanted_bacteria | sed 's/^.*>\(.*\)\/<.*$/\1/')
do
 echo -n "processing ${dir} ... "
 mkdir -p ${dir}
 cd ${dir}
 for file in $(wget -qO - ftp://ftp.ncbi.nih.gov/genomes/Bacteria_DRAFT/${dir}/ | grep 'gbk.tgz' | sed 's/^.* href="\(.*\)">.*$/\1/')
 do
  wget -q "${file}"
  if [ -f "$(basename $(echo "${file}"))" ]; then
   tar xzf $(basename $(echo "${file}"))
   rm -f $(basename $(echo "${file}"))
  fi
 done 
 cd "${cdir}"
 echo "DONE"
done

# create list of accession numbers
# NOT needed for now
#cd ${genomedir}
#find ${genomedir} -name '*.gbk' | sed 's/\(.*\/\([^/.]*\).gbk\)/\2\t\1/' > "acc_${wanted_bacteria}\_drafts.txt"


