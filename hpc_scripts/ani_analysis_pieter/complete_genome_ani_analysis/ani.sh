#!/bin/bash 
#15 -7-2013 bart.verheyde@ugent.be V0.5
# Computes the ANI similarity value between two given complete genome sequences. If a genome sequence is 
# contained within a directory, all chromosomes of the genome sequences are merged before the genomes are 
# compared with each other.
#
# INPUT
#   seq1  GenBank file or directory containing GenBank files for the same genome
#   seq2  GenBank file or directory containing GenBank files for the same genome
#   -p    optional prefix used for creation of temporary file names (default: "ANI")
#   -t    optional directory for storage of temporary files (default: "/tmp")
#
# syntax: ani [-p prefix] [-t tmp_dir] seq1 seq2

#Dependencys: blast, emboss

######################################################################################
# NO changes lower than here!!!  (unless you know what your doing)
######################################################################################


# process command line options
prefix="ANI"
tmp_dir="/tmp_ani"
while getopts 'p:t:' option
do
  case ${option} in
    p) prefix=${OPTARG};;
    t) tmp_dir=`echo "${OPTARG}" | sed -e 's/\/*$//'`;;
    ?) echo "Usage: ani [-p prefix] [-t tmp_dir] seq1 seq2" >&2
       exit 1;;
  esac
done
let "numoptions = ${OPTIND}-1"
shift ${numoptions}

# process command line arguments
if [ $# -ne 2 ]
then
  echo "$0: invalid number of arguments" >&2
  echo "Usage: ani [-p prefix] [-t tmp_dir] seq1 seq2" >&2
  exit 1682
fi
if [ ! -f $1 -a ! -d $1 ]
then
  echo "$0: illegal argument" >&2
  echo "Usage: ani [-p prefix] [-t tmp_dir] seq1 seq2" >&2
  exit 1
fi
if [ ! -f $2 -a ! -d $2 ]
then
  echo "$0: illigal argument" >&2
  echo "Usage: ani [-p prefix] [-t tmp_dir] seq1 seq2" >&2
  exit 1
fi
seq1_file=`echo "$1" | sed -e 's/\/*$//'`                  # remove final slash from directory name
seq2_file=`echo "$2" | sed -e 's/\/*$//'`
seq1_name=`echo "${seq1_file}" | awk -F'/' '{print $NF}'`  # extract name as last part of file or directory name
seq2_name=`echo "${seq2_file}" | awk -F'/' '{print $NF}'`

# construct temporary file names
seq1_mfasta="${tmp_dir}/${prefix}_${seq1_name}.mfasta"     # names for multi fasta files
seq2_mfasta="${tmp_dir}/${prefix}_${seq2_name}.mfasta"
blastout1="${tmp_dir}/${prefix}_${seq1_name}.blast"        # names for blast output
blastout2="${tmp_dir}/${prefix}_${seq2_name}.blast"
makeblastlog1="${tmp_dir}/${prefix}_${seq1_name}.makeblast.log"        # names for makeblast log
makeblastlog2="${tmp_dir}/${prefix}_${seq2_name}.makeblast.log"


# convert GenBank file(s) to multi-FASTA files
# echo "converting GenBank files to multi-FASTA files ..."
if [ -d ${seq1_file} ] #if directory
then
  rm -f ${seq1_mfasta}
  for seqfile in `grep -H '^DEFINITION' ${seq1_file}/*.gbk | grep -v 'plasmid' | sort | cut -d':' -f1`
  do
    # echo "extracting coding sequences from ${seqfile} ..."
    #for debug extract feat, add -verbose
	#originaly all extractfeat had 2>/dev/null to dimp erros we want to know when tere are errors
    extractfeat -type CDS -join Y -sequence ${seqfile} -stdout -auto 2>/dev/null >> ${seq1_mfasta}
  done
else
  extractfeat -type CDS -join Y -sequence ${seq1_file} -stdout -auto 2>/dev/null > ${seq1_mfasta}
fi
seq1_cds=`grep '^>' ${seq1_mfasta} | wc -l`

if [ -d ${seq2_file} ]
then
  rm -f ${seq2_mfasta}
#grep -v removes the hit of from the list
  for seqfile in `grep -H '^DEFINITION' ${seq2_file}/*.gbk | grep -v 'plasmid' | sort | cut -d':' -f1`
  do
    # echo "extracting coding sequences from ${seqfile} ..."
    extractfeat -type CDS -join Y -sequence ${seqfile} -stdout -auto 2>/dev/null  >> ${seq2_mfasta}
  done
else
  extractfeat -type CDS -join Y -sequence ${seq2_file} -stdout -auto 2>/dev/null  > ${seq2_mfasta}
fi
seq2_cds=`grep '^>' ${seq2_mfasta} | wc -l`

# create BLAST databases
#echo "creating BLAST databases ..."
# - p F Input is a nucleotide, not a protein., -i input file

#Depricated #formatdb -p F -i ${seq1_mfasta} -l /dev/null
#Depricated #formatdb -p F -i ${seq2_mfasta} -l /dev/null
#GOS Used conversion tool off blast itself
#legacy_blast.pl formatdb -p F -i seq1_mfasta -l /dev/null --print_only
#legacy_blast.pl formatdb -p F -i seq2_mfasta -l /dev/null --print_only

# -logfile /dev/null is nessesairy otherwise output is scruwed up 
#@ todo write to stream o of hpc job 1> instead of /dev/null?
makeblastdb -in ${seq1_mfasta} -dbtype nucl -logfile ${makeblastlog1}
makeblastdb -in ${seq2_mfasta} -dbtype nucl -logfile ${makeblastlog2}



# perform all-against-all BLAST
#echo "performing all-against-all BLAST ..."
#Depricated # blastall -p BLASTN -d ${seq1_mfasta} -i ${seq2_mfasta} -o ${blastout2} -X 150 -q -1 -F F -b 1 -v 1 -m 8
#Depricated # blastall -p BLASTN -d ${seq2_mfasta} -i ${seq1_mfasta} -o ${blastout1} -X 150 -q -1 -F F -b 1 -v 1 -m 8

#GOS Used conversion tool off blast itself
#legacy_blast.pl blastall -p BLASTN -d ${seq1_mfasta} -i ${seq2_mfasta} -o ${blastout2} -X 150 -q -1 -F F -b 1 -v 1 -m 8 --print_only
# -X dropoff value for gapped alignment (in bits) (zero invokes default behavior, except with megablast, which defaults to 20, and rpsblast and seedtop, which default to 15. The default values for the other commands vary with "program": 30 for blastn, 20 for megablast, 0 for tblastx, and 15 for everything else.)
#-v Number of one-line descriptions to show (V) (default = 500)
#-b Number of database sequences to show alignments for (B) (default is 250)
#-m output format
#-F F  Filter options for DUST or SEG; defaults to T for bl2seq, blast2, blastall, blastall_old, blastcl3, and megablast, and to F for blastpgp, impala, and rpsblast.
#legacy_blast.pl blastall -p BLASTN -d ${seq2_mfasta} -i ${seq1_mfasta} -o ${blastout1} -X 150 -q -1 -F F -b 1 -v 1 -m 8 --print_only

#ORgineel blastn -db ${seq1_mfasta} -query ${seq2_mfasta} -xdrop_gap 150 -num_descriptions 1 -num_alignments 1 -penalty -1 -out ${blastout2} -outfmt 6 -dust no 
# add -xdrop_gap 150 -num_descriptions 1 -num_alignments 1 -penalty -1  --> num_description -max_target_seqs 1 not compatible with max_target_seqs
##the extra options gave:
##BLAST engine error: Error: Gap existence and extension values 0 and 0 are not supported for substitution scores 1 and -1
##3 and 2 are supported existence and extension values
##Het resulterend werken d commando gebuikt defaults voor:
## -xdrop_gap 30 ipv 150 vroeger
##-penalty -3 ipv -1 vroeger, gaf fouten door soms 0 te worden denk ik
##-num_alignments 250 ipv 1

#Extra options -num_threads 16 
blastn -db ${seq1_mfasta} -query ${seq2_mfasta} -out ${blastout2} -outfmt 6 -dust no -max_target_seqs 1
blastn -db ${seq2_mfasta} -query ${seq1_mfasta} -out ${blastout1} -outfmt 6 -dust no -max_target_seqs 1


# parse BLAST output
# echo "parsing BLAST output ..."

awk -v seq1=${seq1_name} -v seq2=${seq2_name} -v seq1_cds=${seq1_cds} -v seq2_cds=${seq2_cds} '
{
  # extract information about query sequence, best hit sequence and best hit alignment
  query_id = $1
  hit_id = $2
  align_similarity = $3
  align_len = $4
  #align_mismatches = $5
  #align_gaps = $6
  align_query_start = $7
  align_query_stop = $8
  align_hit_start = $9
  align_hit_stop = $10
  #align_evalue = $11
  #align_bitscore = $12

  # correct sequence similarity by alignable length
  query_len = align_query_stop - align_query_start + 1
  hit_len = align_hit_stop - align_hit_start + 1
  wl = (sqrt(2)*query_len*hit_len)/sqrt(query_len^2+hit_len^2)
  len_ratio=align_len/wl; if (len_ratio>1) len_ratio=1
  sim_recalc=align_similarity*len_ratio

  # calculate forward or reverse ANI (only for hit segments with maximal similarity)
  if (query_id != prev_query_id) {
    prev_query_id=query_id
    if (len_ratio >= 0.7 && sim_recalc >= 0.3) {
      if (firstfile=="" || FILENAME==firstfile) {
        firstfile=FILENAME
        ++forward_hits
        forward_ani+=sim_recalc
        forward_sim[forward_hits]=sim_recalc
        forward_query[forward_hits]=query_id
        forward_match[query_id]=hit_id
      }
      else {
        ++reverse_hits
        reverse_ani+=sim_recalc
        reverse_sim[reverse_hits]=sim_recalc
        reverse_query[reverse_hits]=query_id
        reverse_match[query_id]=hit_id
      }
    }
  }
}

END {
  # determine best reciprocal hits
  for(i=1;i<=forward_hits;++i) {
    if (reverse_match[forward_match[forward_query[i]]] == forward_query[i]) {
      ++dual_hits
      dual_ani+=forward_sim[i]
    }
  }
  if (forward_hits>0) forward_ani /= forward_hits
  if (reverse_hits>0) reverse_ani /= reverse_hits
  if (dual_hits>0) dual_ani /= dual_hits

  # output ANI (forward, reverse and dual)
  printf("%s\t%s\t%d\t%d\t%d\t%10.8f\t%d\t%10.8f\t%d\t%10.8f\n",seq1,seq2,seq1_cds,seq2_cds,forward_hits,forward_ani,reverse_hits,reverse_ani,dual_hits,dual_ani)
}
' ${blastout1} ${blastout2}

## remove temporary files
rm -f ${blastout1}
rm -f ${blastout2}
rm -f ${makeblastlog1}
rm -f ${makeblastlog2}
rm -f "${seq1_mfasta}"
rm -f "${seq1_mfasta}.nhr"
rm -f "${seq1_mfasta}.nin"
rm -f "${seq1_mfasta}.nsq"
rm -f "${seq2_mfasta}"
rm -f "${seq2_mfasta}.nhr"
rm -f "${seq2_mfasta}.nin"
rm -f "${seq2_mfasta}.nsq"
