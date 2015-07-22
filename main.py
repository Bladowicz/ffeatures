#!/usr/bin/python

import logging
import collections
import sys
import src


def get_occurences(inf):
    out = collections.Counter()
    for line in open(inf):
        line = line.strip().split('|')
        for part in line:
            part = part.split()[1:]
            print part

def filter_features(infile, outfile, minoccur, namespaces):
    with open(outfile, 'w') as fw:
        occurences = get_occurences(infile)

def main():
    config = src.input_parser.results
    filter_features(config.in_file, config.out_file, config.occurence,
                    config.namespaces)
    print config


if __name__=="__main__":
    main()
