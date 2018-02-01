#include "global.h"

int peek, id_ptr;
Scanner scanner;

void parse() {
    Scanner_init(&scanner);
    peek = Scanner_scan(&scanner);
    while (peek != DONE) {
        switch (peek) {
        case ID:
            id_ptr = scanner.literal;
            match(ID); expr(); emit(ID, id_ptr);
            match(';'); emit(';', NONE);
            continue;
        default:
            expr(); match(';'); emit(';', NONE);
        }
    }
}

void expr() {
    int token;
    term();
    while (true) {
        switch (peek) {
        case '+': case '-':
            token = peek;
            match(peek); term(); emit(token, NONE);
            continue;
        default:
            return;
        }
    }
}

void term() {
    int token;
    factor();
    while (true) {
        switch (peek) {
        case '*': case '/': case DIV: case MOD:
            token = peek;
            match(peek); factor(); emit(token, NONE);
            continue;
        default:
            return;
        }
    }
}

void factor() {
    switch (peek) {
    case '(':
        match('('); expr(); match(')'); break;
    case NUM:
        emit(NUM, scanner.literal); match(NUM); break;
    case ID:
        emit(ID, scanner.literal); match(ID); break;
    default:
        printf("what is '%c'?\n", peek);
        error("Illegal syntax error");
    }
}

void match(int token) {
    if (peek == token) {
        peek = Scanner_scan(&scanner);
    } else {
        fprintf(stderr, "Error: got=%d want=%d\n", token, peek);
        error("Match syntax error");
    }
}