#!/usr/bin/python

import geopy
import sys
import os
from math import exp

from geopy.distance import vincenty

if __name__== '__main__':

    if len(sys.argv) < 2:
        print 'Usage: {0} <dist-fn> [phi=0.5]'.format(sys.argv[0])
        sys.exit()

    dist_fn = sys.argv[1]
    phi = 0.5
    if len(sys.argv) >=3:
        phi = float(sys.argv[2])

    save_fn = os.path.splitext(dist_fn)[0] + '_sim-{0}.txt'.format(phi)
    with open(save_fn, 'w') as fidw:
        with open(dist_fn,'r') as fid:
            for aline in fid:
                aline = aline.strip()
                parts = aline.split()
                fidw.write(parts[0]+' ' + parts[1] + ' ' + str(exp( -float(parts[2])**2 / ( 2 * (phi ** 2)))) + '\n' )
                
    print 'Done with {0}'.format(save_fn)
