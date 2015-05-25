#!/usr/bin/env python

import logging
import sys
from io import open
from os import path
from time import time
from glob import glob
from six.moves import range, zip, zip_longest
from six import iterkeys
from collections import defaultdict, Iterable
import random
from random import shuffle
from scipy.io import loadmat
from scipy.sparse import issparse
import numpy as np


logger = logging.getLogger("graph")

LOGFORMAT = "%(asctime).19s %(levelname)s %(filename)s: %(lineno)s %(message)s"

#weighted graph.
class Graph(defaultdict):

    """Efficient basic implementation of nx `Graph' Undirected graphs with self loops"""

    def __init__(self):
        super(Graph, self).__init__(list)

    def nodes(self):
        return self.keys()

    def adjacency_iter(self):
        return self.iteritems()

    def subgraph(self, nodes={}):
        subgraph = Graph()

        for n in nodes:
            if n in self:
                subgraph[n] = [x for x in self[n] if x in nodes]

        return subgraph

    def make_undirected(self):

        t0 = time()

        for v in self.keys():
            for other in self[v]:
                if v != other:
                    self[other[0]].append(tuple(v, other[1]))

        t1 = time()
        logger.info('make_directed: added missing edges {}s'.format(t1 - t0))

        self.make_consistent()
        return self

    def make_consistent(self):
        t0 = time()
        for k in iterkeys(self):
            self[k] = list(sorted(set(self[k])))

        t1 = time()
        logger.info('make_consistent: made consistent in {}s'.format(t1 - t0))

        self.remove_self_loops()

        return self

    def remove_self_loops(self):

        removed = 0
        t0 = time()

        for x in self:
            for y in self[x]:
                if y[0] == x:
                    self[x].remove(y)
                    removed += 1

        t1 = time()

        logger.info(
            'remove_self_loops: removed {} loops in {}s'.format(
                removed,
                (t1 - t0)))
        return self

    def check_self_loops(self):
        for x in self:
            for y in self[x]:
                if x == y[0]:
                    return True

        return False

    def has_edge(self, v1, v2):
        for v in self[v1]:
            if v[0] == v2:
                return True
        for v in self[v2]:
            if v[0] == v1:
                return True
        return False

    def degree(self, nodes=None):
        if isinstance(nodes, Iterable):
            return {v: len(self[v]) for v in nodes}
        else:
            return len(self[nodes])

    def order(self):
        "Returns the number of nodes in the graph"
        return len(self)

    def number_of_edges(self):
        "Returns the number of nodes in the graph"
        return sum([self.degree(x) for x in self.keys()]) / 2

    def number_of_nodes(self):
        "Returns the number of nodes in the graph"
        return order()

    def random_walk(
            self,
            path_length,
            alpha=0,
            rand=random.Random(),
            start=None):
        """ Returns a truncated random walk.
            path_length: Length of the random walk.
            alpha: probability of restarts.
            start: the start node of the random walk.
        """
        G = self
        path_np = np.zeros((path_length,),dtype=int)
        if start:
            #path = [start]
            path_np[0] = start
        else:
            # Sampling is uniform w.r.t V, and not w.r.t E
            #path = [rand.choice(G.keys())]
            path_np[0] = rand.choice(G.keys())
        
        cur_len = 1

        while cur_len < path_length:

            cur = path_np[cur_len-1]
            if len(G[cur]) > 0:
                # proportionally sample from one of its neighbors.
                prob_np = np.zeros((len(G[cur]),))
                node_idx_np = np.zeros((len(G[cur]),),dtype=int)
                vidx = 0
                for v in G[cur]:
                    #p.append(v[1])
                    prob_np[vidx] = v[1]
                    node_idx_np[vidx] = v[0]
                    vidx += 1

                prob_np = prob_np / np.sum(prob_np)
                r = random.random()

                p_s = 0.0
                idx = 0
                for p_a in prob_np:
                    p_s += p_a
                    if p_s > r:
                        break
                    idx += 1
                path_np[cur_len] = node_idx_np[idx]
                cur_len += 1
            else:
                break
        return path_np


def build_corpus(G, num_paths, path_length, alpha=0,
                 rand=random.Random(0)):
    walks = []
    nodes = list(G.nodes())

    for cnt in range(num_paths):
        rand.shuffle(nodes)
        for node in nodes:
            walks.append(
                G.random_walk(
                    path_length,
                    rand=rand,
                    alpha=alpha,
                    start=node))

    return walks

def build_corpus_iter(G, num_paths, path_length, alpha=0,
                      rand=random.Random(0)):
    walks = []
    nodes = list(G.nodes())
    for cnt in range(num_paths):
        rand.shuffle(nodes)
        node = nodes[0]
        yield G.random_walk(path_length, rand=rand, alpha=alpha, start = node)
        #for node in nodes[0]:
        #    yield G.random_walk(path_length, rand=rand, alpha=alpha, start=node)

def load_edgelist_from_list(edge_list, undirected = True):
    G = Graph()
    for edge in edge_list:
        x,y, w = edge.split()
        x = int(x)
        y = int(y)
        w = float(w)
        G[x].append((y,w))
        if undirected:
            G[y].append((x,w))
    G.make_consistent()
    return G
def load_edgelist(file_, undirected=True):
    G = Graph()
    with open(file_) as f:
        for l in f:
            x, y, w = l.strip().split()
            x = int(x)
            y = int(y)
            w = float(w)
            G[x].append((y, w))
            if undirected:
                G[y].append((x, w))

    G.make_consistent()
    return G

def load_matfile(file_, variable_name="network", undirected=True):
    mat_varables = loadmat(file_)
    mat_matrix = mat_varables[variable_name]
    return from_numpy(mat_matrix, undirected)

def from_numpy(x, undirected=True):
    G = Graph()
    if issparse(x):
        cx = x.tocoo()
        for i, j, v in zip(cx.row, cx.col, cx.data):
            G[i].append((j, v))
    else:
        raise Exception("Dense matrices not yet supported.")

    if undirected:
        G.make_undirected()
    G.make_consistent()
    return G
