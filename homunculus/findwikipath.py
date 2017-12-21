from __future__ import print_function
import argparse
from wikipathfinder import *

def main():
    parser = construct_parser()
    args = parser.parse_args()
    start = args.start
    end = args.end or "Homunculus"
    print("Searching:  '%s' -> '%s'" % (start, end))
    pathfinder = WikiPathFinder()
    # returns path or empty list.
    path = pathfinder.find_path(start, end)
    if path:
        path.print_stats()
    else:
        print("Failed Search.")

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