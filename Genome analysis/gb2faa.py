from Bio import SeqIO
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input file")
args = parser.parse_args()
if not args.input:
	print("Input data missing")
	print("Use -i <file> to set the location and name of the input file")
else:	
	filelocation = args.input.rsplit("/", 1)[0]	
	name, extension = args.input.split("/")[-1].split(".")	
	gbk_filename = args.input
	faa_filename = name+".faa"
	input_handle  = open(gbk_filename, "r")
	output_handle = open(filelocation+"/"+faa_filename, "w")

	for seq_record in SeqIO.parse(input_handle, "genbank") :
		print "Dealing with GenBank record %s" % seq_record.id
		for seq_feature in seq_record.features :
		    if seq_feature.type=="CDS" :
		        assert len(seq_feature.qualifiers['translation'])==1
		        output_handle.write(">%s_%s\n%s\n" % (
		               seq_feature.qualifiers['locus_tag'][0],
		               seq_record.name,
		               seq_feature.qualifiers['translation'][0]))

	output_handle.close()
	input_handle.close()
