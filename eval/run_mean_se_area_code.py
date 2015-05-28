#!/usr/bin/python

import os
import sys
import glob

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print 'Usage: {0} <fn_pattern>'.format(sys.argv[0])
        sys.exit()

    for fn in glob.glob(sys.argv[1]):
        cnt_ = 0
        error_best = 0.0
        error_avg = 0.0
        parts = os.path.basename(fn).split('_')
        area_code = parts[1]
        area_code = area_code.split('-')[0]
        with open(fn,'r') as fid:
            for aline in fid:
                parts = aline.split()
                best = float(parts[2])
                t = float(parts[1])
                avg = float(parts[3])

                error_best += (best - t) ** 2
                error_avg += (avg - t) ** 2
                cnt_ += 1

        error_best = error_best / cnt_
        error_avg = error_avg / cnt_
        #print area_code, error_best, error_avg, error_best**.5, error_avg**.5
        print area_code, error_avg, error_avg**.5


