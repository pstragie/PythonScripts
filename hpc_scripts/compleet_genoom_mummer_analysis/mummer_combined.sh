#!/bin/bash
# 6-2-2013 bart.verheyde@ugent.be V0.3
# Compute the MUM-index between two given complete genome sequences. All chromosomes in 
# the given directories are merged into combined genomes, before the genomes are compared 
# with each other.
#
# Dependency http://emboss.sourceforge.net/download/#Stable/ seqret
# Dependency http://mummer.sourceforge.net/ mummer
#
# syntaxis: mummer_combine.sh <seq1_dir> <seq2_dir> <prefix> <tmp_dir>






######################################################################################
# NO changes lower than here!!!  (unless you know what your doing)
######################################################################################


# process arguments
seq1_dir=`echo "$1" | sed -e 's/\/*$//'`             # remove final slash from directory name
seq2_dir=`echo "$2" | sed -e 's/\/*$//'`
seq1=`echo "${seq1_dir}" | awk -F'/' '{print $NF}'`  # extract name as last part of directory name
seq2=`echo "${seq2_dir}" | awk -F'/' '{print $NF}'`
#tmp_dir="/home/pdawyndt/projects/genomic_distance/mumi_tmp"
tmp_dir=$4


# set default values
if [ -z ${tmp_dir} ]
then
  tmp_dir="mumi_tmp"
fi


#seq1_fasta="${tmp_dir}/$3_${seq1}.fasta"                   # construct temporary FASTA file names
#seq2_fasta="${tmp_dir}/$3_${seq2}.fasta"
#mumfile="${tmp_dir}/$3_${seq1}_${seq2}.mummer"             # construct temporary file name to output results
# orgineel $(tempfile) vervangen door $(mktemp) voor op hpc
seq1_fasta=$(mktemp)
seq2_fasta=$(mktemp)
mumfile=$(mktemp)

# convert GenBank files to (concatenated) files in FASTA format
echo ">${seq1}" > ${seq1_fasta}
for seqfile in `grep -H '^DEFINITION' ${seq1_dir}/*.gbk | grep -v 'plasmid' | sort | cut -d':' -f1`
do
  seqret -sequence ${seqfile} -sformat gb -osf fasta -stdout -auto 2> /dev/null | tail -n +2 >> "${seq1_fasta}"
  while [ $? -ne 0 ]
  do
    seqret -sequence ${seqfile} -sformat gb -osf fasta -stdout -auto 2> /dev/null | tail -n +2 >> "${seq1_fasta}"
  done
done

echo ">${seq2}" > ${seq2_fasta}
for seqfile in `grep -H '^DEFINITION' ${seq2_dir}/*.gbk | grep -v 'plasmid' | sort | cut -d':' -f1`
do
  seqret -sequence ${seqfile} -sformat gb -osf fasta -stdout -auto 2> /dev/null | tail -n +2 >> "${seq2_fasta}"
  while [ $? -ne 0 ]
  do
    seqret -sequence ${seqfile} -sformat gb -osf fasta -stdout -auto 2> /dev/null | tail -n +2 >> "${seq2_fasta}"
  done
done

# process sequences by mummer
mummer -mum -b -c -l 19 ${seq1_fasta} ${seq2_fasta} > ${mumfile} 2> /dev/null

# get sequence length
seq1_len=`tail -n +2 ${seq1_fasta} | tr -d '\n\r ' | wc -c`
seq2_len=`tail -n +2 ${seq2_fasta} | tr -d '\n\r ' | wc -c`

awk -v len1=${seq1_len} -v len2=${seq2_len} -v seqname1=${seq1} -v seqname2=${seq2} '
# forward or reverse hit for second sequence
/^>/ { if ($0 ~ /Reverse/) reverse=1; next }

# mark positions covered by MUMs
{
  len+=$3
  for(i=$1;i<$1+$3;++i) seq1[i-1]=1
  if (reverse==1)
    for(i=$2-$3+1;i<=$2;++i) seq2[i-1]=1
  else
    for(i=$2;i<$2+$3;++i) seq2[i-1]=1
}

# determine MUM-index
END {
  # compute MUM-coverages of both genomes
  for(i=0;i<len1;++i) cov1+=seq1[i]
  for(i=0;i<len2;++i) cov2+=seq2[i]

  # first version of MUM-index
  MUM1 = 0.5*(cov1/len1 + cov2/len2)

  # second version of MUM-index
  MUM2 = (cov1 + cov2)/(len1 + len2)

  # output results
  printf("%s\t%s\t%d\t%d\t%f\t%f\n",seqname1,seqname2,len1,len2,MUM1,MUM2);
}
' ${mumfile}

# remove temporary fasta files
rm -f ${seq1_fasta}
rm -f ${seq2_fasta}
rm -f ${mumfile}
