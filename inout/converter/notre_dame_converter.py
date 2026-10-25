from classes import *
from classes.grammar.edge import Edge
from classes.grammar.grammar import Grammar
from classes.grammar.graph import Graph


def read(file_name):
    """ The Graph read by this function should be formatted as described in the following:
    Lines directly starting with an Hashtag are treated as comments.
    All other lines should include 2 Numbers separated by a whitespace or tab.
    They are treated as node ids containing the information from first to second in order of naming.
    Example for this is http://snap.stanford.edu/data/web-NotreDame.html
    :returns a graph object, even if the file is not readable. """
    edge_list = []
    with open(file_name, 'r') as file_input:
        for line in file_input:
            if line.startswith("#"):
                continue
            infos = line.split()
            edge_list.append(Edge('a', infos[0], infos[1]))
    graph = Graph(edge_list)
    return Grammar(graph, lambda x: x == 'a', lambda _: 2, lambda _: 3)


def read_comments(file_name):
    """Read the lines with an hashtag of a file."""
    comments = []
    with open(file_name, 'r') as file_input:
        for line in file_input:
            if line.startswith("#"):
                comments.append(line)
    return "\n".join(comments)
