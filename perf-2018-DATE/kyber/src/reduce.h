#ifndef REDUCE_H
#define REDUCE_H

#include <stdint.h>

uint16_t freeze(uint16_t x);

uint16_t montgomery_reduce(uint32_t a);

uint16_t barrett_reduce(uint16_t a);

static const uint32_t qinv1 = 7679; // -inverse_mod(q,2^18)
static const uint32_t rlog1 = 18;


#define montgomery_reduce_inline(a) { \
                uint32_t u; \
                u = (a * qinv1); \
                u &= ((1<<rlog1)-1); \
                u *= KYBER_Q; \
                a = a + u; \
                a =  a >> rlog1; \
}

#endif
