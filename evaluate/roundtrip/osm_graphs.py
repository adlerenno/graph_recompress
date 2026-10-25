import graphrepair

"""Use the methods of this class to run tests with the osm converter."""


def hypergraph_pc_city():
    tree, m = convert_to_graph('input/paderborncity.osm')

    def is_terminal(rule_name):
        return int(rule_name) <= m

    def rank(rule_name):
        return int(rule_name)

    def size_of(rule_name):
        return int(rule_name) + 1

    grammar = graphrepair.Grammar(tree, is_terminal, rank, size_of)
    begin_size = grammar.size_of_hole_grammar()
    graphrepair.repair(grammar)
    min_size = grammar.size_of_hole_grammar()
    graphrepair.decompress(grammar)
    log('Minimal reachable size: {} of {}. Ratio is {}'.format(min_size, begin_size, min_size/begin_size))

    tree, m = convert_to_graph('input/paderborncity.osm')
    log('Decompressioncheck:', 're-constructable' if tree == grammar.get_start_rule_name() else 'not re-constructable')


def simple_pb_city():
    tree = convert_to_simple_graph('input/paderborncity.osm')

    def is_terminal(rule_name):
        return rule_name == 'a'

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

    # tree, m = convert_to_graph('input/paderborncity.osm')
    # log('Decompressioncheck:', 're-constructable' if tree == grammar.get_start_rule() else 'not re-constructable')
