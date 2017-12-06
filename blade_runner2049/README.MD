# Blade Runner 2049 Movie Review Generator.

### files:

**webscraper.py:**
Collects Rotten Tomato audience reviews from pages 1 - 52 and saves results in path 'data/rawout.txt'.

**ngrams.py:** Save to disk ngrms of a given length to a text file from the collecte reviews. Usage:

	ngrams.py <input file (str)> <N-gram count (int)> <save to disk (T/F)>
eg:

	ngrams.py 'data/rawout.txt' 3 T

**markov.py:** Provides class for generating movie reviews from generated n-grams.

**For requirements:** see 'requirements.txt'

### Example Outputs:

Using trigrams the following was generated.

* brilliant and absolutely phenomenal!!!
* there are people out there who deeply appreciate story like this, and audibly.
* put to sleep. overhyped.
* dull dull, far too long, this movie was loud, slow and i couldn't follow plot
* very boring! effects were gorgeous -- such pretty film. yes the visuals are stunning the acting is great.
* espectacular, solo fans sci-fy calidad, excelente trabajo director villeneuve productor maestro ridley scott
* keeps the feel style and universe of blade runner 2049. blade runner was in themovie with them.
* visually stunning. if you have not seen this movie. not only long as heck but absolutely terrible.
* too self-indulgent, long take after long wait this film!
* while the theatrical release suffered from being edited too short, making it choppy and confusing, 2049 will carry less impact and leave you little confused.
* amazingly different but congruent with the movie which never came. what?
* very boring! effects were gorgeous -- such pretty film. it felt like anything that was well used.


### TODO / Future

Create a probalistic model to classify and predict review scores from what they say. Impersonate reviews on the site but try to keep neutral impact and blend in.