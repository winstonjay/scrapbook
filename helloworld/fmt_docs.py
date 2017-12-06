#!/usr/bin/python
import os

def main():
    "Loop through directory and print out documentation for each file type."
    print(pagehead)
    for filename in os.listdir('src'):
        if filename.startswith('hello'):
            extract_docs('src/%s' % filename)

def extract_docs(filename):
    with open(filename, 'r') as fn:
        for line in fn.readlines():
            if 'Hello World' in line:
                lang = line[line.find("(")+1:line.find(")")].strip()
                print("%s (%s):\n" % (lang, filename))
            if '$' in line:
                run_cmd = line[2:].strip()
                print("\t%s\n" % run_cmd)
        print("")

pagehead = """# Hello, World
## Running Each file type Mac OSX
(Obviously you have to have them all installed.)

"""

if __name__ == '__main__':
    main()