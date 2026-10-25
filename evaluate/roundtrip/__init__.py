import os

from evaluate import timetest
from evaluate.timetest import log
from evaluate.timetest.average import log_average_times, clear_average_times
from inout.output import filewriter
from recompress import recompress, decompress
import inout.converter.notre_dame_converter as notre_dame


def systematic_grammar_test(grammar):
    """Handle all steps testing a grammar."""
    uncompressed_size = grammar.size_of_hole_grammar()
    recompress(grammar)
    min_size = grammar.size_of_hole_grammar()
    log_average_times()
    log('\nMinimal reachable size: {} of {}. Ratio is {}'.format(min_size, uncompressed_size, min_size / uncompressed_size))


def systematic(files):
    """Handles all steps around log and testing a grammar."""
    for input_file, output_file, log_file in files:
        try:
            f = open(log_file, 'w')
            timetest.log_file = f
            log(notre_dame.read_comments(input_file))
            grammar = notre_dame.read(input_file)
            systematic_grammar_test(grammar)
            filewriter.write_grammar(output_file, grammar)
            decompress(grammar)
            clear_average_times()
        except BaseException as e:
            log(e.__str__())


# The following is used to test and save the tested data with more comfort than typing 3 dirs.
help = ('../../../Testgraphen/Ausgangsgraphen/', '../../../Testgraphen/compress/', '../../../Testgraphen/results/')


def help_files(name):
    return (prefix + name for prefix in help)


files = [help_files('Wiki-Vote.txt')]
systematic(files)
