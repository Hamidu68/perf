import operator
import os
NUM_RUNS = 100
MAX_FUNC = 10 # maximum number of functions that we need to analyze
Variants = ["Cycles",
            "cache-references",
            "cache-misses"
         #   "branches",
         #   "branch-misses",
         #   "L1-dcache-load-misses",
         #   "L1-dcache-loads",
         #   "L1-dcache-stores",
         #   "L1-icache-load-misses",
         #   "LLC-load-misses",
         #   "LLC-loads",
         #   "LLC-store-misses",
         #   "LLC-stores"
]
def make_all():
    newDict = {}

   #tuple_list = []
    i = 0
    for var in Variants:
        with open(var, 'r') as f:
           for line in f:
               splitLine = line.split()
               key = splitLine[1]
              # print tuple_list
               if key in newDict.keys():
                   tuple_list = newDict[key]
                   tuple_list.append([var, splitLine[0]])
                   newDict[key] = tuple_list
               else:
                    newDict [key] = [ var, splitLine[0]]
               i = i+1
    return newDict

RetDict = make_all()
for i in RetDict.keys():
    print i, ": ",RetDict[i]
    print i, ": ", RetDict[i][0]
    print i, ": ", RetDict[i][1]
    print i, ": ", RetDict[i][2]
    print i, ": ", RetDict[i][3]



