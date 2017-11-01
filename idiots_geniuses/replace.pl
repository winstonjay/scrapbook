#!/usr/bin/perl

########
# Program tries to solve the problem of null values in our dataset.

use strict;
use warnings;
# Script replaces patterns in files.
# USE: perl replace.pl <filename>


# We want:
# [] -> [["NULL", 0], ["NULL", 0], ["NULL", 0], ["NULL", 0], ["NULL", 0]]

my $newString = "[" . ("[\"NULL\", 0], " x 4) . "[\"NULL\", 0]]";

$^I = '.bak';            # Create a backup copy
while (<>) {             # Loop through file.
   s/\[\]/$newString/g;  # Do the replacement
   print;                # Drint to the modified file
}

# Future ref, maybe just use this one liner,
# perl -p -i -w -e 's/<search>/<replace>/g;' <filename>