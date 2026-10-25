def write(file_name, graph):
    """Uses an own format to write a Graph. Each line is one edge, edges are written as (label, node0, node1, ...).
    Attention: braces, comma and whitespaces must fit!
    Inverse operation of filereader.read
    Only writes, when the file is writeable. No error otherwise.
    :param file_name: complete path to the file.
    :param graph: graph to write to the file."""
    with open(file_name, 'w') as output_file:
        for edge in graph.get_edges():
            output_file.write('({}, {})\n'.format(edge.get_label(), ', '.join(map(str, edge.get_nodes()))))


def write_grammar(file_name, grammar):
    """Uses an own format to write a Grammar.
    A new rule is introduced by an & and the name of the rule without any whitespaces. This is in an own single line.
    Each line between is one edge, edges are written as (label, node0, node1, ...).
    Attention: braces, comma and whitespaces must fit!
    Inverse operation of filereader.read
    Only writes, when the file is writeable. No error otherwise.
    :param file_name: complete path to the file.
    :param grammar: grammar to write to the file."""
    with open(file_name, 'w') as output_file:
        for rule_name in grammar:
            output_file.write('&{}\n'.format(rule_name))
            graph = grammar[rule_name]
            for edge in graph.get_edges():
                output_file.write('({}, {})\n'.format(edge.get_label(), ', '.join(map(str, edge.get_nodes()))))