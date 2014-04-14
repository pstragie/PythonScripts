#!/bin/bash
# 1-3-2013 bart.verheyde@ugent.be v0.1
#
# initilaizeerd mysql op cluster
# Load module
# install db
# create new config file lines
# copy org config file
# Modify config file
#
# @param=project_name=
# @param=mysql_data_dir including /
# init_mysql_on_hpc.sh project_name [mysql_data_dir including trailing /]
# init_mysql_on_hpc.sh project_cgi_1 
# init_mysql_on_hpc.sh project_cgi_2 $VSC_SCRATCH/mysql/


# // #PBS -N test_mysql
# // #PBS -S /bin/bash
# // #PBS -o /user/home/gent/vsc406/vsc40682/scratch/mysql/test_mysql.out
# // #PBS -e /user/home/gent/vsc406/vsc40682/scratch/mysql/test_mysql.err
# // #PBS -m abe
# // #PBS -q debug


project_name=$1
mysql_datadir=$2 #including trailing/ or leve empty and use default $VSC_SCRATCH/mysql/

######################################################################################
# NO changes lower than here!!!  (unless you know what your doing)
######################################################################################

# set default values
if [ -z ${project_name} ]
then
  project_name="mysql_on_hpc"
fi

# set default values
if [ -z ${mysql_datadir} ]
then
  mysql_datadir="$VSC_SCRATCH/mysql/"
fi

#init mysql envirement
DATADIR=${mysql_datadir}${project_name}
mkdir -p $DATADIR

#Load Mysql
module load MariaDB/5.5.29-ictce-4.1.13

cd $DATADIR
$EBROOTMARIADB/scripts/mysql_install_db --basedir=$EBROOTMARIADB --datadir=$DATADIR --user=$USER

cat <<EOF
[client]
socket=$DATADIR/mariadb.socket
[mysqld]
skip-networking
datadir=$DATADIR
socket=$DATADIR/mariadb.socket
user=$USER
[mysqld_safe]
log-error=$DATADIR/mariadb.log
pid-file=$DATADIR/mariadb.pid
EOF

#copy the huge example config (asssuming > 16GB of ram on node) 
cp $EBROOTMARIADB/support-files/my-large.cnf $DATADIR/mariadb.cnf

echo "Modify $DATADIR/mariadb.cnf with the data above!!" 
echo "To start:"
echo "$EBROOTMARIADB/bin/mysqld_safe --defaults-file=$DATADIR/mariadb.cnf >& $DATADIR/mariadb.startup.out & " 

#add soft link to db in directory that is in PATH niet nodig denk ik?
# mkdir -p~/mysql_dbs
# cd ~/mysql_dbs
# ln -s $DATADIR/

#add or replace the result of the cat section to mariadb.cnf

##Config db done

##Manual Start top reset
##http://hpc.ugent.be/userwiki/index.php/Tips:Software:MySQL#Preparations

###############
## Start DB ###
###############
# can only been done when .cnf file is edited

##Load mudule when not yet loaded see with 
#module list
#module load MariaDB/5.5.29-ictce-4.1.13

##SET $DATADIR if not yet done
#DATADIR=$VSC_SCRATCH/mysql/${project_name}
#DATADIR=$VSC_SCRATCH/mysql/cgi_cup_rals_compleet_only/

#IF DATADIR is set
#$EBROOTMARIADB/bin/mysqld_safe --defaults-file=$DATADIR/mariadb.cnf >& $DATADIR/mariadb.startup.out &

##ELSE DATADIR is not set
#$EBROOTMARIADB/bin/mysqld_safe --defaults-file=$VSC_SCRATCH/mysql/cgi_cup_rals_compleet_only/mariadb.cnf >& $VSC_SCRATCH/mysql/cgi_cup_rals_compleet_only/mariadb.startup.out &

###################
##Connect to Db ###
###################
#mysql --defaults-file=$DATADIR/mariadb.cnf

#######################
##DIS Connect to Db ###
#######################
#kill `cat $DATADIR/mariadb.pid`

