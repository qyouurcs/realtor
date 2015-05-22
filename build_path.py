#!/usr/bin/python

from wgraph import *
import pdb
import sys
import os


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print 'Usage: {0} <edge_list> [num_path=200000] [len_p=10]'.format(sys.argv[0])
        sys.exit()
    num_p = 200000
    len_p = 10
    if len(sys.argv) >= 3:
        num_p = int(sys.argv[2])
    if len(sys.argv) >= 4:
        len_p = int(sys.argv[3])

    fn = sys.argv[1]
    G = load_edgelist(fn)

    save_fn = os.path.splitext(os.path.basename(fn))[0] + '_path-{0}-{1}.txt'.format(num_p,len_p)
    fid = open(save_fn,'wb')
    back_stdout = sys.stdout

    for i in build_corpus_iter(G, num_p, len_p):
        str_i = [ str(ii) for ii in i]
        print >>fid, ' '.join(str_i)

    fid.close()
    
    sys.stdout = back_stdout

    print 'Done with {0}'.format(save_fn)
