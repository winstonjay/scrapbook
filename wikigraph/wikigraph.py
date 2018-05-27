#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
wikigraph.py:
Implements classes for finding paths between wikipedia articles
and other related functions using the WikiMedia API.

The `WikiGraph.find_path` method is better run in a shell
session or in a batch collection as its use of memoization will
speed up searches whilst it runs, reducing requests to the Wikimedia API.

Example session:

>>> import wikigraph
>>> w = wikigraph.WikiGraph()
>>> path = w.find_path(start="Tom Hanks", end="Kevin Bacon")
>>> print(path)
<wikigraph.Path: Tom Hanks -> Kevin Bacon>
>>> print(path.info)
Path:
        Path:        Tom Hanks -> Kevin Bacon
        Separation:  1 steps
        Time Taken:  0.578131 seconds
        Requests:    2

>>> path.data
{'start': 'Tom Hanks', 'end': 'Kevin Bacon', 'path': 'Tom Hanks->Kevin Bacon', 'degree': 1}
>>> print(path.json(indent=2))
{
  "start": "Tom Hanks",
  "end": "Kevin Bacon",
  "path": "Tom Hanks->Kevin Bacon",
  "degree": 1
}

TODO:
    Think about memoization. Some cases make this impractical, for example
    the top50 most visited articles have a gigantic amount of links that
    direct to them (top50 mean=47300). Perhaps change the memoizing to be
    optional and editable within the WikiGraph object instances instead of
    just as a function decorator. This would make all functions that need
    to make requests to the api more flexable in terms of their memory usage.

TODO:
    Investigate strategies for cases where inbound links really big for
    similar reasons as above. For example 'United States' has around 463000
    links to it, is it a reasonable to loop through of these before checking
    the other end of the search.

TODO:
    Handle edge cases for when start or end articles have no links pointing
    to and from them. Policy now is just to run until the users patience runs
    out. Of the 500 random sample collected this did not happen or if it did
    wikipedia rediriected us to another page.
'''
from __future__ import print_function

import json
from collections import deque
from datetime import datetime

from wikiapi import WikiAPI


class WikiGraph(WikiAPI):
    '''
    WikiGraph implements methods for connecting to the WikiMedia API
    orientated to finding paths between articles and information between
    nodes. Public methods are: `find_path`, `indegree`. When using with
    find_path it is better use in a session or in a batch collection as
    memoization means it will speed up searches and reduce requests to
    the Wikimedia API.
    '''

    def find_path(self, start, end):
        '''Find a valid path between 2 given wikipedia articles
        and return a Path object.'''
        self.requests_fwd = 0
        self.requests_bwk = 0
        t1 = datetime.now()
        return Path(start=start, end=end,
                    path=self._bidirectional_search(start, end, self.page_links),
                    time=(datetime.now() - t1).total_seconds(),
                    requests=self.requests_fwd + self.requests_bwk)

    def indegree(self, title):
        '''return the number of links to a given article. This corresponds
        to using the "linkshere" property of the WikiMedia api.'''
        params = self.right_params
        params["titles"] = title
        # iterate through requests and get a cumsum.
        total = 0
        for result in self._query(params):
            node = next(iter(result['pages'].values()))
            if not "linkshere" in node:
                print("Title Error: Page missing results? '%s'" % title)
                raise StopIteration
            total += len(node["linkshere"])
        return total

    def _bidirectional_search(self, start, end, successors):
        '''
        Use a unweighted bidirectional search to form paths from start to
        end args. This works as Breath-First-Search from both start and end nodes
        at the same time balancing traversals by requests made to the api from each
        side. It Keeps track of each sides explored nodes returning the shortest
        merged path when a overlap occurs.
        '''
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
                        found_paths.append(path2[::-1])
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


class Path(object):
    '''
    Path is returned by the WikiGraph.find_path method. It stores
    the state of the path whilst implementing methods for displaying
    and returning its data.
    '''
    def __init__(self, start, end, path=[], time=None, requests=None):
        self.start = start
        self.end = end
        self.path = path
        self.degree = len(self.path) - 1
        self.time = time
        self.requests = requests

    def __nonzero__(self):
        "is the path empty"
        return bool(self.path)

    def __str__(self):
        "More infomative string representation"
        return "<%s.%s: %s>" % (self.__class__.__module__,
                                self.__class__.__name__,
                                " -> ".join(self.path))

    @property
    def info(self):
        "return infomaiton about a given path"
        path = " -> ".join(self.path)
        name = self.__class__.__name__
        return ("%s:\n"
                "\tPath:        %s\n"
                "\tSeparation:  %d steps\n"
                "\tTime Taken:  %f seconds\n"
                "\tRequests:    %d\n"
                % (name, path, self.degree, self.time, self.requests))

    @property
    def data(self):
        "return path output as a dict."
        return dict(start=self.start,
                    end=self.end,
                    path="->".join(self.path),
                    degree=self.degree)

    def json(self, **kwargs):
        "return result data as json"
        return json.dumps(self.data, **kwargs)
