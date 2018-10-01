#include "params.h"
#include "reduce.h"
#include "ntt.h"
#include "poly.h"

/*************************************************
* Name:        ntt
* 
* Description: Forward NTT, in-place. No modular reduction is performed after
*              additions or subtractions. Hence output coefficients can be up
*              to 16*Q larger than the coefficients of the input polynomial.
*              Output vector is in bitreversed order.
*
* Arguments:   - uint32_t *p: pointer to polynomial to be transformed
**************************************************/
void ntt(uint32_t *p) {
  unsigned int len, start, j, k,r,h;
  uint32_t zeta, t;
  uint64_t mont_temp;

  k = 0;
  for(len = 128; len > 0; len >>= 1) {

    loop:  for(r = 0; r < N/2; ++r) {

        //for(start = 0; start < N; start = j + len) {
        if( r%len==0) k++;
        zeta = zetas[k];
        //for(j = start; j < start + len; ++j) {
        h = r/len;
        j=(r%len)+(h)*2*len;

        /*montogemry reduction*/
        mont_temp = (uint64_t)zeta * p[j + len];
        montgomery_reduce_inline(mont_temp);
        t = mont_temp;

        p[j + len] = p[j] + 2*Q - t;
        p[j] = p[j] + t;
      }
    }
  }


/*************************************************
* Name:        invntt_frominvmont
* 
* Description: Inverse NTT, in-place. No modular reductions after additions or
*              subtractions. Output coefficients can be up to 256*Q larger than
*              input coefficients. Multiplies with Montgomery factor 2^32.
*
* Arguments:   - uint32_t *p: pointer to vector to be transformed
**************************************************/
void invntt(uint32_t *p) {
  unsigned int start, len, j, r,h;
  int k;
  uint32_t t, zeta;
  uint64_t mont_temp;

  const uint32_t f = (((uint64_t)MONT*MONT % Q) * (Q-1) % Q) * ((Q-1) >> 8) % Q;

  k = -1;
  for(len = 1; len < N; len <<= 1) {

   loop: for(r = 0; r < N/2; ++r) {
    //for(start = 0; start < N; start = j + len) {
       if( r%len==0) k++;
       zeta = zetas_inv[k];
       //zeta = zetas_inv[k++];
      //for(j = start; j < start + len; ++j) {

        h = r/len;
        j=(r%len)+(h)*2*len;
        t = p[j];
        p[j] = t + p[j + len];
        p[j + len] = t + 256*Q - p[j + len];
        
        /*montogemry reduction*/
        mont_temp = (uint64_t)zeta * p[j + len];
        montgomery_reduce_inline(mont_temp);
        p[j + len] = mont_temp;
      }
    }
  

  loop2: for(j = 0; j < N; ++j) {
    /*montogemry reduction*/
    mont_temp = (uint64_t)f * p[j];
    montgomery_reduce_inline(mont_temp);
    p[j] = mont_temp;
  }
}
