import argparse
from wikipathfinder import *

def main():
    parser = construct_parser()
    args = parser.parse_args()
    start = args.start
    end = "Homunculus" if not args.end else args.end
    use_history = args.cache if args.cache is not None else True
    print("Searching:  '%s' -> '%s'" % (start, end))
    pathfinder = WikiPathFinder(use_history=use_history)
    data = pathfinder.find_path(start, end)
    if data:
        pathfinder.print_stats()
    else:
        print("Failed Search.")

def construct_parser():
    # Set up argparse with start as a positional arg and end as optional.
    parser = argparse.ArgumentParser()
    s_help = "Title of valid wiki page to start from. E.g.'Santa Claus'"
    e_help = "Title of valid wiki page to end on default is 'Homunclus'"
    c_help = "Set to false to disable caching results."
    parser.add_argument("start", help=s_help, type=str)
    parser.add_argument("-e", "--end", help=e_help, type=str)
    parser.add_argument("-c", "--cache", help=c_help, type=bool)
    return parser

if __name__ == '__main__':
    main()