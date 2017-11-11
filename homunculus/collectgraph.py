'''
collectGraph.py:

USE:
    Make bulk seraches from a list of pages to find.
    Either use top 50 list or random sample funciton.
'''
from jsoncache import *
from wikisearch import path_to_homunculus, query_cache
try:
    import wikipedia
except:
    print("Warning: wikipedia module not install random sample function will not work.")


def main():
    # search = wikipedia.random(100)
    search = top50
    collect_graph(search)


# Top 50 wikipedia pages 8/10/2017 (only includes pages that are numbered.)
# https://en.wikipedia.org/wiki/Wikipedia:Multiyear_ranking_of_most_viewed_pages
top50 = [
    "United States",
    "Donald Trump",
    "Barack Obama",
    "India",
    "World War II",
    "Michael Jackson",
    "Sex",
    "United Kingdom",
    "Lady Gaga",
    "Eminem",
    "The Beatles",
    "Adolf Hitler",
    "Justin Bieber",
    "World War I",
    "The Big Bang Theory",
    "Steve Jobs",
    "Canada",
    "Game of Thrones",
    "How I Met Your Mother",
    "Academy Awards",
    "Lil Wayne",
    "Kim Kardashian",
    "Australia",
    "Cristiano Ronaldo",
    "Miley Cyrus",
    "Elizabeth II",
    "List of Presidents of the United States",
    "Harry Potter",
    "Rihanna",
    "Japan",
    "Selena Gomez",
    "Glee (TV series)",
    "Germany",
    "The Walking Dead (TV series)",
    "Abraham Lincoln",
    "Taylor Swift",
    "Star Wars",
    "China",
    "Lionel Messi",
    "Breaking Bad",
    "Johnny Depp",
    "New York City",
    "Tupac Shakur",
    "France",
    "Kanye West",
    "Russia",
    "Stephen Hawking",
    "Albert Einstein",
    "Earth",
    "Mark Zuckerberg"
]

def collect_graph(search):
    global query_cache
    end = "Homunculus"
    for page in search:
        start = page
        printf("Searching:  '%s' -> '%s'", start, end)
        # Check if the term has been search for before.
        data = path_to_homunculus(page, end, save_cache=True)
        if data:
            (paths, time_score, request_count) = data
            # Print the results to the stdout.
            printf("Paths:")
            for path in paths:
                printf("\tSeparation:  %d steps", len(path)-1)
                printf("\tPath:        %s", " -> ".join(path))
                printf("...")
            printf("-"*80)
            printf("Time Taken:  %f seconds", time_score)
            printf("requests:    %d", request_count)
            save_query_cache(query_cache)
            print("query cache size: " + getSize("querycache.json"))
        else:
            printf("Failed Search.")
        print("*"*80)


if __name__ == '__main__':
    main()


