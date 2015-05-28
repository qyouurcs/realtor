#!/usr/bin/python
import os
import sys
import glob

if __name__ == '__main__':

    if len(sys.argv) < 4:
        print "Usage: {0} <cut_dir> <san-jose-420...train.txt> <san-jose-420-price-filtered-area-code_val.txt> <save_dir>".format(sys.argv[0])
        sys.exit()

    dict_id_price = {}
    save_dir = sys.argv[4]

    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)

    idx = 0
    with open(sys.argv[2],'r') as fid:
        for aline in fid:
            aline = aline.strip()
            parts = aline.split()
            idx += 1

    with open(sys.argv[3],'r') as fid:
        for aline in fid:
            aline = aline.strip()
            parts = aline.split()
            dict_id_price[idx] = float(parts[1])
            idx += 1

    fns = glob.glob( os.path.join(sys.argv[1], 'cut*.txt'))

    for fn in fns:
        wfid = open(os.path.join(save_dir, os.path.basename(fn)),'w')
        with open(fn, 'r') as fid:
            for aline in fid:
                aline = aline.strip()
                parts = aline.split()
                best_diff = float(parts[2]) - float(parts[1])
                avg_diff = float(parts[3]) - float(parts[1])
                price = dict_id_price[int(parts[0])]
                print >>wfid, parts[0], abs(best_diff) / price, abs(avg_diff)/price, price, best_diff, avg_diff
        wfid.close()

        print 'Done with {0}'.format(os.path.join(save_dir, os.path.basename(fn)))
