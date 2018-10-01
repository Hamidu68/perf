
# TEST_NAME = $TEST_NAME

DIR = $(shell pwd) #ex: /home/hamid/phd/gem5-aladdin/src/aladdin/integration-test/with-cpu/NIST/newhope/newhope512cca
SOURCE_DIR=src/
SHARED_SRC=../shared_src/

SRC= cpapke.c fips202.c kem.c PQCgenKAT_kem.c precomp.c verify.c poly.c reduce.c rng.c aes_core.c aes_misc.c
SRCS= $(addprefix $(SOURCE_DIR),$(SRC))
AES_H_DIR=src/include

DIR_EXTRA_HEADER=$(AES_H_DIR) #used in Makefile.trace & Makefile.gem5

ifeq (${VERSION},base) #if we want to execute the base kyber (paper version)
	SRCS += $(SOURCE_DIR)/ntt_base.c
else #if we want to optimized version (merged loop)
	SRCS += $(SOURCE_DIR)/ntt.c
endif

#ACCEL: function that we want to generate its trace file which will be used inside an SoC (multiple accelerators connected to the CPU)
ifeq ($(KERNEL),) #no accel has been defined => just compile the code
	export WORKLOAD=main
	ACCEL=0
else	
	export WORKLOAD=${KERNEL}
	ACCEL=${KERNEL_ID}
endif

#if it's enabled, we want to dump stats after each invokation of the accel
ifndef DUMP_ACCEL_STATS
	OPTION2_VALUE = 0 #do not dump the stats
else
	OPTION2_VALUE = ${DUMP_ACCEL_STATS}  # 1: dump stats after each invocation; 0: do not dump the stats; 2:debugging
endif
OPTION2 = DUMP_ACCEL_STATS

#OUT=PQCgenKAT_kem
# CC=/usr/bin/gcc

all: $(SRCS)
	$(CC) -g $(SRCS) -Wall -Wextra -march=native -fPIC -I$(AES_H_DIR) -o newhope1024cpa
	# $(CC) -o $@ $(SRCS) $(LDFLAGS) -I$(SOURCE_DIR) -I$(AES_H_DIR)

#include $(INTEGRATION_TEST)/common/Makefile.tracer
#include $(INTEGRATION_TEST)/common/Makefile.gem5

clean:
	rm -f ./src/*.llvm
	rm -f ./src/*.o
	rm -f ./src/*.s
	rm -f *.gz
	rm -f *.o
	rm -f PQCgenKAT_kem
	make clean-gem5
	make clean-trace
	rm -f PQCkemKAT_1888.r*
