#!/usr/bin/env bash

if [ $# -lt 3 ]; then
    echo "$0 <sim_dir> <san-jose-420-price-filtered-area-code_train.txt> <save_dir>"
    exit
fi

sim_fns=`ls $1`

for fn in $sim_fns
do
    ful_fn=$1/$fn
    python build_path_sep.py $ful_fn $2 $3
done

