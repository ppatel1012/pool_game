CC=clang
CFLAGS=-Wall -pedantic -std=c99
#LDFLAGS = -shared
LIBS=-lm # note: the l means library, m means math
all: phylib.o _phylib.so
phylib.o: phylib.c phylib.h
	$(CC) $(CFLAGS) -fPIC -c phylib.c -o phylib.o
libphylib.so: phylib.o
	$(CC) -shared -o libphylib.so phylib.o -lm
phylib_wrap.c: phylib.i
	swig -python phylib.i
phylib.py: phylib.i
	swig -python phylib.i
phylib_wrap.o: phylib_wrap.c
	$(CC) $(CFLAGS) -c phylib_wrap.c -I/usr/include/python3.11/ -fPIC -o phylib_wrap.o
_phylib.so: libphylib.so phylib_wrap.o
	$(CC) $(CFLAGS) -shared phylib_wrap.o -L. -L/usr/lib/python3.11 -lpython3.11 -lphylib -o _phylib.so
clean:
	rm -f *.o *.so
