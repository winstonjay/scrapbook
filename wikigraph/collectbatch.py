#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
collectbatch.py:
For a given sample of articles find a path from each
to a central end article. Write the output to a given csv file.
Set --help or -h flag for more info on cmd-line args.

'''
from __future__ import print_function

import csv
import argparse
from datetime import datetime

from wikigraph import WikiGraph


def main():
    # initialise args from cli
    parser = argparse.ArgumentParser(
        "For a given sample of articles find a path from each to a central end"
        " article. Write the output to a given csv file.")
    parser.add_argument(
        "-o",
        "--outfile",
        help="Filename to save the results to.",
        type=str,
        default="wikiresults.json")
    parser.add_argument(
        "-x",
        "--center",
        help="Title of valid wiki page to center all nodes on",
        type=str,
        default="Homunculus")
    parser.add_argument(
        "-k",
        "--sample_size",
        help="Sample size of k pages to search from. "
             "(Only applies when sample source is not given)",
        type=int,
        default=1)
    parser.add_argument(
        "-s",
        "--sample_source",
        help="Filename containing newline delimited list of valid "
             "wiki article titles if not specified sample defaults "
             "to random selection from wikimedia api. ",
        type=str)
    parser.add_argument(
        "-v",
        action='store_true',
        help="add to display titles of page requests made.")
    args = parser.parse_args()


    wiki_graph = WikiGraph(print_requests=True)

    # resolve any issues with search sample source.
    if args.sample_source:
        sample = load_sample(args.set)
        size = len(sample)
    else:
        sample = wiki_graph.random_sample(args.sample_size)
        size = args.sample_size

    with open(args.outfile, mode='w') as outfile:
        writer = csv.DictWriter(outfile, ["start", "end", "path", "degree"])
        writer.writeheader()

        total_time = datetime.now()
        total_requests = 0

        for i, page in enumerate(sample):
            print("%d/%d Searching: '%s' -> '%s'" % (i+1, size, page, args.center))
            path = wiki_graph.find_path(page, args.center)
            print(path.info)
            writer.writerow(path.data)
            total_requests += path.requests

        total_time = (datetime.now() - total_time).total_seconds()
        print("Finished Totals: "
              "N={}. Time={}. Requests={}.".format(
                args.sample_size, total_time, total_requests))


def load_sample(filename):
    "return list from file of article names delimited by newlines."
    with open(filename, mode='r') as sample:
        return sample.read().strip().splitlines()


if __name__ == '__main__':
    main()