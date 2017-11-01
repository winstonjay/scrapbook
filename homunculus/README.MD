# How many click's away from the Homunculus?

The following aims to find the degree's for seperation between wikipedia
articles with the default end node set to the article 'Homunculus'. It does this and if successful
prints the path on the screen. Return times vary massively and are very much dependent on the amount
of requests needed. Results by default are saved to a json file.

### My Answer:

**Average path length:** ```3.48`` Links

TODO:
Get all results from each item and check all connections for overlaps.

#### Example Output:
```bash
Searching:  'GitHub' -> 'Homunculus'
Saved to cache:  'GitHub->Homunculus'
Paths:
        Separation:  4 steps
        Path:        GitHub -> Blog -> Family -> Heredity -> Homunculus
...
--------------------------------------------------------------------------------
Time Taken:  5.161356 seconds
requests:    13
```

#### Usage:
```bash
$ python wikisearch.py [-h] [-e END] [-c CACHE] start
```

#### Positional arguments:
```bash
start                 Title of valid wiki page to start from. E.g.'Santa Claus'
```

#### Optional arguments:
```bash
-h, --help               show this help message and exit
-e END, --end END        Title of valid wiki page to end on default is'Homunclus'
-c CACHE, --cache CACHE  Set to False to disable caching results.
```