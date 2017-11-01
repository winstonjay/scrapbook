import json
import pprint
from collections import Counter, defaultdict


def loadJson(filename):
    with open(filename) as f:
        return json.load(f)


def printdata(data):
    "print out data niceish"
    pp.pprint(data)

pp = pprint.PrettyPrinter(depth=6)


def json_to_csv(fmt_data, filename):
    data = loadJson(filename)
    head, formated = fmt_data(data)
    # just print to file like: python prog.py > file.csv
    print(head)
    for fmt in formated("genius"):
        print(fmt)


def fmt_csv(data):
    times = data.get("times")
    def fmt_fn(name):
        counts = data.get(name)
        current = times[0][:-14]
        bi, lot = 0, []
        for i, ts in enumerate(times):
            ts = ts[:-14] # remove the timestamps so we just have date.
            if ts != current:
                yield current + "," + make_count(lot)
                current, lot = ts, []
                bi += 1
            lot += counts[i]
        yield current + "," + make_count(lot)
    notes = ",".join(["%d,n%d" % (n, n) for n in range(1, 6)])
    return "date,%s,total" % notes, fmt_fn

def make_count(lst):
    counts = Counter()
    for name, count in lst:
        counts[name] += count
    n = sum(counts.values())
    counts = list(counts.most_common(5))
    return "%s,%s" % (",".join(["%s,%d" % (n, c) for n, c in counts]), n)


if __name__ == '__main__':
    # prints to terminal, print to file if you want.
    json_to_csv(fmt_csv, "data/data-2-8-17.json")