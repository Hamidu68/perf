rm invntt*.txt ntt*.txt
rm test_kyber512
make test_kyber512 NTTLOG=$1
./test_kyber512 > out.txt
