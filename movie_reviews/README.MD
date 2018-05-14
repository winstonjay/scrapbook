A movie review generator
Generate movie reviews with Markov chains from reviews scraped from rotten tomatoes. This is the ideal tool for someone who wants to post interesting movie reviews but has no idea about movies (and also isn’t worried about making any sense).

### Examples

* if you negatively reviewed this movie, and none of them were resolved by the end of the movie, you are crazy.
* story line kinda boring. i did find leto's character not necessary and his monologue felt endless.
* i watched this wonderful movie for the integrity of it.
* put me to sleep. i'm being generous by giving 2 stars because 2 great actors played in it but otherwise real audio and visual communication totally kills it and many other movies done to date.

### Use

**scraper.py**: Scrapes audience reviews for a given film from Rotten tomatoes website. Basic use example:

	$ python scraper.py blade_runner_2049

Movie names must equate to their url within the site, there is no check to see if this is correct, you will just get a 404 error.

**chain.py** : Generate pseudo-random chains of text from tsv file scraped with `scraper.py`.

	$ python chain.py reviews.tsv

**scorer.py**: TODO

Additional info is available for each file with the `-h` flag.

