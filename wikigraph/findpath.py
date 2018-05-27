# -*- coding: utf-8 -*-
'''
findpath.py :
Find a single path between two wikipedia articles and
output information about it to the stdout.

usage: Find a path between two Wikipedia pages via their links.
       [-h] --start START --end END

optional arguments:
  -h, --help     show this help message and exit
  --start START  Title of valid wikipedia page to start from.
  --end END      Title of valid wikipedia page to reach.
'''
from __future__ import print_function

import argparse

from wikigraph import WikiGraph

def main():
    parser = argparse.ArgumentParser(
        "Find a path between two Wikipedia pages via their links.")
    parser.add_argument(
        "--start",
        help="Title of valid wikipedia page to start from.",
        type=str,
        required=True)
    parser.add_argument(
        "--end",
        help="Title of valid wikipedia page to reach.",
        type=str,
        required=True)
    args = parser.parse_args()

    wiki_graph = WikiGraph()
    print("Searching:  '%s' -> '%s'" % (args.start, args.end))
    path = wiki_graph.find_path(args.start, args.end)
    if path:
        print(path.info)
    else:
        print("Failed Search.")

if __name__ == '__main__':
    main()