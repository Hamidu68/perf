We can generate the call graph for any arbitrary function or even mixed of function!!; just run:

```
sh run.sh
```
It also generate barcharts for different functions or mixes.

You should change `config.py` file in order to change the functions to be profiled and the mixed functions (client and server).

# compile Flags
-No compiler optimizations (eliminate -O3, ...)
-Compiler with `-g` flag
-Do not elimiate `frame_pointers`

for example these are the flags from NIST dilithium:
```
CFLAGS = -Wall -Wextra -march=native -mtune=native -O3 -fomit-frame-pointer
```
and here are the prefered flags:
```
CFLAGS = -g -Wall -Wextra -march=native
```

----------------------------------------
# Examples

Examples for DATE paper can be found in [perf-2018-DATE](https://github.com/Hamidu68/perf/tree/master/perf-2018-DATE) folder.

-----------------------------------------


# config.py

First specify number of runs to get the average over all of them in the [config.py](https://github.com/Hamidu68/perf/blob/master/config.py) file.
```NUM_RUNS = 5
```

and also spcify number of functions and ignore functions that consume less that `THRESHOLD` of the whole algorithm.
```
MAX_FUNC = 20 # maximum number of functions that we need to analyze
THRESHOLD = 0.10 # function with less than threshold will not be considered
```

Then we should specify the `roots` and `mixed_profile` lists as below:
```
#`roots` is the array of functions we want to profile
roots = [   "main",
            "crypto_kem_keypair",
            "crypto_kem_enc",
            "crypto_kem_dec"
] #function which we want to draw the call graph

#from functions in the `roots` array, we can merge some with others to get the profiling for a party
mixed_profile = {"client": [
                    "crypto_kem_enc"
                            ],
                 "server":[
                    "crypto_kem_keypair",
                    "crypto_kem_dec"
                 ]
}
```



