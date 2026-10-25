"""Methods of this file are used to automatically write a graph in LaTeX Code. There is no great logic behind
placing the nodes. I use a self-defined Environment named graph. """


def graph_to_formal_definition(graph):
    """Converts a graph to a list of edges written in latex."""
    list_of_edges = "\\), \\(".join((edge_to_formal_definition(e) for e in graph._edges))
    return f'E = {{\\({list_of_edges}\\)}}'


def edge_to_formal_definition(edge):
    """Converts an Edge to a LaTeX code."""
    return "({})".format(", ".join([edge._label, *(str(v) for v in edge._nodes)]))


def graph_to_tikzpicture(graph):
    """Uses tikz to paint a graph."""
    start = '\\begin{graph}{Caption} \n'
    sorted_vertex_list = list({node for e in graph._edges for node in e._nodes})
    sorted_vertex_list.sort()
    for v in sorted_vertex_list:
        start += _node_latex(v) + "\n"
    start += '\\path \n'
    for e in graph._edges:
        start += _edge_latex(e) + '\n'
    start += '; \n\\end{graph}'+ '\n'
    return start


def _node_latex(node):
    """Help method to create node statements."""
    return '\\node [bordered] (v{node}) {near_to} {open}\\({node}\\){close};'.format(node=node, near_to=_near_to(node), open='{', close='}')


def _near_to(node):
    """help method to create near to statements for nodes."""
    if node is 0:
        return "at (0,0)"
    elif node % 4 is 0:
        return "[below of=v{}]".format(node-4)
    else:
        return "[right of=v{}]".format(node-1)


def _edge_latex(edge):
    """Help method to create edge statements. Node that an Hyperedge need isn't really supported within latex."""
    if edge.is_hyperedge():
        return '\\hyperedge{{{label}}}{nodes}'.format(label=edge._label, nodes="".join(sum(map(lambda x: "{{v{}}}".format(x), edge.get_nodes()))))
        # if edge.rank() == 3:
        #     return '\\hyperedge{{{label}}}{{v{v1}}}{{v{v2}}}{{v{v3}}}'.format(label=edge.label, v1=edge.nodes[0], v2=edge.nodes[1], v3=edge.nodes[2])
        # elif edge.rank() == 5:
        #     return '\\hyperedgefive{{{label}}}{{v{v1}}}{{v{v2}}}{{v{v3}}}{{v{v4}}}{{v{v5}}}'.format(label=edge.label, v1=edge.nodes[0], v2=edge.nodes[1], v3=edge.nodes[2], v4=edge.nodes[3], v5=edge.nodes[4])
    elif edge.is_loop():
        return '(v{}) edge [loop right] node [above]{open}{label}{close} (v{})'.format(edge.get_nodes()[0], edge.get_nodes()[1], label=edge.get_label(), open='{', close='}')
    else:
        return '(v{}) edge [bend left] node [above]{open}{label}{close} (v{})'.format(edge.get_nodes()[0], edge.get_nodes()[1], label=edge.get_label(), open='{', close='}')
