#include "global.h"

void Scanner_init(Scanner *s) {
    s->lineo = 1;
    s->literal = NONE;
}

int Scanner_scan(Scanner *s) {
    int t;
    while(true) {
        t = getc(fp);
        if (t == ' ' || t == '\t') {
            continue;
        }
        if (t == '\n') {
            s->lineo++; continue;
        }
        if (isdigit(t)) {
            ungetc(t, fp);
            fscanf(fp, "%d", &s->literal);
            return NUM;
        }
        if (isalpha(t)) {
            int p, b = 0;
            while (isalnum(t)) {
                s->buffer[b] = t;
                t = getc(fp);
                b += 1;
                if (b >= BSIZE) {
                    error("Compiler Error");
                }
            }
            s->buffer[b] = EOS;
            if (t != EOF) {
                ungetc(t, fp);
            }
            p = lookup(s->buffer);
            if (p == 0) {
                p = insert(s->buffer, ID);
            }
            s->literal = p;
            return symboltable[p].token;
        }
        if (t == EOF) {
            return DONE;
        }
        s->literal = NONE;
        return t;
    }
}