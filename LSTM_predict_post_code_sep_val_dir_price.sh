#!/usr/bin/env bash

if [ $# -lt 3 ]; then 
    echo "$0 <model_dir> <testing_dir> <save_dir>"
    exit
fi

model_dir=$1
testing_dir=$2
save_dir=$3

models=`ls $model_dir`

for model in $models
do
    #echo $model
    #params_conf=`echo $model | awk -F".conf" '{layers=$2; for( i = 3; i < NF - 3; i++) layers = layers","$i; print layers;}'`
    params_conf=`echo $model | awk -F".conf" '{layers=$1; print layers;}'`
    params=`echo $params_conf | awk -F"_" '{layers=$(NF-4); layers = layers","$(NF-3); print layers;}'`
    echo $params
    area_code=`echo $model | awk  -F"-" '{print $1;}'`
    model_fn=$model_dir/$model
    test_dir=$testing_dir/$area_code
    #python LSTM_predict_post_code.py $params_conf $model_fn $testing_dir
    python LSTM_predict_post_code_sep.py $params $model_fn $test_dir $save_dir
done
