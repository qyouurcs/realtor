#!/usr/bin/python

import theanets
import numpy as np
import scipy.io
import sys
import pdb
import os



if __name__ == '__main__':
    if len(sys.argv) < 5:
        print 'Usage: {0} <comma-sparated-numbers> <saved_model> <pred_dir> <save_dir>'.format(sys.argv[0])
        sys.exit()

    layer_nums = sys.argv[1].split(',')
    layer_nums = [ int(num) for num in layer_nums ]

    model_fn = sys.argv[2]
    pred_dir = sys.argv[3]
    save_dir = sys.argv[4]
    
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    def fea_num():
        data = np.load(os.path.join(pred_dir,'batch-0.npz'))
        return data['fea_num']

    def layer(n):
        return dict(form='bidirectional', worker='lstm', size=n)

    fea_num_v = fea_num()
    lstm_layers = [ layer(num) for num in layer_nums]
    build_layers = [ fea_num_v]
    [ build_layers.append(lstm_layer) for lstm_layer in lstm_layers ]
    build_layers.append(1)
    build_layers = tuple(build_layers)

    e = theanets.Experiment(
        theanets.recurrent.Regressor,
        layers=build_layers
    )

    e = e.load(model_fn)

    def pred_one_fn(pred_fn):
        data = np.load(pred_fn)

        pred_x = data['batch_x']

        pred_y = e.predict(pred_x)

        pred_y = np.squeeze(pred_y)
        y = data['batch_y']
        y = np.squeeze(y)
        test_id = data['test_id']
        batch_path = data['batch_path']

        dict_test_id = {}
        for idx in test_id:
            dict_test_id[idx] = 1

        num_path = batch_path.shape[0]
        dict_pred_ys = {}
        dict_y = {}

        for i in range(num_path):
            path = batch_path[i,:]
            idx = 0
            for node in path:
                if node in dict_test_id:
                    if node not in dict_pred_ys:
                        dict_pred_ys[node] = []
                    if node not in dict_y:
                        dict_y[node] = y[idx,i]
                    else:
                        if y[idx,i] != dict_y[node]:
                            print 'Error! should not happen'
                            sys.exit()
                    dict_pred_ys[node].append(pred_y[idx,i])

                idx += 1
        return dict_pred_ys, dict_y 

    def nearest(array, value):
        idx = (np.abs(array - value)).argmin()
        return array[idx]


    # Now we have all the needed info.
    if pred_dir[-1] == '/':
        pred_dir = pred_dir[0:-1]

    save_fn = pred_dir.replace('/','') + '_' + os.path.splitext(os.path.basename(model_fn))[0] + '_pred.txt'
    save_fn = os.path.join(save_dir, save_fn)

    dict_pred_ys_all = {}
    dict_y_all = {}
    with open(save_fn,'w') as fid:
        for root, subdirs, fns in os.walk(pred_dir):
            for fn in fns:
                dict_pred_ys, dict_y = pred_one_fn(os.path.join(root, fn))
                for node in dict_pred_ys:
                    if node not in dict_pred_ys_all:
                        dict_pred_ys_all[node] = []
                    dict_pred_ys_all[node] = dict_pred_ys_all[node] + dict_pred_ys[node]

                for node in dict_y:
                    if node not in dict_y_all:
                        dict_y_all[node] = dict_y[node]
                    else:
                        if dict_y_all[node] != dict_y[node]:
                            print 'Error! should not happen'

            #scipy.io.savemat(save_fn, dict_save)
        for node in dict_pred_ys_all:
            pred_y = dict_pred_ys_all[node]
            avg = np.mean(np.asarray(pred_y))
            var = np.var(np.asarray(pred_y))
            print >> fid, node, dict_y_all[node], nearest(pred_y, dict_y_all[node]), avg, var,
            for y in pred_y:
                print >> fid, y,
            print >>fid

    print 'Done with {0}'.format(save_fn)
