#/usr/bin/env bash

param="l1=0.001 l2=0.0001"
conf_fn="sep_san_jose_realtor_200_100_val_dir_high_low.conf"
post_sep="Batches-San-Jose-train-deep-post-code-high-low-sep-1024"
val_dir="Batches-San-Jose-train-deep-post-code-high-low-sep-1024"

log_dir="log_sep_val_dir_high_low"

area_code=`ls $post_sep`

param_s=`echo "$param" | awk '{gsub(" +", "-", $0); gsub("/", "_", $0); print $0;}'`
conf=`echo ${conf_fn} | awk -F\. '{print $1}'`

area_cnt=`ls $post_sep | wc -l`

idx=1
for code in $area_code
do
    gpu=`echo $idx | awk '{if( $0 % 2) print 1; else print 0}'`
    code_dir=$post_sep/$code
    val_fn=$val_dir/$code/batch-0.npz
    cmd="\"THEANO_FLAGS=device=gpu"$gpu\"" python LSTM_realtor_sep.py "$conf_fn" "$code_dir" "$val_fn" $param > "${log_dir}/${conf}_${code}_${param_s}".log"
    #THEANO_FLAGS="device=gpu$gpu" python LSTM_realtor_sep.py $conf_fn $code_dir $val_fn $param > ${log_dir}/${conf}_${code}_${param_s}.log &
    echo $cmd
    idx=`echo $idx" + 1" | bc`
    
    if [ $idx -eq $area_cnt ]; then
        THEANO_FLAGS="device=gpu$gpu" python LSTM_realtor_sep_val_dir.py $conf_fn $code_dir $val_fn $param > ${log_dir}/${conf}_${code}_${param_s}.log &
    else
        THEANO_FLAGS="device=gpu$gpu" python LSTM_realtor_sep_val_dir.py $conf_fn $code_dir $val_fn $param > ${log_dir}/${conf}_${code}_${param_s}.log &
    fi
done
