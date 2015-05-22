#!/usr/bin/python

'''
This script will build the batch data set for RNN.
'''
import ConfigParser
import numpy as np
import sys
import os
import math
import pdb

if __name__ == '__main__':

    cf = ConfigParser.ConfigParser()
    if len(sys.argv) < 2:
        print 'Usage: {0} <conf_fn>'.format(sys.argv[0])
        sys.exit()

    cf.read(sys.argv[1])
    fn_id_train = cf.get('INPUT', 'fn_id_train')
    fn_id_val = cf.get('INPUT', 'fn_id_val')
    fn_price = cf.get('INPUT', 'fn_price')
    fn_fea = cf.get('INPUT', 'fn_fea')
    fn_path = cf.get('INPUT', 'fn_path')

    save_dir = cf.get('OUTPUT', 'save_dir')
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # load id to dictionary dict_id
    dict_id_all = {}
    dict_id = {}
    idx = 0
    with open(fn_id_train,'r') as fid:
        for aline in fid:
            aline = aline.strip()
            dict_id_all[aline] = idx
            idx += 1

    with open(fn_id_val,'r') as fid:
        for aline in fid:
            aline = aline.strip()
            dict_id[aline] = idx
            dict_id_all[aline] = idx
            idx += 1

    dict_price = {}
    with open(fn_price,'r') as fid:
        for aline in fid:
            aline = aline.strip()
            parts = aline.split()
            price = parts[1].replace(',','')
            dict_price[parts[0]] =  float(price)

    T = -1
    fea_num = -1
    dict_fea = {}
    with open(fn_fea, 'r') as fid:
        for aline in fid:
            aline = aline.strip()
            parts = aline.split()
            fea = [ float(p) for p in parts[1:] ]
            dict_fea[parts[0]] =  fea
            if fea_num > 0 and fea_num != len(fea):
                print 'Should not happen'
                sys.exit()
            fea_num = len(fea)

    numpy_fea = np.zeros((idx, fea_num))
    numpy_label = np.zeros((idx, 1))

    for house in dict_id_all:
        numpy_fea[dict_id_all[house], :] = np.asarray(dict_fea[house])
        numpy_label[dict_id_all[house], 0] = dict_price[house]

    # Now, let's do the next job. 
    T = -1
    list_path = []
    with open(fn_path, 'r') as fid:
        for aline in fid:
            aline = aline.strip()
            parts = aline.split()
            T = len(parts)
            path = [ int(p) for p in parts ]
            list_path.append(path)

    # indeed, this is unnecessary, since we have built all paths randomly.
    #random.shuffle(list_path)

    batch_x = np.zeros( (T, len(list_path), fea_num), dtype=np.float32)
    batch_y = np.zeros( (T, len(list_path), 1), dtype = np.float32)

    cnt = 0
    for index in list_path:
        idx_fea = numpy_fea[index,:]
        idx_label = numpy_label[index,:]

        batch_x[:,cnt,:] = idx_fea
        batch_y[:,cnt,:] = idx_label
        cnt += 1

    batch_fn = os.path.join(save_dir,'batch-testing.npz')

    np.savez( batch_fn, batch_x = batch_x, batch_y = batch_y, fea_num=fea_num, batch_path = list_path, test_id = np.asarray(dict_id.values()))
    print 'Done with batch {0}'.format(batch_fn)
