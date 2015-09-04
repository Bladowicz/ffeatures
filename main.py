#!/usr/bin/python

import logging
import collections
import sys
import src
from bisect import bisect_left

def progressbar(it, prefix = "", size = 60):
    count = len(it)
    def _show(_i):
        x = int(size*_i/count)
        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), _i, count))
        sys.stdout.flush()

    _show(0)
    for i, item in enumerate(it):
        yield item
    _show(i+1)
    sys.stdout.write("\n")
    sys.stdout.flush()


def get_occurences(inf):
    out = collections.Counter()
    logging.info('Counting occurences')
    for line in open(inf):
        line = line.strip().split('|')[1:]
        l = set()
        for part in line:
            part = part.split()[1:]
            l.update(part)
        for k in l:
            out[k] += 1
    return out

def do_filtering(inf, good):
    for line in open(inf):
        line = line.rstrip('\r\n').split('|')
        out = [line[0]]
        for part in line[1:]:
            part = part.split()
            part = [part[0]] + sorted(good.intersection(set(part[1:])))
            out.append(' '.join(part))
        yield ' |'.join(out)+'\n'

def load_bad(inf):
    return set([x.strip() for x in open(inf)])


def filter_features(infile, outfile, minoccur, bad_file=None):
    minoccur = int(minoccur)
    occ = occurences = get_occurences(infile)
    occ = sorted(occ.iteritems(), key=lambda x: x[1])
    total = len(occ)
    ddd = [x[1] for x in occ]
    good_features = set((x[0] for x in occ[bisect_left(ddd, minoccur):]))
    good = len(good_features)
    logging.info('Out of {} features, {} were good'.format(total, good))
    if bad_file:
         bad = load_bad(bad_file)
         logging.info('Out of {} features marked as bad, {} were removed'.format(len(bad), 
             len(good_features.intersection(bad)) ))
         good_features.difference_update()

    with open(outfile, 'w') as fw:
        logging.info('Removing from matrix')
        for line in do_filtering(infile, good_features):
            fw.write(line)

def main():

    config = src.input_parser._get()
#    logging.info(str(config))
    #config = src.input_parser.results
    filter_features(config.in_file, config.out_file, config.mincount, config.bad_file)
    


if __name__=="__main__":
    main()
