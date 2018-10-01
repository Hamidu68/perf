#ifndef REDUCE_H
#define REDUCE_H

#include <stdint.h>

uint16_t montgomery_reduce(uint32_t a);


static const uint32_t qinv = 12287; // -inverse_mod(p,2^18)
static const uint32_t rlog = 18;

#define montgomery_reduce_inline(a) { \
  uint32_t u; \
  u = (a * qinv); \
  u &= ((1<<rlog)-1); \
  u *= NEWHOPE_Q; \
  a = a + u; \
  a = a >> 18; \
}


#endif
