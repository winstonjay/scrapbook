#!/usr/bin/python
import os

def extract_docs(filename):
    with open(filename, 'r') as fn:
        for line in fn.readlines():
            if 'Hello World' in line:
                lang = line[line.find("(")+1:line.find(")")].strip()
                printf("%s (%s)", lang, filename)
            if '$' in line:
                run_cmd = line[2:].strip()
                printf("\t %s", run_cmd)


def printf(string, *args): print(string % args)

def main():
    "Loop through directory and print out documentation for each file type."
    for filename in os.listdir('.'):
        if filename.startswith('hello'):
            extract_docs(filename)


if __name__ == '__main__':
    print("""# Hello, World

## Running Each file type.

""")
    main()