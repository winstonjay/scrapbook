"""
How many click's away from the Homunculus?

The following aims to find the degree's for seperation between wikipedia
articles with the default end node set on the article 'Homunculus'. If found
it then prints the results to the screen.

TODO:
    Clean up the mess you made last time...

    In wiki_request_links():
    *   Allow handling for wikipedia autocomplete responses. this currently fails.
    Caching:
    *   Allow caching to return path from cache if it is a subpath of a cached path.
    bidirectional_search():
    *   General refactoring.

    * sort out query cache thing so its more optional that is dumping massive dicts
      in a json file.

    Have propper look for bugs and actually do some testing. (/work out how to.)
"""
from collections import deque
import random
import requests
import sys
import argparse

from jsoncache import jsoncache
from jsoncache import load_query_cache
from jsoncache import save_query_cache
from jsoncache import getSize
from jsoncache import printf

API_URL = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "HOMUNCULUS"


def main():
    # Set up argparse with start as a positional arg and end as optional.
    args = parse_args()
    # Get start, end values and if to save_cache.
    start = args.start
    end   = "Homunculus" if not args.end else args.end
    save_cache = args.cache if args.cache is not None else True
    printf("Searching:  '%s' -> '%s'", start, end)
    # Check if the term has been search for before.
    data = path_to_homunculus(start, end, save_cache=save_cache)
    if data:
        (paths, time_score, request_count) = data
        # Print the results to the stdout.
        printf("Paths:")
        for path in paths:
            printf("\tSeparation:  %d steps", len(path)-1)
            printf("\tPath:        %s", " -> ".join(path))
            printf("...")
        printf("-"*80)
        printf("Time Taken:  %f seconds", time_score)
        printf("requests:    %d", request_count)
        save_query_cache(query_cache)
        print("query cache size: " + getSize("querycache.json"))
    else:
        printf("Failed Search.")


@jsoncache
def path_to_homunculus(start, end="Homunculus", save_cache=True):
    """Return the first found degrees of seperation between
    2 wikipedia pages."""
    path_to_homunculus.requests = 0
    paths = bidirectional_search(start, end, wiki_links)
    return paths, path_to_homunculus.requests



def bidirectional_search(start, end, successors):
    """bidirectional_search(start, end, successors): Do a Breath-First-Search
    from both start and end nodes at the same time. Keep track of each sides
    explored nodes and when they overlap merge the found path."""
    # This outperformed Breath-First-Search massively, mainly due to its ability
    # to widen the local search space and decrease http requests. future:
    # maybe properly cache "Homunculus" to a depth of 2 giving around 200,000
    # iniital state space.
    if start == end:
        return [[start]]
    l_explored, l_front = set(), deque([[start]])
    r_explored, r_front = set(), deque([[end]])
    found_paths = []
    while l_front and r_front:
        # -> Advance forwards from start. ----------------------------
        path = l_front.popleft()
        for state in successors(path[-1], is_forward=True):
            if state not in l_explored:
                l_explored.add(state)
                path2 = path + [state]
                if state == end:
                    found_paths.append(path2)
                else:
                    l_front.append(path2)
        # -----------------------------------------------------------
        # TODO: Maybe find a effective way to get rid of the code duplication.
        # <- Advance backwards from end. ----------------------------
        path = r_front.popleft()
        for state in successors(path[-1],  is_forward=False):
            if state not in r_explored:
                r_explored.add(state)
                path2 = path + [state]
                if state == start:
                    found_paths.append(path2)
                else:
                    r_front.append(path2)
        if found_paths:
            return min(found_paths, key=len)
        path_overlap = l_explored & r_explored
        if path_overlap:
            print(path_overlap)
            return old_merge_paths(l_front, path_overlap, r_front)
        # -----------------------------------------------------------
    return []



def seeded_bidirectional_search(start, successors):
    """seeded_bidirectional_search(): do a bidirectional search but with one
    side of the graph pre loaded from a cache."""
    # check if start is the end because you never know.
    end = "Homunculus"
    if start == end:
        return [[start]]
    # load saved graph from the 'Homunculus' end node and check to
    # see if it is already in range.
    r_explored, r_front = load_cached_graph()
    if start in r_explored:
        return old_merge_paths([[start]], [start], r_front)
    # init left side.
    l_explored, l_front = set(), deque([[start]])
    while l_front and r_front:
        path = l_front.popleft()
        for state in successors(path[-1], is_forward=True):
            if state not in l_explored:
                l_explored.add(state)
                path2 = path + [state]
                if state == end:
                    return [path2]
                else:
                    l_front.append(path2)
        # <> Check for overlaps in explored. if so, we are done.
        path_overlap = l_explored & r_explored
        if path_overlap:
            return old_merge_paths(l_front, path_overlap, r_front)
    return []


def load_cached_graph():
    title = "Homunculus"
    is_forward = False
    results = connect_links(title, is_forward)
    explored = set([title])
    frontier = deque([title])
    for result in results["links"]:
        frontier.append([title, result])
        res = connect_links(result, is_forward)
        explored.add(result)
        if res:
            for r in res["links"]:
                frontier.append([title, result, r])
                explored.add(r)
    return explored, frontier


def connect_links(title, is_forward):
    "same as wiki request links but only use cached."
    global query_cache
    if title in query_cache and query_cache[title]["fwd"] == is_forward:
        return query_cache[title]
    else:
        return {}


def merge_paths(path, overlap, frontier, is_forward):
    if is_forward:
        for right in frontier:
            if overlap in right:
                return [path + list(reversed(right))]
    else:
        for left in frontier:
            if overlap in left:
                return [left + list(reversed(path))]
    return []

def old_merge_paths(l_front, overlaps, r_front):
    paths = []
    best = 1000
    # when only getting the first reverse queues.
    for overlap in overlaps:
        for left in l_front:
            if overlap in left:
                for right in r_front:
                    if overlap in right:
                        path = left[:left.index(overlap)] + list(reversed(right))
                        if path not in paths and len(path) < best:
                            best = len(path)
                            paths.append(path)
    return paths

def wiki_links(title, is_forward):
    results = wiki_request_links(title, is_forward)
    # Fails with wikipedias autocorrect at the moment and
    # also dosent get all the values just the first 500.
    links = results["links"]
    random.shuffle(links)
    for result in links:
        yield result


def wiki_request_links(title, is_forward):
    """Make a request to the Wikipedia API using the given search parameters.
    Returns a parsed dict of the JSON response."""
    global query_cache
    if title in query_cache and query_cache[title]["fwd"] == is_forward:
        return query_cache[title]
    params = (left_params if is_forward else right_params)
    params["titles"] = title
    result = {}
    for res in wiki_query(params):
        result.update(res)

    query_cache[title] = {}
    node = list(result['pages'].values())[0]
    if 'linkshere' in node:
        node_links = node["linkshere"]
        query_cache[title]["links"] = [n["title"] for n in node_links]
    elif 'links' in node:
        node_links = node["links"]
        query_cache[title]["links"] = [n["title"] for n in node_links]
    else:
        query_cache[title]["links"] = []

    query_cache[title]["fwd"] = is_forward
    return query_cache[title]


def wiki_query(request):
    lastContinue = {}
    while True:
        # Clone original request
        req = request.copy()
        # Modify it with the values returned in the 'continue' section of the last result.
        req.update(lastContinue)
        # Call API
        result = requests.get(API_URL, params=req, headers=headers).json()
        if 'error' in result:
            raise Error(result['error'])
        if 'warnings' in result:
            print(result['warnings'])
        if 'query' in result:
            if len(result['query']) != 0:
                yield result['query']
        if 'continue' not in result:
            break
        lastContinue = result['continue']
        print("request: " +  req["titles"])


# https://www.mediawiki.org/wiki/API:Query
default = {"format": "json", "action": "query"}

left_params = {
    "prop": "links",
    "plnamespace": 0,
    "pllimit": "max"
}
left_params.update(default)

right_params = {
    "prop": "linkshere",
    "lhnamespace": 0,
    "lhlimit": "max",
    "lhprop": "title"
}
right_params.update(default)

headers = {
    'User-Agent': USER_AGENT
}


query_cache = load_query_cache()

def parse_args():
    # Set up argparse with start as a positional arg and end as optional.
    parser = argparse.ArgumentParser()
    s_help = "Title of valid wiki page to start from. E.g.'Santa Claus'"
    e_help = "Title of valid wiki page to end on default is 'Homunclus'"
    c_help = "Set to false to disable caching results."
    parser.add_argument("start", help=s_help, type=str)
    parser.add_argument("-e", "--end", help=e_help, type=str)
    parser.add_argument("-c", "--cache", help=c_help, type=bool)
    return parser.parse_args()


if __name__ == '__main__':
    main()

