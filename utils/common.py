

def printf(string, *args, **kwargs):
    print(string.format(*args, **kwargs))

concat = ''.join

def transpose(matrix):
    return zip(*matrix)

def first(iterable):
    return next(iter(iterable))

def load_file(filename, fmt_fn=None):
    '''load_file and format with a given function
       eg to open json: load_file('file.txt', json.load)'''
    with open(filename, 'r', encoding='utf-8') as f:
        return (fmt_fn(f) if fmt_fn else f)