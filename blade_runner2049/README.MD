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

### Example Output:

Using trigrams the following was generated.

	* brilliant and absolutely phenomenal!!!
	* put to sleep. overhyped.
	* espectacular, solo fans sci-fy calidad, excelente trabajo director villeneuve productor maestro ridley scott, could have recaptured the feeling of this movie makes big mistake in putting form over substance.
	* dull dull, far too long, this movie was loud, slow and i couldn't follow plot
	* probably one of the movie, why are they continued to be off-putting to some nice surprises along the way the story moves along so slowly over the course of it's 2 hour and 45 minute running time that i began to doze off in the movie.
	* very boring! effects were gorgeous -- such pretty film. yes the visuals are stunning the acting is great.
	* espectacular, solo fans sci-fy calidad, excelente trabajo director villeneuve productor maestro ridley scott
	* keeps the feel style and universe of blade runner 2049. blade runner was in themovie with them.
	* visually stunning. if you have not seen this movie. not only long as heck but absolutely terrible.
	* spectacular film! totally original with none of the day, bladerunner 2049 is that how denis villeneuve delivers again with this one was philosophical masterpiece but it is profound and lot of ambiguity left for the opportunity to do so.
	* too self-indulgent, long take after long wait this film!
	* igor 3 hour long watch. how this particular characters effected the main characters to advance anything.
	* pretty good with tie-ins to the original blade runner 2049, it more than worth the price of admission is it's jaw dropping visuals, amazing score!
	* while the theatrical release suffered from being edited too short, making it choppy and confusing, 2049 will carry less impact and leave you little confused.
	* i think even the original.
	* great movie, it? s not for the first film, but also one that is painter as well.
	* there are people out there who deeply appreciate story like this, and audibly.
	* amazingly different but congruent with the movie which never came. what?
	* very boring! effects were gorgeous -- such pretty film. it felt like anything that was well used.
	* one of the original.


### TODO / Future

Create a probalistic model to classify and predict review scores from what they say.