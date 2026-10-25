from classes.grammar.grammar import Grammar
from evaluate.timetest import log
from inout.input import recursive_graph_generator

from recompress import recompress, decompress

""" By loading this class, the graph compression algorithm is tested with tree graphs."""


def tree(depth):
    tree = recursive_graph_generator.generate_tree(depth)

    def is_terminal(rule_name):
        return type(rule_name) is not int

    def rank(rule_name):
        return 2

    def size_of(rule_name):
        return 3

    grammar = Grammar(tree, is_terminal, rank, size_of)
    begin_size = grammar.size_of_hole_grammar()
    recompress(grammar)
    min_size = grammar.size_of_hole_grammar()
    decompressed = decompress(grammar)
    decompress_check = decompressed.get_start_rule_name() == recursive_graph_generator.generate_tree(depth)
    log('Decompressioncheck: ' + str(decompress_check))
    assert decompress_check
    log('Minimal reachable size: {} of {}. Ratio is {}'.format(min_size, begin_size, min_size/begin_size))


for i in range(3, 14):
    # timetest.log_file = open('results/tree'+str(i)+'.txt', 'w')
    tree(i)
    # timetest.log_file.close()
