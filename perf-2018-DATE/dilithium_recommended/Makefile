TEST_NAME = dilithium_recommended
SRCS = src/sign.c src/poly.c src/polyvec.c src/fips202.c src/reduce.c src/rounding.c src/packing.c src/randombytes.c
SRCS += src/main.c

# AES_H_DIR=src/include
# DIR_EXTRA_HEADER=$(AES_H_DIR) #used in Makefile.trace & Makefile.gem5

ifeq (${VERSION},base) #if we want to execute the base kyber (paper version)
	SRCS += src/ntt_base.c
else #if we want to optimized version (merged loop)
	SRCS += src/ntt.c
endif


all: $(SRCS)
	$(CC) -g $(SRCS) -Wall -Wextra -march=native -fPIC -o dilithium_recommended

clean:
	rm -f dilithium_recommended
	rm -f ./src/*.o
