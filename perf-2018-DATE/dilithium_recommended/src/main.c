#include <stdio.h>
#include "api.h"
#include "randombytes.h"
#include "params.h"

#define MLEN 59
#define NTESTS 10000


int main(void)
{
  unsigned int i;
  int ret;
  unsigned long long j, mlen, smlen;
  unsigned char m[MLEN]={0};
  unsigned char sm[MLEN + CRYPTO_BYTES];
  unsigned char m2[MLEN + CRYPTO_BYTES];
  unsigned char pk[CRYPTO_PUBLICKEYBYTES];
  unsigned char sk[CRYPTO_SECRETKEYBYTES];

  for(i = 0; i < NTESTS; ++i) {
    // randombytes(m, MLEN);

    crypto_sign_keypair(pk, sk);

    crypto_sign(sm, &smlen, m, MLEN, sk);

    ret = crypto_sign_open(m2, &mlen, sm, smlen, pk);
  }
    

}




// int main(void)
// {
//   unsigned int i;
//   int ret;
//   unsigned long long j, mlen, smlen;
//   unsigned char m[MLEN]={0};
//   unsigned char sm[MLEN + CRYPTO_BYTES];
//   unsigned char m2[MLEN + CRYPTO_BYTES];
//   unsigned char pk[CRYPTO_PUBLICKEYBYTES];
//   unsigned char sk[CRYPTO_SECRETKEYBYTES];

//   for(i = 0; i < NTESTS; ++i) {
//     // randombytes(m, MLEN);

//     crypto_sign_keypair(pk, sk);

// #if !defined(LLVM_TRACE)
//     m5_reset_stats(0,0);
//     crypto_sign(sm, &smlen, m, MLEN, sk);
//     m5_dump_stats(0,0);
//     m5_mynewop(SERVER,1);
// #else
//     crypto_sign(sm, &smlen, m, MLEN, sk);
// #endif

// #if !defined(LLVM_TRACE)
//     ret = crypto_sign_open(m2, &mlen, sm, smlen, pk);
//     m5_dump_stats(0,0);
//     m5_mynewop(CLIENT,1);
// #else
//     ret = crypto_sign_open(m2, &mlen, sm, smlen, pk);
// #endif
    
//     if(ret) {
//       printf("Verification failed\n");
//       return -1;
//     }

//     if(mlen != MLEN) {
//       printf("Message lengths don't match\n");
//       return -1;
//     }

//     for(j = 0; j < mlen; ++j) {
//       if(m[j] != m2[j]) {
//         printf("Messages don't match\n");
//         return -1;
//       }
//     }

//     printf("i:%d Signature verified successfully\n",i);
//   }

//   return 0;
// }
