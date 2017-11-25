import operator
import os
import numpy as np
import matplotlib.pyplot as plt


NUM_RUNS = 5
MAX_FUNC = 20 # maximum number of functions that we need to analyze
COUNT_EVENT = 1000 # number of events to trigger a sample
Variants = ["cycles"
            ,"cache-references"
            ,"cache-misses"
            ,"instructions"
         #   ,"branches"
         #   ,"branch-misses"
         #   ,"L1-dcache-load-misses"
         #   ,"L1-dcache-loads"
         #   ,"L1-dcache-stores"
         #   ,"L1-icache-load-misses"
         #   ,"LLC-load-misses"
         #   ,"LLC-loads"
         #   ,"LLC-store-misses"
         #   ,"LLC-stores"
]

# functions = [
#     "montgomery_reduce",
#     "ntt",
#     "crypto_core_chacha20",
#     "poly_getnoise",
#     "KeccakF1600_StatePermute",
#     "barrett_reduce"
#     "store_littleendian",
#     "g",
#     "load_littleendian",
#     "poly_uniform",
#     "store64",
#     "poly_frombytes",
#     "mul_coefficients",
#     "poly_tobytes",
#     "crypto_stream_chacha20",
#     "abs",
#     "poly_pointwise",
#     "f",
#     "rec",
#     "load64"
# ]

BENCH_DIR = "~/Desktop/hope/newhope/ref/test/test_newhope"
BNECH_NAME = "newhope"
ToProfile = "cycles:u,instructions:u,cache-references:u,cache-misses:u"
CMD = "sudo perf record -e " + ToProfile + " -g -c "+ str(COUNT_EVENT)+ " " + BENCH_DIR

#directory of text results
Directory_Save_Results = "Results/"+BNECH_NAME

#directory for plots
#Directory_Save_Plots = "Plots/"+BNECH_NAME
Directory_Save_Plots = Directory_Save_Results