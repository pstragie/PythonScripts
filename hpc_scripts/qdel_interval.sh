#!/bin/bash
#  6-2-2013 bart.verheyde@ugent.be v1.0
# Removes all jobs in the designated interval
# Its no desistar if you try to remove an unexisting job
# usage: qdel_interval.sh <start_job_nr> <end_job_nr>

start_job_nr=$1
end_job_nr=$2

for ((current_job_nr = $start_job_nr; $current_job_nr <= $end_job_nr; current_job_nr++)); do
    #echo $current_job_nr
    command_todo="qdel $current_job_nr "
    echo $command_todo
    $command_todo

done
