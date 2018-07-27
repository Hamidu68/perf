from graphviz import Digraph
from copy import deepcopy

def vis_call_graph(call_tree_in, fname, threshold, root_percent):
    call_tree = deepcopy(call_tree_in)
    f = Digraph('unix', filename=fname)
    f.node_attr.update(color='lightblue2', style='filled')
    f.attr(label="text inside each node: [function name] ([inclusive percentage], [exclusive percentage]]", size='2,2')

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

    for caller in call_tree:  # key is the caller function
        if caller.name in in_calls.keys():
            caller.name = caller.name +"\n("+ str(in_calls[caller.name]) +","+ str(in_calls[caller.name]-out_calls[caller.name])+")"
        else:
            caller.name = caller.name + "\n" + str(out_calls[caller.name])





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
