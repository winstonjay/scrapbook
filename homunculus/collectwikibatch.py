from __future__ import print_function
import argparse
import csv
from datetime import datetime
from wikipathfinder import *


def main():
    parser = construct_parser()
    args = parser.parse_args()
    size = args.number or 50
    center = args.center or 'Homunculus'
    sample = (load_sample(args.set, size) if args.set else
              wiki_random_sample(size))
    wpf = WikiPathFinder(print_requests=True)
    results = {"start", "end", "path"}
    ttime = datetime.now()
    treqs = 0
    with open(args.outfile, mode='w') as outfile:
        cs = csv.DictWriter(outfile, ["start", "end", "path", "degree"])
        cs.writeheader()
        for page in sample:
            print("Searching:  '%s' -> '%s'" % (page, center))
            path = wpf.find_path(page, center)
            path.print_stats()
            cs.writerow(path.data())
            treqs += path.requests
    ttime = (datetime.now() - ttime).total_seconds()
    print("Finished Totals:\nN={}. Time={}. Requests={}.".format(size, ttime, treqs))

def load_sample(filename, n):
    with open(filename, mode='r') as sample:
        return sample.read().strip().splitlines()[:n]

def construct_parser():
    parser = argparse.ArgumentParser()
    f_help = "file to save the results."
    c_help = """Title of valid wiki page to center all nodes from. E.g.'Santa Claus',\
                default is set to 'Homunculus'"""
    n_help = "Sample size to collect. default is set to 50."
    s_help = """Sample Set to collect, default is a random sample from wikimedia api.
Alternatively specify a filename containing a list."""
    parser.add_argument("outfile", help=f_help, type=str)
    parser.add_argument("-x", "--center", help=c_help, type=str)
    parser.add_argument("-s", "--set", help=s_help, type=str)
    parser.add_argument("-n", "--number", help=n_help, type=int)
    return parser

if __name__ == '__main__':
    main()