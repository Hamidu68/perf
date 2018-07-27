import operator
import os
import numpy as np
import matplotlib.pyplot as plt


NUM_RUNS = 5
MAX_FUNC = 20 # maximum number of functions that we need to analyze
THRESHOLD = 0.10 # function with less than threshold will not be considered

roots = [   "main",
            "crypto_kem_dec",
            "crypto_kem_enc",
            "crypto_kem_keypair"
] #function which we want to draw the call graph


mixed_profile = {"client": [
                    "crypto_kem_enc"
                            ],
                 "server":[
                    "crypto_kem_keypair",
                    "crypto_kem_dec"
                 ]
}