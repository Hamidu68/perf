from parse_perf_output import parse_perf_output, build_tree, vis_call_graph
from config import *
from bar_chart import Plot_Bar
from copy import deepcopy


class Function:
    def __init__(self,
                 name, #name of the function
                 inclusive_percent, #amount of cpu cycles spent in this function with the children
                 exclusive_percent #amount of cpu cycles spent in this function without the children
                 ):
        self.name = name
        self.inclusive_percent = inclusive_percent
        self.exclusive_percent = exclusive_percent


#print the dictionary which consists of all of the results
def Print_All_Results(Final_Dict): #IS_Avg == 1: we need to plot average results, so Total_Events should be average!
    f_write = open("Avg_Results", 'w')
    for key in Final_Dict.keys(): #ex: key=cycles

        f_write.write("--- ")
        f_write.write(key + "\n")
        # for less amount of functions, we can use "min" in the range!!!
        for key_i in range(0, min(MAX_FUNC, len(Final_Dict[key]))):
            tmp_str = str((Final_Dict[key])[key_i][0]) + "  " + str(((Final_Dict[key])[key_i][1])[0]) + "\n"
            f_write.write(tmp_str)

def Plot_All_Parameters (Final_Dict,Is_Avg,Avg_Events,Directory_Save_Plots):
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

        plt.savefig(Directory_Save_Plots + (key) + '.pdf',format='eps', dpi=1000)

    file_func.close()

def Read_Results (Raw_Data,COUNT_EVENT):
    function_list = []
    newDict = {}
    RetDict = {}
    Final_Dict = {}
    Final_function_list={}
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
               event_count =  int (nextline[-1])/COUNT_EVENT
               new_paramter = new_paramter+" "+ str(event_count)
               #event_count = int(splitline[2].replace("k", ""))  # 11k

           # read the call percentage for each function which is contain '[.]'. if there is no call to this function
           # ignore the line!
           if line.__contains__("[.]") and (not(line.__contains__("0.00%"))):
               splitline = line.split()
               func = {splitline[-1]: [int(splitline[2])]}
               RetDict [splitline[-1]] = [int(splitline[2])]
               sorted_x = sorted(RetDict.items(), key=operator.itemgetter(1), reverse=True)

           if line.__contains__("[.]"):
               splitline = line.split()
               inclusive = splitline[0]
               exclusive = splitline[1]
               name = splitline[-1]
               function_list.append(Function(name,inclusive,exclusive))

       # last paramtere!
       Final_Dict[new_paramter] = sorted_x
       Final_function_list[new_paramter]=function_list #
    return [function_list, Final_Dict, event_count]


def calculate_exclusive(call_tree_in, root_percent):
    call_tree = deepcopy(call_tree_in)
    for caller in call_tree:  # key is the caller function
        for callee in caller.kids:
            callee.percent = "{0:.2f}".format (100* float(callee.percent)/root_percent)


    out_calls = {}
    in_calls = {}
    for caller in call_tree:  # key is the caller function
        for callee in caller.kids:
            caller.excl = caller.excl + float(callee.percent)
            if callee.name not in in_calls.keys():
                in_calls[callee.name] = float(callee.percent)
            else:
                in_calls[callee.name] = in_calls[callee.name] + float(callee.percent)


        if caller.name not in out_calls.keys():
            out_calls[caller.name] = caller.excl
        else:
            out_calls[caller.name] = out_calls[caller.name] + caller.excl

    for index in range(len(call_tree)):  # key is the caller function
        caller = call_tree[index]
        if caller.name in in_calls.keys():
            caller.incl = in_calls[caller.name] - out_calls[caller.name]
            call_tree_in[index].incl = caller.incl
            caller.name = caller.name +"\n("+ str(in_calls[caller.name]) +","+ str(in_calls[caller.name]-out_calls[caller.name])+")"

        else:
            caller.name = caller.name + "\n" + str(out_calls[caller.name])

    return call_tree

def Single_Run(Num_Run, All_Data,Directory_Save_Results,COUNT_EVENT):
    [function_list,Final_Dict,event_count] = Read_Results(All_Data,COUNT_EVENT)

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


    jungle_nodes = {}
    #generate the graph for the specified function
    for root in roots:
        list_nodes = parse_perf_output("All_Data.txt",root,event_count)
        build_tree(list_nodes,root)
        jungle_nodes[root] = list_nodes

        # vis_call_graph(list_nodes, write_dir + "_" + root +"_graph",THRESHOLD,list_nodes[0].percent)
        to_draw = calculate_exclusive(list_nodes, list_nodes[0].percent)
        vis_call_graph(to_draw, write_dir + "_" + root + "_graph_proned", 1)






    return [Final_Dict,jungle_nodes]



