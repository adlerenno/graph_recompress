import graphrepair
from functools import reduce

from evaluate.timetest import log
from evaluate.timetest.average import log_average_times, clear_average_times
from inout.output import filewriter

import inout.converter.notre_dame_converter as notre_dame

from evaluate import timetest

"""Use this to test the graph algorithm. No movable digram will be considered. Auto starts with loading a file.
The definition of movable is given within the bachelor thesis."""


def get_digram_to_replace_no_moveable(digram_count, grammar):
    """ This function will be inserted into the algorithm.
    It only returns digrams which are not movable."""
    def compare(a, b):
        if a is None:
            return b
        if b is None:
            return a
        a_moveable = a[0].get_label() == a[1].get_label() and a[0].get_connection_type() != a[1].get_connection_type()
        b_moveable = b[0].get_label() == b[1].get_label() and b[0].get_connection_type() != b[1].get_connection_type()
        if not a_moveable and not b_moveable:
            return a if digram_count[a] > digram_count[b] else b
        elif not a_moveable:
            return a
        elif not b_moveable:
            return b
        else:
            return None
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
        clear_average_times()


# Use functional code to replace the selecting function of the algorithm.
# Note, that there are more efficient ways than replacing this function to get the same effect.
graphrepair.get_digram_to_replace = get_digram_to_replace_no_moveable

# The following is used to test and save the tested data with more comfort than typing 3 dirs.
help = ('../Testgraphen/Ausgangsgraphen/', '../Testgraphen/compress_no_moveable/', '../Testgraphen/results_no_moveable/')


def help_files(name):
    return (prefix + name for prefix in help)


files = [help_files('Cit-HepPh.txt')]
systematic(files)
