UNAME := $(shell uname)

prefix=${HOME}
exec_prefix=${prefix}
libdir=${exec_prefix}/lib
includedir=${prefix}/include

# the build target executable:
TARGET = counterc
TRIE_CODON = trie_codon

CC = gcc
CFLAGS  = -shared -Wl,-soname,$(TARGET).so -Wl,--no-undefined -std=c99 -O3 -funroll-loops

ifeq ($(UNAME), Darwin)
CC = gcc
CFLAGS  = -shared -Wl,-install_name,$(TARGET).so -O3 -funroll-loops
endif

all: $(TARGET)

$(TARGET): $(TARGET).c
	$(CC) $(CFLAGS) -o $(TARGET).so -fPIC $(TARGET).c $(TRIE_CODON).c

clean:
	$(RM) $(TARGET).so