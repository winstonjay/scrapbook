# complie all c files in the directory into one executable.
filename = simple
targets  = emitter.c error.c main.c parser.c scanner.c symbol.c
cflags   = -Wall -Werror -Wextra

all:
	gcc $(CFLAGS) -o $(filename) $(targets)

debug:
	gcc $(CFLAGS) -g -o $(filename) $(targets)

clean:
	rm -r simple.dSYM