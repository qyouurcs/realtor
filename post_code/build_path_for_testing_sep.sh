#/usr/bin/env bash

if [ $# -lt 4 ];then
    echo "$0 <sim_dir> <train_id> <val_id> <save_dir>"
    exit
fi

sim_fns=`ls $1`

for fn in $sim_fns
do
    ful_fn=$1/$fn
    python build_path_for_testing_sep.py $ful_fn $2 $3 $4
done
