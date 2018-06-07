from graphviz import Digraph

# call_tree = {'a':[['b',1],['c',2],['d',4],['g',5]],
#              'b':[['g',6]],
#              'c':[['e',7],['f',8]],
#              'e':[['g',9]]}


def vis_call_graph(call_tree, fname):
    f = Digraph('unix', filename=fname)
    f.attr(size='2,2')
    f.node_attr.update(color='lightblue2', style='filled')

    for caller in call_tree: #key is the caller function
        for callee in caller.kids:
            f.edge(caller.name,callee.name,callee.percent)

 #   f.view()
    f.render()

#vis_call_graph(call_tree, 'test')
