#!/usr/bin/env python

import ConfigParser
import climate
import io
import numpy as np
import theanets
import scipy.io
import os
import tempfile
import urllib
import zipfile
import pdb
import glob
import random
import sys

logging = climate.get_logger('lstm-chime')

climate.enable_default_logging()

def main(layer_nums, data_dir, model_dir, val_fn, sep_data_dir, sep_val_fn, **kwargs):
    
    layer_nums = [ int(num) for num in layer_nums ]

    hidden_l1 = None
    if 'hidden_l1' in kwargs:
        hidden_l1 = float(kwargs['hidden_l1'])

    l1 = None

    if 'l1' in kwargs:
        l1 = float(kwargs['l1'])

    l2 = None
    if 'l2' in kwargs:
        l2 = float(kwargs['l2'])
        
    def batch_train():
        batches = glob.glob(data_dir + '/*')
        num_ = len(batches)
        idx = random.choice(range(1,num_))
        data = np.load( os.path.join(data_dir, 'batch-{0}.npz'.format(idx)))
        
        return [ data['batch_x'], data['batch_y'] ]
    
    def batch_val():
        data = np.load(val_fn)
        return [ data['batch_x'], data['batch_y'] ]
    
    def batch_train_sep():
        batches = glob.glob(sep_data_dir + '/*')
        num_ = len(batches)
        idx = random.choice(range(1,num_))
        data = np.load( os.path.join(sep_data_dir, 'batch-{0}.npz'.format(idx)))
        return [ data['batch_x'], data['batch_y'] ]
    
    def get_area_code():
        if sep_data_dir[-1] == '/':
            return os.path.basename(sep_data_dir[0:-1])
        return os.path.basename(sep_data_dir)

    def batch_val_sep():
        data = np.load(sep_val_fn)
        return [ data['batch_x'], data['batch_y'] ]
    
    def fea_num():
        data = np.load(os.path.join(data_dir, 'batch-0.npz'))
        return data['fea_num']
    def batch_size():
        data = np.load(os.path.join(data_dir, 'batch-0.npz'))
        return data['batch_size']
    
    def layer(n):
        return dict(form='bidirectional', worker='lstm', size=n)

    fea_num_v = fea_num()
    batch_size_v = batch_size()
    build_layers = [ fea_num_v]
    lstm_layers = [ layer(num) for num in layer_nums]
    [ build_layers.append(lstm_layer) for lstm_layer in lstm_layers ]
    build_layers.append(1)
    build_layers = tuple(build_layers)

    
    e = theanets.Experiment(
        theanets.recurrent.Regressor,
        layers=build_layers
    )
    
    layer_str = sys.argv[1].replace(',','-')
    #val_base = os.path.splitext(os.path.basename(val_fn))[0]
    if not os.path.isdir(model_dir):
        os.makedirs(model_dir)
    save_fn = os.path.join(model_dir, '{5}-models-{0}-{1}-{2}-{3}-{4}.pkl'.format(layer_str, batch_size_v, hidden_l1, l1, l2, get_area_code()))
    print save_fn
    e.train(
        batch_train,
        batch_val,
        algorithm='rmsprop',
        learning_rate=0.001,
        gradient_clip=1,
        train_batches=30,
        valid_batches=3,
        batch_size=batch_size_v,
        weight_l2 = l2,
        weight_l1 = l1,
        hidden_l1 = hidden_l1
    )

    e.train(batch_train_sep,
            batch_val_sep,
            algorithms = 'rmsprop',
            learning_rate = 0.00001,
            gradient_clip = 1e5,
            train_batches = 10,
            valid_batches = 2,
            batch_size = batch_size_v,
            weight_l2 = l2,
            weight_l1 = l1,
            hidden_l1 = hidden_l1
    )
    e.save(save_fn)

if __name__ == '__main__':

    cf = ConfigParser.ConfigParser()
    
    if len(sys.argv) < 4:
        print 'Usage: {0} <conf_fn> <sep_data_dir> <sep_val_fn> [hidden_l1 or l1 or l2]'.format(sys.argv[0])
        sys.exit()
    
    cf.read(sys.argv[1])
    layer_nums=cf.get('INPUT', 'layer_nums').split(',')
    data_dir=cf.get('INPUT', 'data_dir')
    val_fn=cf.get('INPUT', 'val_fn')
    model_dir=cf.get('OUTPUT','model_dir')

    sep_data_dir = sys.argv[2]
    sep_val_fn = sys.argv[3]

    idx_s = 4
    if len(sys.argv) > 5:
        if len(sys.argv[5]) == 1:
            idx_s = 5

    kwargs = dict(x.split('=', 1) for x in sys.argv[idx_s:])
    main(layer_nums, data_dir, model_dir, val_fn, sep_data_dir, sep_val_fn, **kwargs)

