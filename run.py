from bar_chart import Plot_Bar
from Avg_Results import Avg_Results
from config import mixed_profile
from extract_data import *
import operator
import os
import sys
import numpy as np
import matplotlib.pyplot as plt


def mixed_tree(jungle_nodes, Avg_mix, Avg_Events_mix):
    for mix in mixed_profile.keys():
        list_func_mixed = []
        dict_mixed = {}
        mixed = []
        overal_percent = 0
        for func in (mixed_profile[mix]):
            mixed = mixed + jungle_nodes[func]
            overal_percent = int(overal_percent + jungle_nodes[func][0].percent)
        to_draw = calculate_exclusive(mixed, overal_percent)
        vis_call_graph(to_draw, write_dir + mix + "-mixed_graph_proned", 1)
        for item in mixed:
            # dict_func[item.name]=item.incl
            to_add = (item.name, [int(item.incl * overal_percent / 100)])
            if to_add not in list_func_mixed:
                list_func_mixed.append(to_add)
                list_func_mixed = sorted(list_func_mixed, key=operator.itemgetter(1), reverse=True)
        dict_mixed["cycles " + str(overal_percent)] = list_func_mixed
        if i is 0:
            Avg_mix[mix] = {}
            Avg_Events_mix[mix] = {}

        [Avg_mix[mix], Avg_Events_mix[mix]] = Avg_Results(dict_mixed, i, Avg_mix[mix], Avg_Events_mix[mix])

plt.close('all')
MAX_FUNC = 20 # maximum number of functions that we need to analyze
COUNT_EVENT = 10 # number of events to trigger a sample

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

BENCH_DIR = sys.argv[1]#"/home/hamid/phd/profiling/newhope/newhope/ref/test/test_newhope" #address to ob file
BNECH_NAME = sys.argv[2]#"newhope"

# BENCH_DIR= "/home/hamid/phd/profiling/perf-2018-DATE/dilithium_recommended/dilithium_recommended dilithium_recommended"
# BNECH_NAME="dilithium_recommended"


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

Avg_mix = {}
Avg_Events_mix = {}

mix_to_plot = {}

for i in range (0 , NUM_RUNS):
   os.system(CMD)
   print (CMD)

   os.system("sudo perf report -n > "+ All_Data)
   os.system("mkdir -p "+ Directory_Save_Results+"/"+str(i))
   write_dir = Directory_Save_Results+"/"+str(i)+"/"

   [Final_Dict,jungle_nodes] = Single_Run(i,All_Data, write_dir, COUNT_EVENT) # finla dict: the results which are written into the "Event" file

   #for iteration number 0, we shoud create the dictionary
   [Avg, Avg_Events] = Avg_Results(Final_Dict,i,Avg,Avg_Events)
   os.system("cp stdout.gz" + " " + write_dir + "/stdout_"+str(i)+".gz" ) #save the stdout

   mixed_tree(jungle_nodes, Avg_mix, Avg_Events_mix)
   print "Round "+str(i)+" is done"

#main function
Print_All_Results (Avg)
print Avg_Events
Plot_All_Parameters(Avg,1,Avg_Events,Directory_Save_Plots+"/")

#mixed; e.g., client and server
for mix in mixed_profile.keys():
    Print_All_Results (Avg_mix[mix]) #Avg_mix
    print Avg_Events_mix[mix] # Avg_Events_mix
    Plot_All_Parameters(Avg_mix[mix],1,Avg_Events_mix[mix],Directory_Save_Plots+"/"+mix+"-")

os.system("cp "+BENCH_DIR + " " + Directory_Save_Results )#save the obj file for the future!
os.system("cp functions.txt "+ Directory_Save_Results )#save the obj file for the future!
os.system("cp perf.data "+ Directory_Save_Results )#save the obj file for the future!
os.system("cp All_Data.txt "+ Directory_Save_Results )#save the obj file for the future!
os.system("sudo rm -f perf.data*")
os.system("sudo rm -f *.txt *.gz")
