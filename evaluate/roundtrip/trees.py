
from inout.input import recursive_graph_generator
import graphrepair

from evaluate import timetest


def tree(depth):
    """Does everything around testing a recursively generated tree. See recursive_graph_generator.py"""
    tree = recursive_graph_generator.generate_tree(depth)

    def is_terminal(rule_name):
        return type(rule_name) is not int

    def rank(rule_name):
        return 2

    def size_of(rule_name):
        return 3

    grammar = graphrepair.Grammar(tree, is_terminal, rank, size_of)
    begin_size = grammar.size_of_hole_grammar()
    graphrepair.repair(grammar)
    min_size = grammar.size_of_hole_grammar()
    graphrepair.decompress(grammar)
    log('Minimal reachable size: {} of {}. Ratio is {}'.format(min_size, begin_size, min_size/begin_size))


# Tests on load the file.
for i in range(16, 19):
    timetest.log_file = open('results/tree' + str(i) + '.txt', 'w')
    tree(i)
    timetest.log_file.close()

# the lines below were the first roundtrip code in this project. You can see the usage of the latex.py and testings of
# subalgorithms of the repair algorithm.

#tree = graphgenerator.generate_tree(5)
#log('Decompressioncheck:', 're-constructable' if tree == grammar.get_start_rule() else 'not re-constructable')

#log(tree)
#log(len(tree))
#tex = latex.graph_to_formal_definition(tree)
#log(tex)
#view = latex.graph_to_tikzpicture(tree)
#log(view)
#node_edge_adjacency_dir = graphrepair.create_node_edge_adjacency_dir(tree)
#occurence_count_dir = graphrepair.count_digrams(node_edge_adjacency_dir)
#digram_to_replace = graphrepair.get_digram_to_replace(occurence_count_dir)
#rc = graphrepair.RuleCreator(digram_to_replace, grammar)
#log(node_edge_adjacency_dir)
#log(occurence_count_dir)
#log(digram_to_replace)
#log(rc.get_rule())
#log(graphrepair.find_occurence_of_digram(digram_to_replace, tree))
#log(tree[2], tree[3])
#log(rc.get_hyperedge_for_edges(tree[2], tree[3]))
#log('Decompressioncheck:', 're-constructable' if tree == grammar.get_start_rule() else 'not re-constructable')
#tree = graphgenerator.generate_tree_hyperedge(4)
#log(tree)
#log(len(tree))
#tex = latex.graph_to_formal_definition(tree)
#log(tex)
#view = latex.graph_to_tikzpicture(tree)
#log(view)

#loops = graphgenerator.generate_loops(10)
#grammar = graphrepair.Grammar(loops)
#graphrepair.repair(grammar)
#log('Minimal reachable size:', grammar.size_of_hole_grammar())
#log(grammar)
#graphrepair.decompress(grammar)
#loops = graphgenerator.generate_loops(10)
#log('Decompressioncheck:', 're-constructable' if loops == grammar.get_start_rule() else 'not re-constructable')
