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
    fn_id = cf.get('INPUT', 'fn_id')
    fn_price = cf.get('INPUT', 'fn_price')
    fn_fea = cf.get('INPUT', 'fn_fea')
    fn_path = cf.get('INPUT', 'fn_path')
    batch_size = int(cf.get('INPUT', 'batch_size'))

    save_dir = cf.get('OUTPUT', 'save_dir') + '-' + str(batch_size)
    
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    
    # load id to dictionary dict_id
    dict_id = {}
    idx = 0
    with open(fn_id,'r') as fid:
        for aline in fid:
            aline = aline.strip()
            parts = aline.split()
            dict_id[parts[0]] = idx
            idx += 1

    dict_price = {}
    with open(fn_price,'r') as fid:
        for aline in fid:
            aline = aline.strip()
            parts = aline.split()
            price = parts[1].replace(',','')
            avg_price = parts[2].replace(',','')
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

    numpy_fea = np.zeros((len(dict_id), fea_num))
    numpy_label = np.zeros((len(dict_id), 1))

    for house in dict_id:
        numpy_fea[dict_id[house], :] = np.asarray(dict_fea[house])
        numpy_label[dict_id[house], 0] = dict_price[house]

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

    batch_x = np.zeros( (T, batch_size, fea_num), dtype=np.float32)
    batch_y = np.zeros( (T, batch_size, 1), dtype = np.float32)

    batch_num = int(math.floor( len(list_path) / float(batch_size))) # just discard the last paths.
    for batch_idx in xrange(batch_num):
        idx = list_path[batch_idx * batch_size : (batch_idx + 1 ) * batch_size]

        cnt = 0
        for index in idx:
            idx_fea = numpy_fea[index,:]
            idx_label = numpy_label[index,:]

            batch_x[:,cnt,:] = idx_fea
            batch_y[:,cnt,:] = idx_label
            cnt += 1

        batch_fn = os.path.join(save_dir,'batch-{0}'.format(batch_idx))
        batch_path = list_path[batch_idx * batch_size : (batch_idx + 1 ) * batch_size]

        np.savez( batch_fn, batch_x = batch_x, batch_y = batch_y, batch_idx = batch_idx, fea_num=fea_num, batch_size = batch_size, batch_path = batch_path)
        print 'Done with batch {0}'.format(batch_fn)
