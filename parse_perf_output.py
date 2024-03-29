from __future__ import print_function
import re
from ast import parse
from visual_call_tree import vis_call_graph

def is_valid_variable_name(name):
    try:
        parse('{} = None'.format(name))
        return True
    except SyntaxError, ValueError:
        return False

class Node:
    def __init__(self,
                 name, #name of the function
                 percent, #amount of cpu cycles spent in this function
                 n_dash, #number of dashes in the line after the function
                 dash # dashes in the line of the function
                 ):
        self.name = name
        self.percent = percent
        self.n_dash = n_dash
        self.dash = dash
        self.incl = 0 #including percentage
        self.excl = 0 #exclusing percentage
        self.kids = [] #keeps id of the kids!

    def __eq__(self, other):
        return (self.name == other.name and self.percent ==other.percent)

def parse_perf_output (Raw_Data, root_func, event_count):
    list_nodes = []
    with open(Raw_Data, 'r') as f:
       for line in f:
           # read the call percentage for each function which is contain '[.]'. if there is no call to this function
           # ignore the line!
           if ((line.__contains__("[.] "+root_func))): #root_func: e.g., main
               list_nodes.insert(0, Node(root_func, float(line.split()[0][:-1])*event_count/100, 0, 0))
               while( not line.__contains__("|--")):#start of the tree
                   line = f.next()
               while (line.__contains__("|") or line.__contains__("--")): #read until reach end of main!!!
                   splitline = line.split("--") #ex: --17.95%-- char_pool_refresh # Modification added to split line based on '--'
                   percent = float ((splitline[-2].replace("|","")).replace("--","")[:-1])*event_count/100
                   name = splitline[-1]
                   dash = line.count("|")

                   line = f.next()
                   if not line.__contains__("|"): #end of main!
                       return list_nodes

                    # sometimes a function calls another one imediately so we should just consider the last one
                   if (not line.__contains__("--")):
                       while (True): #do it till we cosider all the immedite function calls
                            if re.search('[a-zA-Z]+',line) : # if the function is directly call another function immediately
                               name=line.split()[-1]
                               line = f.next()
                            else :
                                break #no immediate calls remain.


                   while(is_valid_variable_name(line.split()[-1])): #read next dashes; sometimes we shoud ignore the next line!!!!! this function consumes neglible cycles (zero) in the perf!!
                       line=f.next()
                   n_dash = line.count("|") #dashes after the function
                   line = f.next()
                   list_nodes.append(Node(name, percent, n_dash, dash))



def build_tree(list_nodes, root_func):
    list_prev =[]
    i=0;

    while (i < len(list_nodes)-1):
        current = list_nodes[i]
        next = list_nodes[i+1]
        if len(list_prev):
            index = [index for index in range(0, len(list_nodes)) if (list_nodes[index].__eq__(list_prev[-1]))]# index of the head node for the stack of dads in the list_nodes!!!

        if (current.n_dash < next.n_dash):
            if (current.dash < next.dash):
                list_nodes[i].kids.append(next)
                list_prev.append(current)
            elif (current.dash == next.dash):
                list_nodes[index[0]].kids.append(next)
            else:
                print("error1! unhandeled situation!")
        elif (current.n_dash == next.n_dash):
            if (current.dash < next.dash):
                list_nodes[i].kids.append(next)
                list_prev.append(current)
            elif (current.dash == next.dash): # do not change the prev
                if (current.dash < current.n_dash):
                    list_nodes[i].kids.append(next)
                elif (current.dash == current.n_dash):
                    list_nodes[index[0]].kids.append(next)
                else:
                    print ("error2! unhandeled situation!")
            else:
                list_nodes[index[0]].kids.append(next)
                list_prev.pop()
        elif (current.n_dash > next.n_dash):
            if (current.dash > next.dash):
                list_nodes[index[0]].kids.append(next)
                list_prev.pop()
            elif (current.dash == next.dash):
                list_nodes[i].kids.append(next)
        i = i+1

    # root_percent = 0
    # for callee in list_nodes[0].kids:
    #     root_percent = root_percent + float(callee.percent)

# file = "/home/hamid/phd/profiling/perf/results/dilithium_recommended/All_Data.txt"
# list_nodes = parse_perf_output(file,"crypto_sign_open",100000)
# build_tree(list_nodes)
# for node in list_nodes:
#     print(node.name+":", end='')
#     for kid in node.kids:
#         print (kid.name+", ",end='')
#     print ("")

# vis_call_graph(list_nodes, 'test')
