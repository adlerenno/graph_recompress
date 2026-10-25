import xml.etree.ElementTree as ET
from classes import *

"""Can be used to load osm data. It's simply xml, so the xml.etree package is used."""


def convert_to_graph(input_file):
    """Used to read osm file from open street map. It's XML Data and there are 3 kinds of children for the root: nodes,
    relations and ways. Only uses nodes and ways to generate the graph. The Label of an Edge is the same as it's rank.
    This can lead to edges with a rank over 380."""
    g = Graph()
    root = ET.parse(input_file).getroot()
    node_dir = {}
    m = 0
    nodes = root.findall('node')
    for i, type_tag in zip(range(len(nodes)), nodes):
        node_dir[type_tag.get('id')] = i
    for way in root.findall('way'):
        nodes = [node_dir[nd.get('ref')] for nd in way.findall('nd')]
        m = max(m, len(nodes))
        g += Edge(len(nodes), *nodes)
    return g, m


def convert_to_simple_graph(input_file):
    """As above, but I understand every way as a clique. So if a way has rank 3, there are generated 3 directed Edges
    to connect the first to the second, the first to the third and the second towards the third. """
    g = Graph()
    root = ET.parse(input_file).getroot()
    node_dir = {}
    nodes = root.findall('node')
    for i, type_tag in zip(range(len(nodes)), nodes):
        node_dir[type_tag.get('id')] = i
    for way in root.findall('way'):
        nodes = [node_dir[nd.get('ref')] for nd in way.findall('nd')]
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                g += Edge('a', nodes[i], nodes[j])
    return g


if __name__ == '__main__':
    # convert('paderborncity.osm', 'paderborncity.txt')
    pass
