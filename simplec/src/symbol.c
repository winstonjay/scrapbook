#include "global.h"

#define STRMAX 0x400     // size of lexemes array
#define SYMMAX 0x80      // size of symboltable

char lexemes[STRMAX];
Entry symboltable[SYMMAX];

int lastchar = -1,
    lastentry = 0;

int lookup(char string[]) {
    int p;
    for (p = lastentry; p > 0; p--) {
        if (strcmp(symboltable[p].lexptr, string) == 0) {
            return p;
        }
    }
    return 0;
}

int insert(char string[], int token) {
    int len = strlen(string);
    if (lastentry + 1 >= SYMMAX) {
        error("symbol table full");
    }
    if (lastchar+len+1 >= STRMAX) {
        error("lexemes array full");
    }
    lastentry += 1;
    symboltable[lastentry].token = token;
    symboltable[lastentry].lexptr = &lexemes[lastchar+1];
    lastchar += len+1;
    strcpy(symboltable[lastentry].lexptr, string);
    return lastentry;
}