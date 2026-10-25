from classes.grammar.graph import Graph
from evaluate import timetest
from evaluate.timetest.average import log_average_times
from evaluate.timetest.normal import time_function
from inout.input.random_graph_generator import random_grammar, random_3_grammar
from recompress import recompress, decompress


def random_test(vertex_count=1000, edge_count=5000, rule_count=2, labels=None):
    """Creates a random graph with the given characteristics.
    :returns size of the compressed graph and the size of the graph before it was compressed."""
    if labels is None:
        labels = ['a', 'b', 'c']
    grammar = random_grammar(vertex_count, edge_count, rule_count, labels, {label: 2 for label in labels})
    # grammar2 = grammar.clone()
    begin_size = grammar.size_of_hole_grammar()

    ret, time_directly_recompress_function = time_function(recompress, grammar)
    directly_compressed = grammar.size_of_hole_grammar()
    grammar = decompress(ret)
    decompressed_size = grammar.size_of_hole_grammar()
    return begin_size, decompressed_size, directly_compressed, time_directly_recompress_function


def single_test():
    timetest.log_file = open('../../../Testgraphen/results/results_recompress_single_random_grammar_output_9.txt', 'w')
    data_file = open('../../../Testgraphen/results/results_recompress_single_random_grammar_output_9.csv', 'w')
    data_file.write('Edge Count;Vertex Count;Begin size;Decompressed Size;Recompressed Size;Time Recompression;\n')
    begin_size, decompressed_size, directly_compressed, time_directly_recompress_function \
        = random_test(vertex_count=1,
                      edge_count=200,
                      rule_count=2,
                      labels=['a'])
    # timetest.log_file.close()
    data_file.write(
        f'{100}; {1000}; {begin_size}; {decompressed_size}; {directly_compressed}; {time_directly_recompress_function}\n')
    data_file.flush()
    data_file.close()
    log_average_times()
    timetest.log_file.flush()
    timetest.log_file.close()

single_test()
