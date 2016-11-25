import operator
import os
NUM_RUNS = 5
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

def Read_Stats (Raw_Data):
    newDict = {}
    RetDict = {}
    i = 0
    with open(Raw_Data, 'r') as f:
       for line in f:
           if line.startswith("#") or line.__contains__("[k]"):
               continue
           splitLine = line.split()
           key = splitLine[0]
           key = (key.replace("%",""))
           newDict[i] = [splitLine[0],splitLine[5]]
           i = i+1
           if i == MAX_FUNC:
               break
    for j in range(0 , min(MAX_FUNC,i)):
       key = (str(newDict[j][0])).replace("%","")
       func = (str(newDict[j][1]))
       RetDict[func] = key
      # print float (key), func
    return RetDict


Avg_Stats = {}
sorted_x = {}
j = 0
OBJ_FILE = "~/Dropbox/UCI/newhope-20160815/ref/test/test_newhope"
os.system("sudo rm raw_data*")
for var in Variants:
    for i in range (0,NUM_RUNS):
        if var == "Cycles":
            os.system("sudo perf record " + OBJ_FILE)
        else:
            os.system("sudo perf record -e "+var+" -c 100 " + OBJ_FILE)
        os.system("sudo perf report -n > raw_data"+str(i)+".txt")
        Dict = Read_Stats("raw_data"+str(i)+".txt")
        #os.system("sudo rm raw_data*")
        for key in Dict.iterkeys():
            #print Dict[key]
            if (i == 0):
                Avg_Stats [key] = 0;
            if key in Avg_Stats.keys():
                Avg_Stats[key] = ((float(Avg_Stats[key])*i+float(Dict[key]))/(i+1))
    #print Avg_Stats
    sorted_x = sorted(Avg_Stats.items(), key=operator.itemgetter(1), reverse=True)

    f = open(var,'w')
    for i in  range (0,len(sorted_x)):
        f.write(("{0:10} \t").format(str(sorted_x[i][1])))
        f.write(("{0:20}\n").format(str(sorted_x[i][0])))
    f.close()
#os.system("sudo rm raw_data*")




