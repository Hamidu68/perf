from __future__ import print_function
from parse_perf_output import parse_perf_output
from parse_perf_output import Node

# list_nodes=[]
# list_nodes.append(Node('a',10,2,1))
# list_nodes.append(Node('b',10,3,2))
# list_nodes.append(Node('c',10,4,3))
# list_nodes.append(Node('d',10,5,4))
# list_nodes.append(Node('e',10,5,4))
# list_nodes.append(Node('f',10,5,4))
# list_nodes.append(Node('g',10,6,5))
# list_nodes.append(Node('h',10,7,6))
# list_nodes.append(Node('i',10,7,7))
# list_nodes.append(Node('j',10,6,6))
# list_nodes.append(Node('k',10,7,6))
# list_nodes.append(Node('l',10,6,6))
# list_nodes.append(Node('m',10,5,5))
# list_nodes.append(Node('n',10,4,4))
# list_nodes.append(Node('n',10,3,3))
# list_nodes.append(Node('p',10,4,3))
# list_nodes.append(Node('q',10,5,4))

def build_tree(list_nodes):
    list_prev =[]
    i=0;
    prev_index=0
    while (i < len(list_nodes)-1):
        current = list_nodes[i]
        next = list_nodes[i+1]
        if len(list_prev):
            index = [index for index in range(0, len(list_nodes)) if (list_nodes[index].__eq__(list_prev[-1]))]# index of the head node for the stack of dads in the list_nodes!!!

        if (current.n_dash < next.n_dash):
            if (current.dash < next.dash):
                list_nodes[i].kids.append(next)
                list_prev.append(current)
            elif (current.dash == current.dash):
                list_nodes[index[0]].kids.append(next)
        elif (current.n_dash == next.n_dash):
            if (current.dash < next.dash):
                list_nodes[i].kids.append(next)
                list_prev.append(current)
            elif (current.dash == next.dash): # do not change the prev
                list_nodes[i].kids.append(next)
        elif (current.n_dash > next.n_dash):
            if (current.dash > next.dash):
                list_nodes[index[0]].kids.append(next)
                list_prev.pop()
            elif (current.dash == next.dash):
                list_nodes[i].kids.append(next)
        i = i+1


file = "/home/hamid/phd/profiling/perf/All_Data.txt"
list_nodes = parse_perf_output(file,0.10)
build_tree(list_nodes)
for node in list_nodes:
    print(node.name+":", end='')
    for kid in node.kids:
        print (kid.name+", ",end='')
    print ("")