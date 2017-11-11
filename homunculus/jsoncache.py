import json
import os
from datetime import datetime
from functools import update_wrapper

# FileNotFoundError is not defined in python 2.7
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d


@decorator
def jsoncache(f):
    "Cache results of already run paths to reduce requests to wikipedia."
    def _f(*args, **kwargs):
        save_cache = kwargs["save_cache"]
        title = "->".join(args)
        try:
            with open("history.json") as hist:
                data = json.load(hist)
            cached = data[title]
            result = (cached["paths"], cached["time"], cached["requests"])
            print("Results Loaded from cache in 'history.json'.")
            return result
        except (FileNotFoundError, KeyError):
            t1 = datetime.now()
            paths, req = f(*args, **kwargs)
            time_score = (datetime.now() - t1).total_seconds()
            if not paths:
                return []
            result = (paths, time_score, req)
            if save_cache:
                save_json_cache(title, result, *args)
            return result
    return _f


def save_json_cache(title, data, start, end, filename='history.json'):
    "Save latest search in file, is file does not exist make a new one."
    (paths, time_score, request_count) = data
    try:
        with open(filename) as hist:
            data = json.load(hist)
    except FileNotFoundError:
        data = {}
    data[title] = {
        "start": start, "end": end,
        "paths": paths, "time": time_score,
        "requests": request_count}
    # Save either new dict or an updated old one.
    with open(filename,  mode='w') as hist:
        json.dump(data, hist, sort_keys=True, indent=4)
    printf("Saved to cache: '%s'", title)
    return True

# I been enjoying printf to much lol...
def printf(string, *args):
    print(string % args)


def load_query_cache():
    try:
        with open("querycache.json") as qc:
            return json.load(qc)
    except:
        return {}

def save_query_cache(data):
    with open("querycache.json",  mode='w') as qc:
        json.dump(data, qc)

def getSize(filename):
    st = os.stat(filename)
    sizeMB = st.st_size / 2.0**20
    return "%f MB" % sizeMB




