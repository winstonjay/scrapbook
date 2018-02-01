#include "global.h"

extern Scanner scanner;

void error(char *msg) {
    fprintf(stderr, "line %d: %s\n", scanner.lineo, msg);
    exit(1); // exit failure...
}