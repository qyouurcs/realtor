#!/usr/bin/python

import geopy
import sys
import os
import pdb

from geopy.distance import vincenty

if __name__== '__main__':

    if len(sys.argv) < 3:
        print 'Usage: {0} <lat_long.txt> <san-jose-420-price-filtered-area-code_train.txt> [ dist = 5 miles]'.format(sys.argv[0])
        sys.exit()

    dist = 5.0
    fn = sys.argv[1]
    fn_id = sys.argv[2]
    if len(sys.argv) > 3:
        dist = float(sys.argv[3])

    '''
    Line number in $fn is the idx for each property.
    '''
    dict_idx = {}
    idx = 0
    dict_c = {}

    idx = 0
    
    with open(fn_id, 'r') as fid:
        for aline in fid:
            aline = aline.strip()
            parts = aline.split()
            #dict_idx[idx] = parts[0]
            dict_idx[parts[0]] = idx
            idx += 1

    with open(fn,'r') as fid:
        for aline in fid:
            aline = aline.strip()
            parts = aline.split()
            dict_c[parts[0]] = (float(parts[1]), float(parts[2]))
    dict_code = {}
    with open(fn_id, 'r') as fid:
        for aline in fid:
            aline = aline.strip()
            parts = aline.split()
            if parts[-1] not in dict_code:
                dict_code[parts[-1]] = []
            dict_code[parts[-1]].append(parts[0])

    save_fn = os.path.splitext(fn)[0] + '_dist-{0}_{1}.txt'.format(dist, os.path.splitext(fn_id)[0])
    # Now, start to calculate the distance between different properties. 
    with open(save_fn,'w') as fid:
        for code in dict_code:
            len_code = len(dict_code[code])
            for i in range(len_code):
                for j in range(i+1,len_code):
                    dist_ = vincenty(dict_c[dict_code[code][i]], dict_c[dict_code[code][j]])
                    if dist_ < dist:
                        print >>fid, dict_idx[dict_code[code][i]],dict_idx[dict_code[code][j]],dist_.miles
    print 'Done with {0}'.format(save_fn)
