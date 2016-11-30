import operator
import os
from bar_chart import Plot_Bar
from Avg_Results import Avg_Results
import numpy as np
import matplotlib.pyplot as plt

#directory for plots
Directory_Save_Plots = "Plots"
os.system("rm -r "+ Directory_Save_Plots)
os.system("mkdir "+ Directory_Save_Plots)

#directory of text results
Directory_Save_Results = "Results"
os.system("rm -r "+ Directory_Save_Results
          )
os.system("mkdir "+ Directory_Save_Results)



import random
plt.close('all')
NUM_RUNS = 5
MAX_FUNC = 20 # maximum number of functions that we need to analyze
COUNT_EVENT = 1000 # number of events to trigger a sample
Variants = ["Cycles"
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

#print the dictionary which consists of all of the results
def Print_All_Results(Final_Dict): #IS_Avg == 1: we need to plot average results, so Total_Events should be average!
    f_write = open("Avg_Results", 'w')
    for key in Final_Dict.keys():

        f_write.write("--- ")
        f_write.write(key + "\n")
        # for less amount of functions, we can use "min" in the range!!!
        for key_i in range(0, min(MAX_FUNC, len(Final_Dict[key]))):
            tmp_str = str((Final_Dict[key])[key_i][0]) + "  " + str(((Final_Dict[key])[key_i][1])[0]) + "\n"
            f_write.write(tmp_str)

def Plot_All_Parameters (Final_Dict,Is_Avg,Avg_Events):
    for key in Final_Dict.keys():
        if key.__contains__("cache-references"):
            key_cache_references = key
            break

    Total_Events = []
    j = 0
    #write_dir = Directory_Save_Results+"/"+"Events_"+str(Num_Run)
    #f_write = open(write_dir, 'w')
    #f_write.write("Maximum number of functions to analysis " + str(MAX_FUNC) + "\n")++
    file_func = open("functions.txt",'w')

    for key in Final_Dict.keys():
        if key.__contains__("cache-misses"):
            key_cache_misses = key
        elif key.__contains__("cache-references"):
            key_cache_references = key
        #f_write.write("--- ")
        value = []
        x_lable = []

        Total_Events = []

        # for less amount of functions, we can use "min" in the range!!!
        for key_i in range(0, min(MAX_FUNC, len(Final_Dict[key]))):

            #ex: montgomery_reduce  73
            tmp_str = str((Final_Dict[key])[key_i][0]) + "  " + str(((Final_Dict[key])[key_i][1])[0]) + "\n"

            value.append(((Final_Dict[key])[key_i][1])[0])
            x_lable.append(((Final_Dict[key])[key_i][0])[0:12])

            #print functions : used in annotation!!
            if key.__contains__("cycles"):
                file_func.write ((Final_Dict[key])[key_i][0]+"\n")



            if key.__contains__("cache-misses"):
               if Is_Avg == 1:
                    Total_Events.append((Final_Dict[key_cache_references])[key_i][1][0])
               else:
                    Total_Events.append((Final_Dict[key_cache_references])[0][1][0])
            else:
                if Is_Avg == 1:
                    Total_Events.append(Avg_Events[key])
                else:
                    Total_Events.append(int(filter(str.isdigit, key)))
        y_lable = key
        title = key+ str (Avg_Events[key])
        #  Total_Events[key] = int(filter(str.isdigit, key))
        # if key.__contains__("cache-misses"):

        Plot_Bar(value, min(MAX_FUNC, len(Final_Dict[key])), x_lable, y_lable, title, Total_Events)

        plt.savefig(Directory_Save_Plots + "/" + (key) + '.png')

    file_func.close()

def Read_Results (Raw_Data):
    newDict = {}
    RetDict = {}
    Final_Dict = {}
    new_paramter = ""
    sorted_x = {}
    i = 0
    with open(Raw_Data, 'r') as f:
       for line in f:
           #there is a new parameter to sample!!!
           if line.__contains__("Samples: ") and line.__contains__("of event"):
               if i == 0 :
                   i = i+1
               else:
                   Final_Dict[new_paramter] = sorted_x
               #print line
               splitline = line.split() # ex:   Samples: 11K of event 'cycles:u'
               # new parameters that we have the samples!!!
               new_paramter =  splitline[-1][1:-3]
               nextline = f.next().split()
               evencount =  int (nextline[-1])/COUNT_EVENT
               new_paramter = new_paramter+" "+ str(evencount)
               #evencount = int(splitline[2].replace("k", ""))  # 11k

           # read the call percentage for each function which is contain '[.]'. if there is no call to this function
           # ignore the line!
           if line.__contains__("[.]") and (not(line.__contains__("0.00%"))):
               splitline = line.split()
               func = {splitline[-1]: [int(splitline[2])]}
               RetDict [splitline[-1]] = [int(splitline[2])]
               sorted_x = sorted(RetDict.items(), key=operator.itemgetter(1), reverse=True)

       # last paramtere!
       Final_Dict[new_paramter] = sorted_x
    return Final_Dict

def Single_Run(Num_Run, All_Data):
    Final_Dict = Read_Results(All_Data)

    # to retrieve number of cache misses/cache references in each function!!!
    for key in Final_Dict.keys():
        if key.__contains__("cache-references"):
            key_cache_references = key
    j = 0
    write_dir = Directory_Save_Results+"/"+"Events_"+str(Num_Run)
    f_write = open(write_dir, 'w')
    f_write.write("Maximum number of functions to analysis " + str(MAX_FUNC) + "\n")
    for key in Final_Dict.keys():
        f_write.write("-----------------")
        f_write.write(key + "\n")
        # for less amount of functions, we can use "min" in the range!!!
        for key_i in range(0, min(MAX_FUNC, len(Final_Dict[key]))):
            tmp_str = str((Final_Dict[key])[key_i][0]) + "  " + str(((Final_Dict[key])[key_i][1])[0]) + "\n"
            f_write.write(tmp_str)
    f_write.close()
    #Plot_All_Parameters(Final_Dict)
    return Final_Dict

OBJ_FILE = "~/Dropbox/UCI/newhope-20160815/ref/test/test_newhope"
To_Profile = "cycles:u,instructions:u,cache-references:u,cache-misses:u"
Avg = {}
Avg_Events = {}
All_Data = "All_Data.txt"
#os.system("sudo rm *.txt")
for i in range (0 , NUM_RUNS):
   # os.system("sudo perf record -e cycles:u,instructions:u,cache-references:u,cache-misses:u -g -c 1000 ../test/test_newhope")
   # os.system("sudo perf report -n > "+ All_Data)
    Final_Dict = Single_Run(i,All_Data) # finla dict: the results which are written into the "Event" file
    print "Round "+str(i)+" is done"

   #for iteration number 0, we shoud create the dictionary
    [Avg, Avg_Events] = Avg_Results(Final_Dict,i,Avg,Avg_Events)
Print_All_Results (Avg)
print Avg_Events
Plot_All_Parameters(Avg,1,Avg_Events)
