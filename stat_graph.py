#!/usr/bin/python

fn='tmp_path.txt'

stat = {}
with open(fn, 'r') as fid:
    for aline in fid:
        aline = aline.strip()
        parts = aline.split()
        pre_part = parts[0]
        for part in parts[1:]:
            if pre_part not in stat:
                stat[pre_part] = {}
            if part not in stat[pre_part]:
                stat[pre_part][part] = 0
            stat[pre_part][part] += 1
            pre_part = part

for part in stat:
    sum_s = 0.0
    for part2 in stat[part]:
        sum_s += stat[part][part2]
    print 'start with {}'.format(part),
    for part2 in stat[part]:
        print part2,':',str(stat[part][part2] / sum_s),
    print
