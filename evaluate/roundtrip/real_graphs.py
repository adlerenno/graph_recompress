import graphrepair
from inout.output import filewriter

import inout.converter.notre_dame_converter as notre_dame
from inout import converter as chess, converter as prep

from evaluate import timetest

"""Use this class to test graphs loaded from files. """


def notre_dame_test(input_file, output_file):
    """Simple call to compress a graph written in the syntax of the notre_dame_converter."""
    grammar = notre_dame.read(input_file)
    begin_size = grammar.size_of_hole_grammar()
    graphrepair.repair(grammar)
    min_size = grammar.size_of_hole_grammar()
    filewriter.write_grammar(output_file, grammar)
    graphrepair.decompress(grammar)
    log('Minimal reachable size: {} of {}. Ratio is {}'.format(min_size, begin_size, min_size/begin_size))


def chess_read(input_file='../Testgraphen/Ausgangsgraphen/chess_legal.txt', output_file='../Testgraphen/Ausgangsgraphen/chess_legal_converted.txt'):
    """Simple call to read a graph written in the syntax of the chess_converter."""
    grammar = chess.read(input_file)
    filewriter.write_grammar(output_file, grammar)
    return grammar


def chess_test(input_file, output_file):
    """Simple call to compress a graph written in the syntax of the chess_converter."""
    grammar = chess.read(input_file)
    begin_size = grammar.size_of_hole_grammar()
    graphrepair.repair(grammar)
    min_size = grammar.size_of_hole_grammar()
    filewriter.write_grammar(output_file, grammar)
    graphrepair.decompress(grammar)
    log('Minimal reachable size: {} of {}. Ratio is {}'.format(min_size, begin_size, min_size/begin_size))


def systematic_grammar_test(grammar):
    """Handle all steps testing a grammar."""
    uncompressed_size = grammar.size_of_hole_grammar()
    graphrepair.repair(grammar)
    min_size = grammar.size_of_hole_grammar()
    log_average_times()
    log('\nMinimal reachable size: {} of {}. Ratio is {}'.format(min_size, uncompressed_size, min_size / uncompressed_size))


def systematic_file_test(files, converter):
    """Handles all steps around log and testing a grammar.
    Note that you can pass converters in there here. Python allows modules as parameters as well."""
    for input_file, output_file, log_file in files:
        f = open(log_file, 'w')
        timetest.log_file = f
        log(converter.read_comments(input_file))
        grammar = converter.read(input_file)
        systematic_grammar_test(grammar)
        filewriter.write_grammar(output_file, grammar)
        graphrepair.decompress(grammar)
        clear_average_times()


def systematic_real_graph_test():
    """The following is used to test and save the tested data with more comfort than typing 3 dirs."""
    help = ('../Testgraphen/Ausgangsgraphen/', '../Testgraphen/compress/', '../Testgraphen/results/')

    def help_files(name):
        return (prefix + name for prefix in help)

    files = [help_files('ttt_win.txt')]
    systematic_file_test(files, chess)


def convert_chess_to_georgi_format():
    """Used to convert multiple files with the georgi_converter."""
    help = ('../Testgraphen/Ausgangsgraphen/', '../Testgraphen/georgi/', '../Testgraphen/results/')

    def help_files(name):
        return (prefix + name for prefix in help)

    files = [help_files('chess_legal.txt')]
    for input_file, output_file, log_file in files:
        prep.read(input_file, output_file)

