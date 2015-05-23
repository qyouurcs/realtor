#!/usr/bin/env bash

if [ $# -lt 1 ]; then
    echo $0" <base_dir>"
    exit
fi

base_dir=$1

txts=`ls ${base_dir}/batch*.txt`


for txt in $txts
do
    
    base_name=`basename $txt`
    cut -d" " -f1,2,3,4 $txt > ${base_dir}/cut_$base_name
done
