from bar_chart import Plot_Bar
from Avg_Results import Avg_Results
#from config import *
from extract_data import *
import operator
import os
import sys
import numpy as np
import matplotlib.pyplot as plt


import random
plt.close('all')
MAX_FUNC = 20 # maximum number of functions that we need to analyze
COUNT_EVENT = 10 # number of events to trigger a sample
roots = ["main", "crypto_kem_dec", "crypto_kem_enc", "crypto_kem_keypair"]

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

if not len(sys.argv) == 3:
    print len(sys.argv)
    print("error in argument: python run.py [benchdir] [bencname]")
    print("ex: python extractPareto.py /home/hamid/phd/profiling/newhope/newhope/ref/test/test_newhope newhope")
   # exit()

# BENCH_DIR = sys.argv[1]#"/home/hamid/phd/profiling/newhope/newhope/ref/test/test_newhope" #address to ob file
# BNECH_NAME = sys.argv[2]#"newhope"

BENCH_DIR = "./test_kyber512"
BNECH_NAME = "kyber512"


ToProfile = "cycles:u"#,instructions:u,cache-references:u,cache-misses:u"
CMD = "sudo perf record -e " + ToProfile + " -g -c "+ str(COUNT_EVENT)+ " " + BENCH_DIR + " gzip -c > stdout.gz"

#directory of text results
Directory_Save_Results = "results/"+BNECH_NAME

#directory for plots
Directory_Save_Plots = Directory_Save_Results


os.system("mkdir -p results")
os.system("rm -rf "+ Directory_Save_Plots)
os.system("mkdir -p "+ Directory_Save_Plots)
os.system("sudo rm -f perf.data*")


Avg = {}
Avg_Events = {}
All_Data = "All_Data.txt"

for i in range (0 , NUM_RUNS):
   os.system(CMD)
   print (CMD)

   os.system("sudo perf report -n > "+ All_Data)
   os.system("mkdir -p "+ Directory_Save_Results+"/"+str(i))


   Final_Dict = Single_Run(i,All_Data,Directory_Save_Results+"/"+str(i),COUNT_EVENT,roots) # finla dict: the results which are written into the "Event" file

   print "Round "+str(i)+" is done"

   #for iteration number 0, we shoud create the dictionary
   [Avg, Avg_Events] = Avg_Results(Final_Dict,i,Avg,Avg_Events)
   os.system("cp stdout.gz" + " " + Directory_Save_Results+"/"+str(i) + "/stdout_"+str(i)+".gz" ) #save the stdout
Print_All_Results (Avg)
print Avg_Events
Plot_All_Parameters(Avg,1,Avg_Events,Directory_Save_Plots)


os.system("cp "+BENCH_DIR + " " + Directory_Save_Results )#save the obj file for the future!
os.system("cp functions.txt "+ Directory_Save_Results )#save the obj file for the future!
os.system("cp perf.data "+ Directory_Save_Results )#save the obj file for the future!
os.system("cp All_Data.txt "+ Directory_Save_Results )#save the obj file for the future!
os.system("sudo rm -f perf.data*")
os.system("sudo rm -f *.txt *.gz")
