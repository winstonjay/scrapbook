# the compiler: gcc for C program, define as g++ for C++
CC = g++

# compiler flags:
#  	-g    adds debugging information to the executable file
#  	-Wall turns on most, but not all, compiler warnings
CFLAGS  = -std=c++11 -g -Wall -Werror -Wextra

# the build target executable:
TARGET = zebra

all: $(TARGET)

$(TARGET): $(TARGET).cc
	$(CC) $(CFLAGS) -o build/$(TARGET) $(TARGET).cc

clean:
	rm -f $(TARGET)
	rm -r $(TARGET).dSYM