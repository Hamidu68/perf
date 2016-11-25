import operator
import os
from bar_chart import Plot_Bar
import numpy as np
import matplotlib.pyplot as plt

#directory for plots
Directory_Save_Plots = "Plots"
os.system("rm -r "+ Directory_Save_Plots)
os.system("mkdir "+ Directory_Save_Plots)


import random
plt.close('all')
NUM_RUNS = 5
MAX_FUNC = 10 # maximum number of functions that we need to analyze
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
               print line
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

Final_Dict = Read_Results("All_Data")


j =0
for key in Final_Dict.keys():
    print "----------------------------------------------------------------"
    value = []
    x_lable = []
    print key
    Total_Events = int(filter(str.isdigit, key))

    for key_i in range(0, min (MAX_FUNC, len(Final_Dict[key]))):
        print (Final_Dict[key])[key_i][0],((Final_Dict[key])[key_i][1])[0]
        value.append(((Final_Dict[key])[key_i][1])[0])
        x_lable.append(((Final_Dict[key])[key_i][0])[0:12])
    y_lable = key
    title   = key
    Plot_Bar(value,min(MAX_FUNC,len(Final_Dict[key])),x_lable, y_lable,title,Total_Events)
   # plt.show()
    plt.savefig (Directory_Save_Plots+"/"+(key)+'.png')
   # savefig('foo.png')