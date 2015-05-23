#!/usr/bin/env bash

txts=`ls batch*.txt`

for txt in $txts
do
    cut -d" " -f1,2,3,4 $txt > cut_$txt
done
