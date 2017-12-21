from functools import update_wrapper

def decorator(d):
    "Make function d a decorator: d wraps a function fn."
    def _d(fn):
        return update_wrapper(d(fn), fn)
    update_wrapper(_d, d)
    return _d

@decorator
def memoize(f):
    "Cache results of already run paths to reduce requests to wikipedia."
    cache = {}
    def _f(*args):
        try:
            res = cache[args[1:]]
            # print("cache:", args[1:])
            return res
        except KeyError:
            cache[args[1:]] = result = list(f(*args))
            return result
        raise ValueError
    return _f