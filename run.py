
from bar_chart import Plot_Bar
from Avg_Results import Avg_Results
from config import *
from extract_data import *

os.system("mkdir -p results")
os.system("rm -rf "+ Directory_Save_Plots)
os.system("mkdir "+ Directory_Save_Plots)
os.system("sudo rm -f perf.data*")

import random
plt.close('all')

Avg = {}
Avg_Events = {}
All_Data = "All_Data.txt"

for i in range (0 , NUM_RUNS):
   os.system(CMD)
   os.system("sudo perf report -n > "+ All_Data)
   #os.system("cp")
   Final_Dict = Single_Run(i,All_Data) # finla dict: the results which are written into the "Event" file
   print "Round "+str(i)+" is done"

   #for iteration number 0, we shoud create the dictionary
   [Avg, Avg_Events] = Avg_Results(Final_Dict,i,Avg,Avg_Events)
   os.system("cp stdout.gz" + " " + Directory_Save_Results + "/stdout_"+str(i)+".gz" ) #save the stdout
Print_All_Results (Avg)
print Avg_Events
Plot_All_Parameters(Avg,1,Avg_Events)


os.system("cp "+BENCH_DIR + " " + Directory_Save_Results )#save the obj file for the future!
os.system("cp functions.txt "+ Directory_Save_Results )#save the obj file for the future!
os.system("sudo rm -f perf.data*")
os.system("sudo rm -f *.txt *.gz")
