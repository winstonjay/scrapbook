/*
compile:
    gcc -o simple emitter.c error.c main.c parser.c scanner.c symbol.c
use:
    ./simple <filename>

language specification:

    start   -> list eof
    list    -> stmt ; list | €
    stmt    -> expr | id expr
    expr    -> expr + term | expr - term | term
    term    -> term * factor | factor
    factor  -> ( expr ) | num | id

    num:    any base 10 32 bit integer.
    id:     any alphabetic char optionally followed by any alphanumeric.
*/
#include "global.h"


Entry keywords[] = {
    {"div", DIV},
    {"mod", MOD},
    {0,     0}
};

void init() {
    // load keywords into symbol table.
    for (Entry *p = keywords; p->token; p++) {
        insert(p->lexptr, p->token);
    }
}


int main(int argc, char **argv) {
    if (argc < 2) {
        fprintf(stderr, "No args! Filename required...\n");
        exit(1);
    }
    fp = fopen(argv[1], "r");
    if (fp == NULL) {
        fprintf(stderr, "File Error: Can't open input file\n");
        exit(1);
    }
    printf(".global _start\n_start:\n");
    init();
    parse();
    fclose(fp);
    printf("\tmov r0, #0\n\tmov r7, #1\n\tswi 0\n");
    exit(0);
}