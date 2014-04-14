#!/bin/bash -x

#PBS -N testcgi_DBconn
#PBS -q debug
#PBS -m abe
#PBS -l walltime=00:59:00
#PBS -l nodes=1:ppn=1


# submit this job script to raichu (Intel Sandy Bridge CPUs)
# $ module swap cluster/raichu
# $ qsub sleep_job.sh

# log in on the workernode where the job is running
#
# $ qstat -an
#
# master13.raichu.gent.vsc: 
#                                                                          Req'd  Req'd   Elap
# Job ID               Username Queue    Jobname          SessID NDS   TSK Memory Time  S Time
# -------------------- -------- -------- ---------------- ------ ----- --- ------ ----- - -----
# 44096.master13.r     vsc40023 long     SWPC13                0     1  16    --  36:00 R   -- 
#    node829+node829+node829+node829+node829+node829+node829+node829+node829
#    +node829+node829+node829+node829+node829+node829+node829
#
# $ ssh node829.raichu.gent.vsc

# make sure you're really at the raichu workernode

# $ hostname
# node829.raichu.os

#shange sleep lenght to need in seconds
sleep 3500000 
