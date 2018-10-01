CC=/usr/bin/gcc
LDFLAGS=-lcrypto

#DIR=/home/hamid/phd/pqc-collaboration/NewHope/Reference_Implementation/crypto_kem/newhope512cca/

SOURCE_DIR=$(DIR)/
SHARED_SRC=$(DIR)/../src

SRCS= cpapke.c fips202.c kem.c PQCgenKAT_kem.c precomp.c rng.c verify.c
SOURCES= $(addprefix $(SOURCE_DIR),$(SRCS))
SOURCES += $(SHARED_SRC)/poly.c $(SHARED_SRC)/reduce.c


HDRS= api.h cpapke.h fips202.h rng.h verify.h 
HEADERS= $(addprefix $(SOURCE_DIR),$(HDRS))
HEADERS += $(SHARED_SRC)/reduce.h


OUT=PQCgenKAT_kem

ifeq (${VERSION},base) #if we want to execute the base kyber (paper version)
	SOURCES += $(SHARED_SRC)/ntt_base.c
	OUT=PQCgenKAT_kem-base
else #if we want to my version (merged loop)
	SOURCES += $(SHARED_SRC)/ntt.c
endif

ifeq (${SANITY},) #no sanity check
	SANITY=0
endif

$(OUT): $(HEADERS) $(SOURCES)
	$(CC) -DSANITY=$(SANITY) -o $@ $(SOURCES) $(LDFLAGS) -I$(SOURCE_DIR)

.PHONY: clean

clean:
	-rm $(OUT) 
