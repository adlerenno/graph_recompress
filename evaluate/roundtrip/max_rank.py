import graphrepair
from functools import reduce

from inout.output import filewriter

import inout.converter.notre_dame_converter as notre_dame

from evaluate import timetest

"""Use this to test the graph algorithm with a restriction to the maximum rank. Auto starts with loading a file."""

# Specify the max allowed rank by editing this field.
max_rank = 12


def get_digram_to_replace_max_rank(digram_count, grammar):
    """ This function will be inserted into the algorithm.
    It only returns digrams with a rank smaller or equal than max_rank."""
    def compare(a, b):
        if a is None:
            return b
        if b is None:
            return a
        a_over_max_rank = (grammar.rank_of_rule(a[0].get_label()) + grammar.rank_of_rule(a[1].get_label())) > max_rank
        b_over_max_rank = (grammar.rank_of_rule(b[0].get_label()) + grammar.rank_of_rule(b[1].get_label())) > max_rank
        if a_over_max_rank and b_over_max_rank:
            return None
        elif a_over_max_rank:
            return b
        elif b_over_max_rank:
            return a
        else:
            return a if digram_count[a] >= digram_count[b] else b
    return reduce(compare, digram_count.keys())


def systematic_grammar_test(grammar):
    """Handle all steps testing a grammar."""
    uncompressed_size = grammar.size_of_hole_grammar()
    graphrepair.repair(grammar)
    min_size = grammar.size_of_hole_grammar()
    log_average_times()
    log('\nMinimal reachable size: {} of {}. Ratio is {}'.format(min_size, uncompressed_size, min_size / uncompressed_size))


def systematic(files):
    """Handles all steps around log and testing a grammar."""
    for input_file, output_file, log_file in files:
        f = open(log_file, 'w')
        timetest.log_file = f
        log(notre_dame.read_comments(input_file))
        grammar = notre_dame.read(input_file)
        systematic_grammar_test(grammar)
        filewriter.write_grammar(output_file, grammar)
        graphrepair.decompress(grammar)
        timetest.clear_average_times()


# Use functional code to replace the selecting function of the algorithm.
# Note, that there are more efficient ways than replacing this function to get the same effect.
graphrepair.get_digram_to_replace = get_digram_to_replace_max_rank

# The following is used to test and save the tested data with more comfort than typing 3 dirs.
help = ('../Testgraphen/Ausgangsgraphen/', '../Testgraphen/compress_max_rank/', '../Testgraphen/results_max_rank/')


def help_files(name):
    return (prefix + name for prefix in help)


files = [help_files('Cit-HepPh.txt')]
systematic(files)
