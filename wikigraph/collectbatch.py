#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
collectbatch.py:
For a given sample of start articles find a path from each
to a central end article. Save the output to a given csv file.
Set --help or -h flag for more info on cmd-line args.
eg: python collectbatch.py --help.
'''
from __future__ import print_function
import argparse
import csv
from datetime import datetime
from wikigraph import WikiGraph


def main():
    parser = construct_parser()
    args = parser.parse_args()
    size = args.num or 1
    center = args.center or 'Homunculus'
    wg = WikiGraph(print_requests=True)
    sample = (load_sample(args.set, size) if args.source else
              wg.random_sample(size))
    results = {"start", "end", "path"}
    (ttime, treqs) = (datetime.now(), 0)
    with open(args.outfile, mode='w') as outfile:
        cs = csv.DictWriter(outfile, ["start", "end", "path", "degree"])
        cs.writeheader()
        for page in sample:
            print("Searching: '%s' -> '%s'" % (page, center))
            path = wg.find_path(page, center)
            path.print_stats()
            cs.writerow(path.data())
            treqs += path.requests
    ttime = (datetime.now() - ttime).total_seconds()
    print("Finished Totals:\nN={}. Time={}. Requests={}.".format(size, ttime, treqs))

def load_sample(filename, n):
    "return list from file of article names delimited by newlines."
    with open(filename, mode='r') as sample:
        return sample.read().strip().splitlines()[:n]

def construct_parser():
    parser = argparse.ArgumentParser()
    f_help = "Filename to save the results to."
    c_help = '''Title of valid wiki page to center all nodes from.
                default="Homunculus"'''
    n_help = "Sample size to collect. default=1."
    s_help = '''Filename containing newline delimited list of valid
                wiki article titles if not specified sample defaults
                to random selection from wikimedia api.'''
    parser.add_argument("outfile", help=f_help, type=str)
    parser.add_argument("-x", "--center", help=c_help, type=str)
    parser.add_argument("-s", "--source", help=s_help, type=str)
    parser.add_argument("-n", "--num", help=n_help, type=int)
    return parser

if __name__ == '__main__':
    main()