# Hello, World
## Running Each file type Mac OSX
(Obviously you have to have them all installed.)


C (src/hello.c):

	$ gcc -o bin/hello_c hello.c
	$ ./bin/hello_c

C++ (src/hello.cc):

	$ g++ -o bin/hello_cc hello.cc
	$ ./bin/hello_cc

C# (src/hello.cs):

	$ ...?

Elixir http://elixir-lang.github.io/ (src/hello.exs):

	$ elixir hello.exs

Go https://golang.org/ (src/hello.go):

	$ go run hello.go

Haskell (src/hello.hs):

	$ ghc -o bin/hello_hs hello.hs
	$ ./bin/hello_hs

Java (src/hello.java):

	$ javac hello.java
	$ java hello

Julia https://julialang.org/ (src/hello.jl):

	$ julia hello.jl

JavaScript (src/hello.js):

	$ node hello.js

Objective-C (src/hello.m):

	$ gcc -framework Foundation hello.m -o bin/hello_objc

PHP http://www.php.net/ (src/hello.php):

	$ php hello.php

Perl https://www.perl.org/ (src/hello.pl):

	$ perl hello.pl

Python https://www.python.org/ (src/hello.py):

	$ python hello.py

Ruby https://www.ruby-lang.org/ (src/hello.rb):

	$ ruby hello.rb

Rust https://www.rust-lang.org/ (src/hello.rs):

	$ rustc hello.rs --crate-name bin/hello_rs
	$ ./hello_rs

Bash (src/hello.sh):

	$ bash hello.sh

Swift https://developer.apple.com/swift/ (src/hello.swift):

	$ swift hello.swift

Assembly Raspberry Pi ARM (src/hello_arm.s):

	$ as -o tmp/hello_arm.o hello_arm.s
	$ ld -o bin/hello_arm tmp/hello_arm.o
	$ ./bin/hello_arm

Assembly Mac osx (src/hello_macho64.s):

	$ nasm -f macho64 -o hello_macho64.s hello_macho64.s
	$ ld -o hello_macho64 hello_macho64.o
	$ hello_macho64.s
	en:   equ     $ - msg

