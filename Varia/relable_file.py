#! /usr/bin/env python
# Relable File
#
# converts old labels into new labels in source file, where old and new labels are
# read from specific columns in a label file. Tabs are used as default field separator in
# the label file.
#
# syntax: relabel_file <source_file> <label_file> <column_old_label> <column_old_label>
#
# Excpected source file -> text
# Excpected lable file  -> csv or other column based format
# for content for both files:
#	kol1	kol2	kol3 .....
#	kol1;kol2;kol3 .....
#	kol1 kol2 kol3 .....
#
#
# INPUT
#   Sourcefile
#	labelfile
#	column_old_label: the values witch need replacing
#	column_old_label: the new values
#   -c --csv   optional delimter for label file (default: ";")
#   -d --debug   optional delimter for label file (default: "\t")
#   -v --verbose verbose progres and messages
#
# syntax: relabel_file [-v][-d] [-c 'delimiter']  <source_file> <label_file> <column_old_label> <column_new_label>
#
#@TODO
#TESTING for \n as delimiter wil lnot work i think
#Writing -v to log file,
#Stream for error file?

from symbol import break_stmt
from pydoc import describe
from datetime import datetime
import sys
import optparse
import os
import re
import glob
import datetime
import fileinput

__author__="baverhey"
__date__ ="$4-jan-2013$"

# process command line options


def process_command_line():
	desc="""Relable File

	converts old labels into new labels in source file, where old and new labels are
	read from specific columns in a label file. Tabs are used as default field separator in
	he label file.

	syntax: relabel_file <source_file> <label_file> <column_old_label> <column_old_label>

	Excpected source file -> text
	Excpected lable file  -> csv or other column based format
	for content for both files:
		kol1	kol2	kol3 ...
		kol1;kol2;kol3 ...
		kol1 kol2 kol3 ...


	INPUT
		Sourcefile: the text witch will be searched
		labelfile: the kolom file witch contains the label to replace and new one on 1 line
		column_old_label: the values witch need replacing
		column_new_label: the new values
		-c --csv   optional delimter for label file (default: ";")
		-d --debug   optional delimter for label file (default: "\t")
		-v --verbose verbose progres and messages

	syntax: relabel_file [-v][-d] [-c 'delimiter']  <source_file> <label_file> <column_old_label> <column_new_label>
	python relable_file.py -vd -c ' ' RAxML_bootstrap.exampleRun_conserved_genes burkholderia+CH34.cgi.input 3 1

	"""

	#Maakt variable opties overal aanspreekbaar
	global options

	parser = optparse.OptionParser(  description=desc,
							usage="usage: %prog [options] dir or (file1 file2) [file_n ...]",
							version='%prog version 0.1')

		  
	parser.add_option("-c", "--csv",
					  action="store",
					  dest="o_delimiter",
					  default=";",
					  help="optional delimiter used for spliting the columns\
					  (default: [%default] )")

	parser.add_option("-d", "--debug",
					  action="store_true",
					  dest="o_debug_flag",
					  default=False,
					  help="Writes all kinds of debug info and progres not good for piping")

	parser.add_option("-v", "--verbose",
					  action="store_true",
					  dest="o_verbose_flag",
					  default=False,
					  help="Writes all kinds of info and progres not good for piping")

#	parser.add_option("-s", "--save_file",
#					  action="store",
#					  dest="o_save_file",
#					  default="Result_sort_genoom_tree",
#					  help="Filename where the results will be saved in same directory of first file (default: [%default] )")
	(options, args) = parser.parse_args()   #split the options and the arguments

#region for testing input on validity
	if not args[2].isdigit() or not args[3].isdigit():
		parser.error("<column_old_label> <column_new_label> arguments,are not numbers")
	#cast to inteer for furter usage
	else:
		try:
			args[2]= int(args[2]) -1 #computers start counting from 0
			args[3]= int(args[3]) -1 #computers start counting from 0
		except ValueError:
			parser.error("<column_old_label> <column_new_label> arguments,are not numbers")
			
#End of testing region

	#Way of accessing the options
	if options.o_verbose_flag :
		print "options: "
		print options
		print "Arguments: "
		print args

	# hier zijn options vlaggen gevuld en argumenten worden verder doorgegeven
	#all arguments and options ready to use
	return args 
 


def construct_substitution_dictionary(args):
	
	"""
	Takes all the args and uses the label_file argument to build a dictionary
	of the type dictionary[old_lable]=new_label
	@return dictionary of type dictionary[oldlabels]= new labels
	"""

	if options.o_verbose_flag :
		print ("Started building substitution table from "+ args[1] + 
				 "From columns " + str(args[2]) + "and " + str(args[3]))
	
	#define empty dictionary
	dictionary_labels={}
	#input arg label file
	in_labelfile=args[1]
	#input arg column_old_label
	in_old_label_colnr=args[2]
	#input arg new_label
	in_new_label_colnr=args[3]

	#read file line for line
	for line in fileinput.input(in_labelfile):
		
		#process(line) with split to list
		#split in colums by delimiter defined by option -c
		list_of_columns=line.split(options.o_delimiter)

		#save relevent old key and new key
		#trip awy \n from line (keeps last \n intact
		old_label=list_of_columns[in_old_label_colnr].strip('\n')
		new_label=list_of_columns[in_new_label_colnr].strip('\n')
		
		dictionary_labels[old_label]=new_label
		
		#print verbose what is saved
		if options.o_verbose_flag :
			print (" \n dictionary_labels[ "+ list_of_columns[in_old_label_colnr] + " ] = " +
					list_of_columns[in_new_label_colnr])
	
	#return result
	if options.o_debug_flag :
		print "dictionary_labels"
		print dictionary_labels
		
	return dictionary_labels
	


def process_file(args):

	#create dictionary
	dictionary_labels=construct_substitution_dictionary(args)

	for line in fileinput.input(args[0]):
		#process(line) with substitution dictionary
		#search for every old_label in line 
		for old_label, new_label in dictionary_labels.iteritems():

			#re.sub(pattern, repl, string, count=0, flags=0)
			line = re.sub('\\b'+re.escape(old_label)+'\\b',new_label,line)

		#print line to standard out
		print line

	#end of program


def main(args=None):

	# if no args are filled in use sensible defaulds
	if args is None:
		#not nessesary at the moment
		if options.o_verbose_flag :
			print "Using defaulds"

	process_file(args)

# main function
if __name__ == "__main__":

	args=process_command_line()

	if options.o_verbose_flag :
		now = datetime.datetime.now()
		print "Started at "+ now.strftime("%d-%m-%Y %H:%M")

	#Run main program
	main(args)

	if options.o_verbose_flag :
		now = datetime.datetime.now()
		print "Finished at "+ now.strftime("%d-%m-%Y %H:%M")
