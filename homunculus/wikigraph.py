#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
wikigraph.py:
Implements classes for finding paths between wikipedia articles
and other related functions.

When using with WikiGraph.find_path method it is better use in a
session or in a batch collection as its use of memoization will
speed up searches and reduce requests to the Wikimedia API.

Example session:
    >>> from wikigraph import WikiGraph
    >>> wg = WikiGraph()
    >>> path = wg.find_path("Kevin Bacon", "Tom Hanks")
    >>> path.print_stats()
    Found Path:
        Path:        Tom Hanks -> Kevin Bacon
        Separation:  1 steps
        Time Taken:  1.498983 seconds
        Requests:    5
    -------------------------------------------------------------
'''
from __future__ import print_function

from collections import deque
from datetime import datetime

import random
import requests

from memo import memoize


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


class WikiGraph(object):
    '''WikiGraph implements methods for connecting to the WikiMedia API
    orientated to finding paths between articles and information between
    nodes. Its public methods are find_path, indegree and random_sample.
    When using with find_path it is better use in a session or in a batch
    collection as memoization means it will speed up searches and reduce
    requests to the Wikimedia API.'''
    def __init__(self, print_requests=False):
        self.print_requests = print_requests
        self.requests_fwd = 0
        self.requests_bwk = 0

    def find_path(self, start, end):
        '''Find a valid path between 2 wikipedia articles
        and return a Path object.'''
        self.requests_fwd = 0
        self.requests_bwk = 0
        t1 = datetime.now()
        return Path(start=start, end=end,
                    path=self._bidirectional_search(start, end, self.wiki_links),
                    time=(datetime.now() - t1).total_seconds(),
                    requests=self.requests_fwd + self.requests_bwk)

    def indegree(self, title):
        "return the number of links to a given article."
        return len(self.wiki_links(title, False))

    def random_sample(self, n=1):
        '''return a n sized list of random page titles.
        Reference: https://www.mediawiki.org/wiki/API:Random'''
        params = {'list': 'random', 'rnnamespace': 0, 'rnlimit': n}
        params.update(default)
        request = requests.get(API_URL, params=params, headers=headers).json()
        return [page['title'] for page in request['query']['random']]

    def _bidirectional_search(self, start, end, successors):
        '''Use a unweighted bidirectional search to from paths from start to
        end args. This works as Breath-First-Search from both start and end nodes
        at the same time balancing traversals by requests made to the api from each
        side. It Keeps track of each sides explored nodes returning the shortest
        merged path when a overlap occurs.'''
        if start == end:
            return [start]
        found_paths = []
        l_explored, l_front = set(), deque([[start]])
        r_explored, r_front = set(), deque([[end]])
        while l_front and r_front:
            # -> Advance forwards from start.
            if self.requests_fwd < self.requests_bwk and l_front:
                path = l_front.popleft()
                for state in successors(path[-1], True):
                    if state in l_explored:
                        # ignore the already explored
                        continue
                    l_explored.add(state)
                    path2 = path + [state]
                    if state == end:
                        found_paths.append(path2)
                    elif state in r_explored:
                        found_paths.append(self._merge_paths(path2, r_front))
                    else:
                        l_front.append(path2)
            elif r_front:
                # <- Advance backwards from end.
                path = r_front.popleft()
                for state in successors(path[-1], False):
                    if state in r_explored:
                        # ignore the already explored.
                        continue
                    r_explored.add(state)
                    path2 = path + [state]
                    if state == start:
                        found_paths.append(path2)
                    elif state in l_explored:
                        # reverse the result so its the right way round.
                        found_paths.append(self._merge_paths(path2, l_front)[::-1])
                    else:
                        r_front.append(path2)
            # we waited till we have done a full loop through the
            # results of these requests so we can find the shortest
            # possible in the data we have recieved.
            if found_paths:
                return min(found_paths, key=len)
        return [] # failed search.

    def _merge_paths(self, path, frontier):
        '''Connect two overlapping paths from a bidirectional search
        and return the shortest one.'''
        overlap = path.pop()
        return min([path + opposite[::-1]
                    for opposite in frontier
                    if overlap in opposite], key=len)

    @memoize
    def wiki_links(self, title, is_forward):
        '''Make a request to the Wikipedia API using the given search
        parameters. Returns a parsed dict of the JSON response.'''
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
            for link in links:
                yield link

    def _query(self, request):
        '''Generator function for retrieving links from wikimedia API whilst
        keeping track of request counts. Reference:
        https://www.mediawiki.org/wiki/API:Query'''
        lastContinue = {}
        while True:
            if request["prop"] == 'links':
                self.requests_fwd += 1
            else:
                self.requests_bwk += 1
            # Clone original request
            req = request.copy()
            if self.print_requests:
                print("request: " + req["titles"])
            # Modify it with the values returned in the 'continue' section
            # of the last result.
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


class Path(object):
    '''Path is returned by the WikiGraph.find_path method. It stores
    the state of the path whilst implementing methods for displaying
    and returning its data.'''
    def __init__(self, start, end, path=[], time=None, requests=None):
        self.start = start
        self.end = end
        self.path = path
        self.degree = len(self.path) - 1
        self.time = time
        self.requests = requests

    def __nonzero__(self): return bool(self.path)

    def data(self):
        "return path output as a dict."
        return dict(start=self.start,
                    end=self.end,
                    path="->".join(self.path),
                    degree=self.degree)

    def print_stats(self):
        "Print the results to the stdout."
        print("Found Path:")
        print("\tPath:        %s" % " -> ".join(self.path))
        print("\tSeparation:  %d steps" % (self.degree))
        print("\tTime Taken:  %f seconds" % self.time)
        print("\tRequests:    %d" % self.requests)
        print("-"*80)