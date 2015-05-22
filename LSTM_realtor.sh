#!/usr/bin/env bash

if [ $# -lt 4 ]; then
#    echo "Usage: $0 <comma-speparated-layers> <batches_dir> [gpu=0]"
    echo "Usage: $0 <comma-sparated-numbers> <batches_dir> <model_dir> <val_fn> [gpu=0] [hidden_l1 or l1 or l2]"
    exit
fi

batch_dir=$2

param="$@"

param=`echo "$param" | awk '{gsub(" +", "-", $0); gsub("/", "_", $0); print $0;}'`

gpu=0
if [ $# -ge 5 ]; then
    gpu=$5
fi

batch_id=`basename $batch_dir`

##THEANO_FLAGS="device=gpu$gpu" python LSTM_realtor.py $1 $2 > logs/lstm-${1}-${batch_id}.log
THEANO_FLAGS="device=gpu$gpu" python LSTM_realtor.py "$@" > logs/lstm-${param}.log

