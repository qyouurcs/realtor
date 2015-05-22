#!/usr/bin/python

fn='tmp_graph.txt'
from wgraph import *
import pdb

G = load_edgelist(fn)

for i in build_corpus_iter(G, 100000, 10):
    str_i = [ str(ii) for ii in i]
    print ' '.join(str_i)

