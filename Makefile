UNAME := $(shell uname)

prefix=${HOME}
exec_prefix=${prefix}
libdir=${exec_prefix}/lib
includedir=${prefix}/include

# the build target executable:
TARGET = counterc

CC = gcc
CFLAGS  = -shared -Wl,-soname,$(TARGET).so -Wl,--no-undefined -I${includedir} -L${libdir} -std=c99 -O3 -funroll-loops

ifeq ($(UNAME), Darwin)
CC = gcc
CFLAGS  = -shared -Wl,-rpath,${libdir},-install_name,$(TARGET).so -I${includedir} -L${libdir} -O3 -funroll-loops
endif

all: $(TARGET)

$(TARGET): $(TARGET).c
	$(CC) $(CFLAGS) -o $(TARGET).so -fPIC $(TARGET).c -lcalg

clean:
	$(RM) $(TARGET)