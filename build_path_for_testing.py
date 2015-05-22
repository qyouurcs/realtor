#!/usr/bin/python

from wgraph import *
import pdb
import sys
import os
import datetime

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print 'Usage: {0} <edge_list> <train_id> <val_id> [num_path_per_node=100] [len_p=10]'.format(sys.argv[0])
        sys.exit()

    num_p = 100 
    len_p = 10
    if len(sys.argv) >= 5:
        num_p = int(sys.argv[4])
    if len(sys.argv) >= 6:
        len_p = int(sys.argv[5])

    idx = 0
    with open(sys.argv[2],'r') as fid:
        for aline in fid:
            aline = aline.strip()
            idx += 1


    dict_val = {}
    num_s = 0
    with open(sys.argv[3],'r') as fid:
        for aline in fid:
            aline = aline.strip()
            dict_val[idx] = aline
            idx += 1
            num_s += 1

    num_s *= num_p

    num_t = num_s * 100 # ensure enough iterations of the whole random walks.

    fn = sys.argv[1]
    G = load_edgelist(fn)
    ts = datetime.datetime.now()
    ts = str(ts)
    ts = ts.replace(' ','_')
    ts = ts.replace(':','_')
    save_fn = os.path.splitext(os.path.basename(fn))[0] + '_testing-path-{0}-{1}-{2}.txt'.format(num_p,len_p, ts)
    fid = open(save_fn,'wb')
    back_stdout = sys.stdout

    idx_c = 0
    for i in build_corpus_iter(G, num_t, len_p):
        is_p = 0
        for ii in i:
            if ii in dict_val:
                #is_p = True
                is_p += 1
        if is_p == 1: # one and only one.
            str_i = [ str(ii) for ii in i]
            print >>fid, ' '.join(str_i)
            idx_c += 1
            if idx_c >= num_s:
                break

    fid.close()
    
    sys.stdout = back_stdout

    print 'Done with {0}'.format(save_fn)
