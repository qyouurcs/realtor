#!/usr/bin/python

import os
import sys
import glob
import pdb

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print 'Usage: {0} <fn_pattern>'.format(sys.argv[0])
        sys.exit()
    
    cnt_ = 0
    error_best = 0.0
    error_avg = 0.0

    for fn in glob.glob(sys.argv[1]):
        print fn
        with open(fn,'r') as fid:
            for aline in fid:
                parts = aline.split()
                best = float(parts[2])
                t = float(parts[1])
                avg = float(parts[3])

                error_best += abs((best - t) / t)
                error_avg += abs((avg - t) / t)
                cnt_ += 1

    error_best = error_best / cnt_
    error_avg = error_avg / cnt_
    print error_best, error_avg, error_best**.5, error_avg**.5


