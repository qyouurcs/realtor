#!/usr/bin/python

import os
import sys

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print 'Usage: {0} <san-jose-420-price-filtered.txt> <post_area_cnt.txt> [cnt_threshold=100]'.format(sys.argv[0])
        sys.exit()

    fn_price = sys.argv[1]
    fn_cnt = sys.argv[2]
    th = 100
    if len(sys.argv) >= 4:
        th = int(sys.argv[3])

    with open(fn_price, 'r') as fid:
        for aline in fid:
            aline = aline.strip()
            parts = aline.split()

    dict_area_cnt = {}
    with open(fn_cnt,'r') as fid:
        for aline in fid:
            parts = aline.split()
            dict_area_cnt[parts[0]] = int(parts[1])

    save_fn = os.path.splitext(sys.argv[1])[0] + '-area-code.txt'

    with open(save_fn, 'w') as wfid:
        with open(fn_price,'r') as fid:
            for aline in fid:
                aline = aline.strip()
                parts = aline.split()
                if dict_area_cnt[parts[-1]] > th:
                    #print >> wfid, parts[0], float(parts[1]) - float(parts[2])
                    print >> wfid, aline
    print "Done with {0}".format(save_fn)
