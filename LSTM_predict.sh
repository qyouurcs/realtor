#!/usr/bin/env bash

if [ $# -lt 2 ]; then 
    echo "$0 <model_dir> <testing_fn>"
    exit
fi

model_dir=$1
testing_fn=$2

models=`ls $model_dir`

for model in $models
do
    echo $model
    params_conf=`echo $model | awk -F"-" '{layers=$2; for( i = 3; i < NF - 3; i++) layers = layers","$i; print layers;}'`
    model_fn=$model_dir/$model
    python LSTM_predict.py $params_conf $model_fn $testing_fn
done
