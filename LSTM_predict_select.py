#!/usr/bin/python

import theanets
import numpy as np
import scipy.io
import sys
import pdb
import os

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print 'Usage: {0} <comma-sparated-numbers> <saved_model> <pred_data>'.format(sys.argv[0])
        sys.exit()

    layer_nums = sys.argv[1].split(',')
    layer_nums = [ int(num) for num in layer_nums ]

    model_fn = sys.argv[2]
    pred_fn = sys.argv[3]

    def fea_num():
        data = np.load(pred_fn)
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

    dict_pred_y_min_cost = {}
    dict_pred_y_min_idx = {}

    for i in range(num_path):
        path = batch_path[i,:]
        idx = 0
        cost = []
        node_t = -1
        for node in path:
            if node in dict_test_id:
                # all
                if node_t != -1:
                    print 'Error should not happen'
                    sys.exit()

                node_t = node
                if node not in dict_pred_ys:
                    dict_pred_ys[node] = []
                dict_pred_ys[node].append(pred_y[idx,i])

                if node not in dict_y:
                    dict_y[node] = y[idx,i]
                else:
                    if y[idx,i] != dict_y[node]:
                        print 'Error! should not happen'
                        sys.exit()
            else:
                cost.append( pred_y[idx, i] - y[idx, i])

            # Node.
            idx += 1

        cost = np.asarray(cost)
        if node_t not in dict_pred_y_min_cost:
            dict_pred_y_min_cost[node_t] = float('inf')
            dict_pred_y_min_idx[node_t] = dict_pred_ys[node_t][-1]

        if abs(cost.mean()) < dict_pred_y_min_cost[node_t]:
            dict_pred_y_min_cost[node_t] = cost.mean()
            dict_pred_y_min_idx[node_t] = dict_pred_ys[node_t][-1]

    # Now we have all the needed info.
    save_fn = os.path.splitext(pred_fn)[0] + '_' + os.path.splitext(os.path.basename(model_fn))[0] + '_pred.txt'

    def nearest(array, value):
        idx = (np.abs(array - value)).argmin()
        return array[idx]
    
    with open(save_fn,'w') as fid:
        for node in dict_pred_ys:
            pred_y = dict_pred_ys[node]
            avg = np.mean(np.asarray(pred_y))
            var = np.var(np.asarray(pred_y))
            print >> fid, node, dict_y[node], nearest(pred_y, dict_y[node]), dict_pred_y_min_idx[node], avg, var,
            for y in pred_y:
                print >> fid, y,
            print >>fid

        #scipy.io.savemat(save_fn, dict_save)

    print 'Done with {0}'.format(save_fn)

