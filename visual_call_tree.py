from graphviz import Digraph
from copy import deepcopy


def vis_call_graph(call_tree_in, fname, threshold):
    call_tree = deepcopy(call_tree_in)
    f = Digraph('unix', filename=fname)
    f.node_attr.update(color='lightblue2', style='filled')
    f.attr(label="text inside each node: [function name] ([inclusive percentage], [exclusive percentage]]", size='2,2')

    for caller in call_tree: #key is the caller function
        for callee in caller.kids:
            if float(callee.percent) > threshold:
                f.edge(caller.name,callee.name,str(callee.percent))

 #  f.view()
    f.render()

# call_tree = {'a':[['b',1],['c',2],['d',4],['g',5]],
#              'b':[['g',6]],
#              'c':[['e',7],['f',8]],
#              'e':[['g',9]]}
#vis_call_graph(call_tree, 'test')
