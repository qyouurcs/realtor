#!/usr/bin/python

import sys
import os
import random

if __name__ == '__main__':

    if len(sys.argv) < 2:
        print 'Usage: {0} <id.txt> [test_ratio=0.2]'.format(sys.argv[0])
        sys.exit()

    fn_id = sys.argv[1]
    test_ratio = 0.2

    list_ids = []
    with open(fn_id,'r') as fid:
        for aline in fid:
            aline = aline.strip()
            list_ids.append(aline)

    random.shuffle(list_ids)

    num_samples = len(list_ids)
    num_test = int(num_samples * test_ratio)
    num_train = num_samples - int(num_samples * test_ratio)

    prefix = os.path.splitext(fn_id)[0]

    train_fn = prefix + '_train.txt'
    test_fn = prefix + '_val.txt'

    with open(test_fn, 'w') as fid:
        for i in range(num_test):
            fid.write( list_ids[i] + '\n')

    with open(train_fn, 'w') as fid:
        for i in range(num_test, num_samples):
            fid.write( list_ids[i] + '\n')

    print 'Done with {0} and {1}'.format(train_fn, test_fn)
