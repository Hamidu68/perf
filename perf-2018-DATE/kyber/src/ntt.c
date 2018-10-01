#include "inttypes.h"
#include "ntt.h"
#include "params.h"
#include "reduce.h"

extern const uint16_t omegas_inv_bitrev_montgomery[];
extern const uint16_t psis_inv_montgomery[];
extern const uint16_t zetas[];

#include <stdio.h>

// FILE * pFile_invntt;
// FILE * pFile_ntt;

static const uint32_t qinv = 7679; // -inverse_mod(q,2^18)
static const uint32_t rlog = 18;
/*************************************************
* Name:        ntt
* 
* Description: Computes negacyclic number-theoretic transform (NTT) of
*              a polynomial (vector of 256 coefficients) in place; 
*              inputs assumed to be in normal order, output in bitreversed order
*
* Arguments:   - uint16_t *p: pointer to in/output polynomial
**************************************************/
// void ntt(uint16_t *p) 
// {
//   int level, start, j, k;
//   uint16_t zeta, t;

//   // pFile_ntt  = fopen ("ntt.txt","a");

//   k = 1;
//   for(level = 7; level >= 0; level--) 
//   {
//     // fprintf(pFile_ntt,"---------------------------level: %d\n",level);
//     for(start = 0; start < KYBER_N; start = j + (1<<level)) 
//     {
//       zeta = zetas[k++];
//       for(j = start; j < start + (1<<level); ++j) 
//       {
//         t = montgomery_reduce((uint32_t)zeta * p[j + (1<<level)]);

//         p[j + (1<<level)] = barrett_reduce(p[j] + 4*KYBER_Q - t);

//         if(level & 1) /* odd level */
//           p[j] = p[j] + t; /* Omit reduction (be lazy) */
//         else 
//           p[j] = barrett_reduce(p[j] + t);
//   //       fprintf(pFile_ntt,"k:%3d - j:%3d -start:%3d - a[%3d] - a[%3d] - zeta:%5d\n",k-1,j,start,j,j + (1<<level),zeta);
//       }
//     }
//   }
//   // fclose (pFile_ntt);
// }

void ntt(uint16_t *p) 
{
  int level, start, j, k;
  uint16_t zeta, t;
  uint32_t mask; //to determine if j is a multiple of (1<<level+1)

  uint16_t temp, W;
  uint32_t m1, m2;
  uint32_t bar;
  uint32_t u;
  uint32_t monte, monte_tmp; //it should be uint32_t,


  // pFile_ntt  = fopen ("ntt2.txt","a");

  int distance, idx;

  k = 0;
  for(level = 7; level >= 0; level--) 
  {
    distance = 1 << level;
 // fprintf(pFile_ntt,"---------------------------level: %d\n",level);
    loop: for (idx=0; idx<KYBER_N/2; idx++)
    {
      
      start = idx & (distance-1);
      j = (((idx & (~(distance - 1))) <<1 ) & (KYBER_N-1)) + start;
      
      
      mask = ((1<<(level+1))-1)&j;
      k += !(mask &&& mask);
      zeta = zetas[k];
     
      //montgomery_reduce
      monte_tmp = ((uint32_t)zeta * p[j + (1<<level)]);
      u = (monte_tmp * qinv);
      u &= ((1<<rlog)-1);
      u *= KYBER_Q;
      monte_tmp = monte_tmp + u;
      monte_tmp >> rlog;
      t = monte_tmp >> rlog;

      //barret reduction
      temp = (p[j] + 4*KYBER_Q - t); 
      u = (temp) >> 13;
      u *= KYBER_Q;
      p[j + (1<<level)] = temp - u;

      //barret reduction
      temp = p[j];
      m1 = ~(level & 0x0001) + 1;
      m2 = (level & 0x0001) - 1;
      u = ((uint32_t) (temp + t) ) >> 13;
      u *= KYBER_Q;
      bar = (temp + t) - u;
      p[j] = ((m1)&bar) | ((m2)&(temp+ t)); //TODO: lazy reduction and compare it with this

     // fprintf(pFile_ntt,"k:%3d - j:%3d -start:%3d - a[%3d] - a[%3d] - zeta:%5d\n",k,j,start,j,j + (1<<level),zeta);
    }
  }
  // fclose (pFile_ntt);
}

// void invntt(uint16_t * a)
// {

//   // pFile_invntt  = fopen ("invntt.txt","a");


//   int start, j, jTwiddle, level;
//   uint16_t temp, W;
//   uint32_t t;

//   for(level=0;level<8;level++)
//   {
//     // fprintf(pFile_invntt,"--------------------------------level: %d\n",level);
//     for(start = 0; start < (1<<level);start++)
//     {
//       jTwiddle = 0;
//       for(j=start;j<KYBER_N-1;j+=2*(1<<level))
//       {
        
//         W = omegas_inv_bitrev_montgomery[jTwiddle++];
//         temp = a[j];

//         if(level & 1) /* odd level */
//           a[j] = barrett_reduce((temp + a[j + (1<<level)]));
//         else
//           a[j] = (temp + a[j + (1<<level)]); /* Omit reduction (be lazy) */
        
//         t = (W * ((uint32_t)temp + 4*KYBER_Q - a[j + (1<<level)]));
//         // fprintf(pFile_invntt,"start:%3d - W:%5d - temp:%5d -%10d: -",start,W,temp,t);

//         a[j + (1<<level)] = montgomery_reduce(t);
//         // fprintf(pFile_invntt,"a[%3d]:%5d - a[%3d]:%5d\n",j,a[j], j + (1<<level), a[j + (1<<level)]);
//       }
//     }
//   }

//   for(j = 0; j < KYBER_N; j++)
//     a[j] = montgomery_reduce((a[j] * psis_inv_montgomery[j]));

//   // fclose (pFile_invntt);
  
// }

/*************************************************
* Name:        invntt
* 
* Description: Computes inverse of negacyclic number-theoretic transform (NTT) of
*              a polynomial (vector of 256 coefficients) in place; 
*              inputs assumed to be in bitreversed order, output in normal order
*
* Arguments:   - uint16_t *a: pointer to in/output polynomial
**************************************************/
void invntt(uint16_t * a)
{
  // pFile_invntt  = fopen ("invntt2.txt","a");

  int i, start, j, jTwiddle, distance, k;
  uint16_t temp, W;
  uint32_t m1, m2;
  uint32_t bar;
  uint32_t u;
  uint32_t monte, monte_tmp; //it should be uint32_t,

  for(i=0;i<8;i+=1)
  {
    // fprintf(pFile_invntt,"--------------------------------level: %d\n",i);
    distance = (1<<i);
    loop: for (k=0; k<KYBER_N/2; k++)
    {
      start = k & (distance-1);
      j = (((k & (~(distance - 1))) <<1 ) & (KYBER_N-1)) + start;
      jTwiddle = j >> (i+1);

      W = omegas_inv_bitrev_montgomery[jTwiddle++];
      temp = a[j];
      m1 = ~(i & 0x0001) + 1;
      m2 = (i & 0x0001) - 1;
      u = ((uint32_t) (temp + a[j + distance]) ) >> 13;
      u *= KYBER_Q;
      bar = (temp + a[j + distance]) - u;
      a[j] = ((m1)&bar) | ((m2)&(temp+ a[j + distance])); //TODO: lazy reduction and compare it with this

      monte_tmp = (W * ((uint32_t)temp + 4*KYBER_Q - a[j + distance]));
      // fprintf(pFile_invntt,"start:%3d - W:%5d - temp:%5d -%10d: -",start, W,temp,monte_tmp);
    
      u = (monte_tmp * qinv);
      u &= ((1<<rlog)-1);
      u *= KYBER_Q;
      monte_tmp = monte_tmp + u;
      monte_tmp >> rlog;
      a[j + distance] = monte_tmp >> rlog;
    //  fprintf(pFile_invntt,"a[%3d]:%5d - a[%3d]:%5d\n",j,a[j], j + distance, a[j + distance]);
    }
  }

loop2: for(j = 0; j < KYBER_N; j++) //TODO: unrool this loop
  {
    monte_tmp = (a[j] * psis_inv_montgomery[j]);
    montgomery_reduce_inline(monte_tmp);
    a[j]=monte_tmp;
  }

  // fclose (pFile_invntt);
}

