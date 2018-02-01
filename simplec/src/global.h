#ifndef global_h
#define global_h

#include <stdio.h>      // io routines
#include <stdbool.h>    // true & false
#include <ctype.h>      // character test funcs
#include <string.h>     // strlen strcpy...
#include <stdlib.h>     // exit...

#define BSIZE   128     // buffer size.
#define NONE    -1
#define EOS     '\0'

#define NUM     256
#define DIV     257
#define MOD     258
#define ID      259
#define PUTS    260
#define DONE    261

// file to read from in main.
FILE *fp;

// form of scanner.
typedef struct {
    int lineo, literal;
    char buffer[BSIZE];
} Scanner;

// scanner functions;
void Scanner_init(Scanner *s);
int Scanner_scan(Scanner *s);

// parser functions
void parse(), expr(), term(), factor(), match(int t);

// form of symbol table entry.
typedef struct {
    char *lexptr; int token;
} Entry;

#define STRMAX 0x400     // size of lexemes array
#define SYMMAX 0x80      // size of symboltable

char lexemes[STRMAX];
Entry symboltable[SYMMAX];

// symbol table functions.
int lookup(char string[]),
    insert(char string[], int token);

// emitter
void emit(int token, int literal);

// errors
void error(char *msg);

#endif