
import random
import requests

from memo import memoize


#### Info for connecting to the api.
API_URL    = "https://en.wikipedia.org/w/api.php"
USER_AGENT = "HOMUNCULUS"
headers    = {'User-Agent': USER_AGENT}

# https://www.mediawiki.org/wiki/API:Query
default = {
    "format": "json",
    "action": "query"
}

# for searching forwards.
left_params = {
    "prop": "links",
    "plnamespace": 0,
    "pllimit": "max"
}
left_params.update(default)

# for searching backwards.
right_params = {
    "prop": "linkshere",
    "lhnamespace": 0,
    "lhlimit": "max",
    "lhprop": "title"
}
right_params.update(default)


class WikiAPI(object):
    '''
    WikiAPI provides the underlying functionality for retreiving pages links
    from the Wikipedias mediawiki.org api service.
    '''
    def __init__(self, print_requests=False):
        self.print_requests = print_requests
        self.requests_fwd = 0
        self.requests_bwk = 0
        self.left_params  = left_params
        self.right_params = right_params

    def links(self, title, inbound=True):
        '''
        For a given article return a list of links to or from it based
        on if kwarg inbound is set to True or False. These correspond to
        the "linkshere" or "links" properties of the WikiMedia api.
        '''
        return list(self.page_links(title, False))

    def random_sample(self, n=1):
        '''
        return a n sized list of random page titles.
        Reference: https://www.mediawiki.org/wiki/API:Random
        '''
        params = {'list': 'random', 'rnnamespace': 0, 'rnlimit': n}
        params.update(default)
        request = requests.get(API_URL, params=params, headers=headers).json()
        return [page['title'] for page in request['query']['random']]

    @memoize
    def page_links(self, title, is_forward):
        '''
        Make a request to the Wikipedia API using the given search
        parameters. Returns a parsed dict of the JSON response.
        '''
        params = (left_params if is_forward else right_params)
        params["titles"] = title
        # iteraterate through the results of our query.
        for result in self._query(params):
            node = next(iter(result['pages'].values()))
            # if there isnt any links like can happen exit the gen loop.
            if not params["prop"] in node:
                print("Title Error: Page missing results? '%s'" % title)
                # TODO: this could mean page has no links.
                raise StopIteration
            links = [n["title"] for n in node[params["prop"]]]
            # shuffle to stop the results being completely aphabetical.
            random.shuffle(links)
            # emit the links gathered.
            for link in links:
                yield link

    def _query(self, request):
        '''
        Generator function for retrieving links from wikimedia API whilst
        keeping track of request counts. Reference:
        https://www.mediawiki.org/wiki/API:Query
        '''
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
