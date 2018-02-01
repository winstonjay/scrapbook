#include "global.h"

int reg = 0; // register index to put numbers into.

void emit(int token, int literal) {
    // first check for end of statement.
    if (token == ';') {
        reg = 0; printf("\n"); return;
    }
    printf("\t");
    switch (token) {
    case '+': reg--; printf("add r%d, r%d\n", reg-1, reg); break;
    case '-': reg--; printf("sub r%d, r%d\n", reg-1, reg); break;
    case '*': reg--; printf("mul r%d, r%d\n", reg-1, reg); break;
    // case '/': reg--; printf("div r%d, r%d\n", reg-1, reg); break;
    // case MOD: reg--; printf("mod r%d, r%d\n", reg-1, reg); break;
    case NUM: printf("mov r%d, #%d\n", reg++, literal);    break;
    case ID: printf("bl %s\n", symboltable[literal].lexptr); break;
    default: error("Print Error: Unrecognised operation.");
    }
}