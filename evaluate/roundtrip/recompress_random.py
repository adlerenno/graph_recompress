from functools import reduce

from classes.grammar.graph import Graph
from evaluate import timetest
from evaluate.timetest import log
from evaluate.timetest.average import log_average_times
from evaluate.timetest.normal import timing, time_function
from inout.input.random_graph_generator import random_grammar, random_base_grammar
from recompress import recompress, decompress

"""Use this class to test random generated graphs."""


def random_test(vertex_count=1000, edge_count=5000, split_count=5, labels=None):
    """Creates a random graph with the given characteristics.
    :returns size of the compressed graph and the size of the graph before it was compressed."""
    if labels is None:
        labels = ['a', 'b', 'c']
    grammar = random_base_grammar(vertex_count, edge_count, labels, {label: 2 for label in labels})
    # grammar2 = grammar.clone()
    begin_size = grammar.size_of_hole_grammar()

    start_rule = grammar[grammar.get_start_rule_name()]
    start_rule_edge_count = len(start_rule.get_edges())
    step_size = start_rule_edge_count // split_count
    edges_of_start_rule = []
    rules = {}  # bookkeep rules, because they are deleted in pruning
    for i in range(split_count):
        grammar[0] = Graph(start_rule.get_edges()[step_size*i:step_size*(i+1)])
        recompress(grammar)
        edges_of_start_rule.extend(grammar[0].get_edges())
        rules.update(grammar._rules)

    grammar[0] = Graph(edges_of_start_rule + start_rule.get_edges()[step_size*split_count:])
    for rule_name in rules.keys():
        if rule_name is not 0:
            grammar[rule_name] = rules[rule_name]
    print(grammar)

    single_min_size = grammar.size_of_hole_grammar()
    ret, time_recompress_function = time_function(recompress, grammar)
    recompressed_size = grammar.size_of_hole_grammar()
    decompress(grammar)
    decompressed_size = grammar.size_of_hole_grammar()
    return begin_size, single_min_size,  recompressed_size, decompressed_size, time_recompress_function


def systematic_random_graph_test():
    """Tests complete sets of characteristics and write them to a file"""
    data_file = open('../../../Testgraphen/results/results_recompress_random_grammar_4.csv', 'w')
    data_file.write('Edge Count;Vertex Count;Begin size;Steps Recompressed Size;Recompressed Size;Decompressed Size;'
                    + 'Time Recompression;\n')
    for edge_count in (2000,):
        for vertex_count in (500,):
            for labels in (['a'],):
                for _ in range(1):
                    timetest.log_file = open('../../../Testgraphen/results/random_{}_{}_{}.txt'.format(edge_count, vertex_count, ''.join(labels)), 'w')
                    begin_size, single_min_size, recompressed_size, decompressed_size, time_recompress_function, \
                        = random_test(vertex_count=vertex_count,
                                      edge_count=edge_count,
                                      split_count=5,
                                      labels=labels)
                    timetest.log_file.close()
                    data_file.write(f'{edge_count}; {vertex_count}; {begin_size}; {single_min_size}; {recompressed_size}; {decompressed_size}; {time_recompress_function};\n')
                    data_file.flush()
    data_file.close()

systematic_random_graph_test()
