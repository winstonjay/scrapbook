"""
File is used for collecting graph from homunculus to a depth of 3.
The query_cache.json file has not completely been filled. To continue
collection just run again and it should zoom past all the nodes that have
already been collected.
"""
from jsoncache import *
from wikisearch import query_cache
from wikisearch import wiki_request_links
from wikisearch import wiki_query

def collectGraph(title="Homunculus", is_forward=False):
    global query_cache
    results = wiki_request_links(title, is_forward)
    for result in results["links"]:
        print(title, "<-", result)
        res = wiki_request_links(result, is_forward)
        for r in res["links"]:
            rp = wiki_request_links(r, is_forward)
            print(result, "<-", r)
            print(len(rp["links"]))
            print("."*40)
        save_query_cache(query_cache)
        print("query cache size: " + getSize("querycache.json"))
        print("."*80)
    print("Finished...")



if __name__ == '__main__':
    collectGraph()