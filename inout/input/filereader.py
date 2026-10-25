from classes import *
from classes.grammar.edge import Edge
from classes.grammar.grammar import Grammar
from classes.grammar.graph import Graph


def read(file_name):
    """Uses an own format to read a Graph. Each line is one edge, edges are written as (label, node0, node1, ...).
    Attention: braces, comma and whitespaces must fit!
    Inverse operation of filewriter.write
    :param file_name: full path to the file.
    :returns a graph object, even if the file is not readable. """
    edge_list = []
    with open(file_name, 'r') as file_input:
        for line in file_input:
            info = line[1:-2].split(sep=', ')
            edge_list.append(Edge(info[0], *map(int, info[1:])))
    return Graph(edge_list)


def read_grammar(file_name):
    """Uses an own format to read a Grammar.
    A Line starting with & indicates a new rule.
    Each other line is one edge, edges are written as (label, node0, node1, ...).
    Attention: braces, comma and whitespaces must fit exactly!
    Inverse operation of filewriter.write_grammar
    Note that returns a grammar assuming that each terminal is of rank 2 an size 3.
    :param file_name: full path to the file.
    :returns a grammar object, even if the file is not readable. """
    rules = {}
    next_rule_name = '0'
    edge_list = None
    with open(file_name, 'r') as file_input:
        for line in file_input:
            if line.startswith('&'):
                if edge_list is None:
                    edge_list = []
                else:
                    rules[next_rule_name] = Graph(edge_list)
                    edge_list = []
                next_rule_name = _int_if_possible(line[1:-1])
            else:
                info = line[1:-2].split(sep=', ')
                edge_list.append(Edge(_int_if_possible(info[0]), *map(int, info[1:])))
        rules[next_rule_name] = Graph(edge_list)
    grammar = Grammar(rules[0], lambda x: x not in list(rules.keys()), lambda x: 2, lambda x: 3)
    for rule_name, rule in rules.items():
        grammar.add_rule(rule_name, rule)
    return grammar


def _int_if_possible(value):
    try:
        return int(value)
    except ValueError as e:
        return value
