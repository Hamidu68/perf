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
        self.kids = [] #keeps id of the kids!

    def __eq__(self, other):
        return (self.name == other.name and self.percent ==other.percent)

def parse_perf_output (Raw_Data,threshold):
    list_nodes = []
    with open(Raw_Data, 'r') as f:
       for line in f:
           # read the call percentage for each function which is contain '[.]'. if there is no call to this function
           # ignore the line!
           if ((line.__contains__("[.] main"))):
               while( not line.__contains__("|--")):#start of the tree
                   line = f.next()
               while (line.__contains__("|")):
                   splitline = line.split() #ex: --17.95%-- char_pool_refresh
                   percent = (splitline[-2].replace("|","")).replace("--","")
                   name = splitline[-1]
                   dash = line.count("|")
                   line = f.next()
                   while(is_valid_variable_name(line.split()[-1])): #read next dashes; sometimes we shoud ignore the next line!!!!! this function consumes neglible cycles (zero) in the perf!!
                       line=f.next()
                   n_dash = line.count("|") #dashes after the function
                   line = f.next()
                   #if float(percent[:-1]) >= threshold :
                   list_nodes.append(Node(name, percent, n_dash, dash))
    return list_nodes


def build_tree(list_nodes):
    list_prev =[]
    i=0;
    prev_index=0

    #first node should be the main()
    list_nodes.insert(0,Node("main","100",0,0))
    list_prev.append(list_nodes[0])

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


# file = "/home/hamid/phd/profiling/perf/All_Data.txt"
# list_nodes = parse_perf_output(file,0.10)
# build_tree(list_nodes)
# for node in list_nodes:
#     print(node.name+":", end='')
#     for kid in node.kids:
#         print (kid.name+", ",end='')
#     print ("")
#
# vis_call_graph(list_nodes, 'test')