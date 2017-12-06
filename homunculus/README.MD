# Degrees of Seperation Between Wikipedia Articles; How many click's away from the Homunculus?

This folder contains python files for finding paths between wikipedia articles online using the [wikimedia API](https://www.mediawiki.org/wiki/API:Main_page). A path is created by linking articles by the links they contain, just like the [wikipedia game](https://en.wikipedia.org/wiki/Wikipedia:Wiki_Game). It dosent necessarily find the
shortest path between the two as it uses a bi-directional search instead of breadth-first. This was a trade-off to reduce time taken to collect paths. **Here is an example output**:

    Searching:  'GitHub' -> 'Homunculus'
    Found Path:
            Separation:  4 steps
            Path:        GitHub -> United States -> Pragmatism -> Alchemy -> Homunculus
            Time Taken:  5.207734 seconds
            Requests:    19
    --------------------------------------------------------------------------------

### Usage:

**Requirements:** `requests` is needed to do the internets stuff.

    $ pip install requests

**findwikipath.py** will find a path between two wikipedia articles. See command line arg details below.

    usage: findwikipath.py [-h] [-e END] start

    positional arguments:
    start              Title of valid wiki page to start from. E.g.'Santa Claus'

    optional arguments:
    -h, --help         show this help message and exit
    -e END, --end END  Title of valid wiki page to end on default is 'Homunclus'

**collectwikibatch.py** will collect a random sample of paths to a given article page. It gets faster as it goes because it memoizes the links of the pages that it has already visited reducing api calls. Because of this, it might not be recomended to collect too large a sample. For more info See command line arg details below. [default sampler](https://www.mediawiki.org/wiki/API:Random)

    usage: collectwikibatch.py [-h] [-x CENTER] [-s SET] [-n NUMBER] outfile

    positional arguments:
    outfile               file to save the results.

    optional arguments:
    -h, --help            show this help message and exit
    -x CENTER, --center CENTER
                            Title of valid wiki page to center all nodes from.
                            E.g.'Santa Claus', default is Homunculus
    -s SET, --set SET     Sample Set to collect, default is a random sample from
                            wikimedia api. Alternatively specify a filename containing
                            a valid article title per line.
    -n NUMBER, --number NUMBER
                            Sample size to collect. default is set to 50.

