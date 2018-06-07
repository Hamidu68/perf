import re
from ast import parse

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
                   if float(percent[:-1]) >= threshold :
                       list_nodes.append(Node(name, percent, dash, n_dash))
    return list_nodes


# file = "/home/hamid/phd/profiling/perf/All_Data.txt"
# list_nodes = parse_perf_output(file,0.10)
#
# for node in list_nodes:
#     print(node.name+" "+node.percent+" "+str(node.n_dash)+" "+str(node.dash))

