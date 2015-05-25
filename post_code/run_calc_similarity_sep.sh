#!/usr/bin/env bash

if [ $# -lt 2 ]; then
    echo "$0 <dist_dir> <save_sim_dir>"
    exit
fi

dist_fns=`ls $1`

for fn in $dist_fns
do
    ful_fn=$1/$fn
    python run_calc_similarity_sep.py $ful_fn $2
done
