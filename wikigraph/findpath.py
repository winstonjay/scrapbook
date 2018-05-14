#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
findpath.py:
Find a single path between two wikipedia articles and
output information about it to the stdout.
Set --help or -h flag for more info on cmd-line args.
eg: python findpath.py --help
'''
from __future__ import print_function
import argparse
from wikigraph import WikiGraph

def main():
    parser = construct_parser()
    args = parser.parse_args()
    start, end = args.start, args.end or "Homunculus"
    wiki_graph = WikiGraph()
    print("Searching:  '%s' -> '%s'" % (start, end))
    path = wiki_graph.find_path(start, end)
    print(path.print_stats() if path else "Failed Search.")

def construct_parser():
    # Set up argparse with start as a positional arg and end as optional.
    parser = argparse.ArgumentParser()
    s_help = "Title of valid wiki page to start from. E.g.'Santa Claus'"
    e_help = "Title of valid wiki page to end on default is 'Homunclus'"
    parser.add_argument("start", help=s_help, type=str)
    parser.add_argument("-e", "--end", help=e_help, type=str)
    return parser

if __name__ == '__main__':
    main()