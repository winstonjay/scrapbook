from __future__ import print_function

from collections import deque
from datetime import datetime

import random
import requests

from memo import memoize


class WikiPathFinder(object):
    '''WikiPathFinder...'''
    def __init__(self, print_requests=False):
        self.print_requests = print_requests
        self.start, self.end = None, None
        self.path = []

    def find_path(self, start, end):
        "Find a valid path between 2 wikipedia articles."
        self.start, self.end = start, end
        self.requests = 0
        self.requests_fwd, self.requests_bwk = 0, 0
        t1 = datetime.now()
        self.path = self._bidirectional_search(start, end, self.wiki_links)
        self.time = (datetime.now() - t1).total_seconds()
        return self.path

    def data(self):
        return dict(start=self.start,
                    end=self.end,
                    path="->".join(self.path),
                    degree=len(self.path)-1)

    def print_stats(self):
        # Print the results to the stdout.
        print("Found Path:")
        print("\tSeparation:  %d steps" % (len(self.path)-1))
        print("\tPath:        %s" % " -> ".join(self.path))
        print("\tTime Taken:  %f seconds" % self.time)
        print("\tRequests:    %d" % self.requests)
        print("-"*80)

    def _bidirectional_search(self, start, end, successors):
        """bidirectional_search(start, end, successors): Do a Breath-First-Search
        from both start and end nodes at the same time. Keep track of each sides
        explored nodes and when they overlap merge the found path."""
        if start == end:
            return [start]
        l_explored, l_front = set(), deque([[start]])
        r_explored, r_front = set(), deque([[end]])
        while l_front and r_front:
            # -> Advance forwards from start.
            if self.requests_fwd < self.requests_bwk and l_front:
                path = l_front.popleft()
                for state in successors(path[-1], True):
                    if state not in l_explored:
                        l_explored.add(state)
                        path2 = path + [state]
                        if state == end:
                            return path2
                        elif state in r_explored:
                            return self._merge_paths(path2, r_front)
                        else:
                            l_front.append(path2)
            else:
                # <- Advance backwards from end.
                path = r_front.popleft()
                for state in successors(path[-1], False):
                    if state not in r_explored:
                        r_explored.add(state)
                        path2 = path + [state]
                        if state == start:
                            return path2
                        elif state in l_explored:
                            # reverse the result so its the right way round.
                            return self._merge_paths(path2, l_front)[::-1]
                        else:
                            r_front.append(path2)
        return []

    def _merge_paths(self, path, frontier):
        overlap = path.pop()
        return min([path + opposite[::-1]
                    for opposite in frontier
                    if overlap in opposite], key=len)
    @memoize
    def wiki_links(self, title, is_forward):
        """Make a request to the Wikipedia API using the given search
        parameters. Returns a parsed dict of the JSON response."""
        params = (left_params if is_forward else right_params)
        params["titles"] = title
        # iteraterate through the results of our query.
        for result in self._query(params):
            node = next(iter(result['pages'].values()))
            # if there isnt any links like can happen exit the gen loop.
            if not params["prop"] in node:
                print("Title Error: Page missing results?", "'"+title+"'")
                raise StopIteration
            links = [n["title"] for n in node[params["prop"]]]
            # shuffle to stop the results being completely aphabetical.
            random.shuffle(links)
            # emit the links gathered.
            for link in links: yield link

    def _query(self, request):
        # Code from advice on wikimedia api.
        lastContinue = {}
        while True:
            # Clone original request
            req = request.copy()
            self.requests += 1
            if request["prop"] == 'links':
                self.requests_fwd += 1
            else:
                self.requests_bwk += 1

            if self.print_requests:
                print("request: " +  req["titles"])
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


def wiki_random_sample(pages=1):
    # https://www.mediawiki.org/wiki/API:Random
    params = {'list': 'random', 'rnnamespace': 0, 'rnlimit': pages}
    params.update(default)
    request = requests.get(API_URL, params=params, headers=headers).json()
    return [page['title'] for page in request['query']['random']]


API_URL = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "HOMUNCULUS"
headers = {'User-Agent': USER_AGENT}

# https://www.mediawiki.org/wiki/API:Query
default = {"format": "json", "action": "query"}
# for searching forwards.
left_params = {"prop": "links", "plnamespace": 0, "pllimit": "max"}
left_params.update(default)
# for searching backwards.
right_params = {"prop": "linkshere", "lhnamespace": 0,
                "lhlimit": "max", "lhprop": "title"}
right_params.update(default)

