#!/usr/bin/python

from wgraph import *
import pdb
import sys
import os
import datetime

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print 'Usage: {0} <sim_fn> <train_id> <val_id> [num_path_per_node=2] [len_p=10]'.format(sys.argv[0])
        sys.exit()

    num_p_node = 2
    len_p = 10
    if len(sys.argv) >= 5:
        num_p_node = int(sys.argv[4])
    if len(sys.argv) >= 6:
        len_p = int(sys.argv[5])

    dict_id_code = {}
    idx = 0
    with open(sys.argv[2],'r') as fid:
        for aline in fid:
            aline = aline.strip()
            parts = aline.split()
            dict_id_code[idx] = int(parts[-1])
            idx += 1

    dict_val = {}

    with open(sys.argv[3],'r') as fid:
        for aline in fid:
            aline = aline.strip()
            parts = aline.split()
            dict_val[idx] = parts[0]
            dict_id_code[idx] = int(parts[-1])
            idx += 1

    dict_graph = {}
    with open(sys.argv[1],'r') as fid:
        for aline in fid:
            aline = aline.strip()
            parts = aline.split()
            code = dict_id_code[int(parts[0])]
            code2 = dict_id_code[int(parts[0])]
            if code != code2:
                print 'Error should not happen'
                sys.exit()
            if code not in dict_graph:
                dict_graph[code] = []
            dict_graph[code].append(aline)

    ts = datetime.datetime.now()
    ts = str(ts)
    ts = ts.replace(' ','_')
    ts = ts.replace(':','_')
    save_fn = os.path.splitext(os.path.basename(sys.argv[1]))[0] + '_testing-path-{0}-{1}-{2}.txt'.format(num_p_node,len_p, ts)
    fid = open(save_fn,'wb')

    for code in dict_graph:
        edge_list = dict_graph[code]
        G = load_edgelist_from_list(dict_graph[code])

        for i in build_corpus_iter(G, num_p_node * len(dict_graph[code]), len_p):
            is_p = 0
            for ii in i:
                if ii in dict_val:
                    is_p += 1
            if is_p == 1: # one and only one.
                str_i = [ str(ii) for ii in i]
                print >>fid, ' '.join(str_i)
    fid.close()

    print 'Done with {0}'.format(save_fn)
