CC = /usr/bin/cc
CFLAGS = -Wall -Wextra -march=native -mtune=native -O3 -fomit-frame-pointer
NISTFLAGS = -O3 -fomit-frame-pointer -march=native -fPIC
SOURCES = sign.c polyvec.c packing.c poly.c reduce.c ntt.c rounding.c fips202.c
HEADERS = api.h params.h sign.h polyvec.h packing.h poly.h reduce.h ntt.h \
  rounding.h fips202.h

all: test_dilithium

test_dilithium: $(SOURCES) randombytes.c test_dilithium.c $(HEADERS) randombytes.h 
	$(CC) $(CFLAGS) $(SOURCES) randombytes.c test_dilithium.c -o $@

.PHONY: clean

clean:
	rm -f test_dilithium
