#!/bin/bash
#
# Fils the first colom/ field of list2matrix result -> using codes to be 10 carachters long filed out with spaces
#
#
# usage: to_phylip <input_file> 

# define helper variables
input_file="$1"

awk '
{
#$0 compleet line
# get first colom $1

bacterie_code_short=$1

  #give error when $1 is longer than 10
  if(length(bacterie_code_short) > 10){
	#to long give error
	print bacterie_code_short " is to long maximum 10 long for converting into valid phylip format.\n Tip: use create_lable_list_dir folowed by  relable_file.sh"
	exit 1
  }
  else{
	#modify $1 to be 10 caracters long filled out with spaces
	bacterie_code_long= sprintf("%-10s",bacterie_code_short)
  }

  # find replace in $0 old value $1 with new long$1
  sub(bacterie_code_short,bacterie_code_long,$0)

  #print result
  print $0

}' $1
