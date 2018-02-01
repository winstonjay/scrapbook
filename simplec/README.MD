# SimpleC - a simple compiler

A work in progress, bare minimum compiler for educational purposes to learn about compilers and assembly programing.
It follows and extends chapter 2 of the [dragon book](https://en.wikipedia.org/wiki/Compilers:_Principles,_Techniques,_and_Tools)
with alterations made to produce working assembley code tageting the ARM achetecture on the Raspberry Pi.

### Usage

To compile the compiler with `gcc` can just run the makefile or:

    $ gcc -o simple emitter.c error.c main.c parser.c scanner.c symbol.c

This should create the `simple` executable. With this we can compile our
own scripts with.

    $ simple <filename> > <filename.s>

Running ARM file in python simulation can be done with. Simulator is merely
configured to run code the compiler is capable of generating.

    $ python3 vm.py <filename.s>

Compiling from ARM assembly to executable. Any external/library functions need to be
defined and linked at this stage.

    $ as -g -o <filename.o> <filename.s>
    $ ld -o <filename> <filename.o>

### Language specification.

    start   -> list eof
    list    -> stmt ; list | €
    stmt    -> expr | id expr
    expr    -> expr + term | expr - term | term
    term    -> term * factor | factor
    factor  -> ( expr ) | num | id

    num:    any base 10 32 bit integer.
    id:     any alphabetic char optionally followed by any alphanumeric.

### Future plans

Keep structure relatively similar and complexity as low as possible. Add support for strings
library functions (print, read), variable definitions, basic conditionals.