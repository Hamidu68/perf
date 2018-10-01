import operator
import os
import numpy as np
import matplotlib.pyplot as plt


NUM_RUNS = 5
MAX_FUNC = 20 # maximum number of functions that we need to analyze
THRESHOLD = 0.10 # function with less than threshold will not be considered


#####For DS
roots = [   "main",
            "crypto_sign_keypair",
            "crypto_sign",
            "crypto_sign_open"
] #function which we want to draw the call graph


mixed_profile = {"sign": [
                    "crypto_sign"
                            ],
                 "verify":[
                    "crypto_sign_open",
                 ]
}









####################for KEM
# roots = [   "main",
#             "crypto_kem_keypair",
#             "crypto_kem_enc",
#             "crypto_kem_dec"
# ] #function which we want to draw the call graph


# mixed_profile = {"client": [
#                     "crypto_kem_enc"
#                             ],
#                  "server":[
#                     "crypto_kem_keypair",
#                     "crypto_kem_dec"
#                  ]
# }